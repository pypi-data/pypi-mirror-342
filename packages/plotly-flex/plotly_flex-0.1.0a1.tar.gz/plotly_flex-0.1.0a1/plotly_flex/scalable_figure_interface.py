import re
import itertools
import time
import polars as pl

from plotly.basedatatypes import BaseFigure, BaseTraceType
from abc import ABC
from uuid import uuid4
from dataclasses import dataclass


from typing import List, Iterable, Optional, Dict, Union, Tuple

from .LF import LFQueryBuilder, AggregationSpec
from .trace.scalable_trace_interface import AbstractScalableTrace
from .trace.mapping import _SCALABLE_TRACES


@dataclass
class Selection:
    x_ref: str  # subplot x-axis anchor
    y_ref: str  # subplot y-axis anchor
    x_range: Optional[Tuple[float, float]]
    y_range: Optional[Tuple[float, float]]


class AbstractScalableFigure(BaseFigure, ABC):
    """Abstract interface for data aggregation functionality for plotly figures."""

    def __init__(
        self,
        figure: BaseFigure,
        # TODO: make Optional[Dict[str, Union[pl.DataFrame, pl.LazyFrame]]]?
        backend_data: Union[pl.DataFrame | pl.LazyFrame] = None,
        row_index_col: Optional[str | pl.Expr] = None,
        convert_existing_traces: bool = True,
        verbose: bool = False,
    ):
        if backend_data is not None:
            # Transform to a LFQueryBuilder (which encapsulates a LazyFrame)
            backend_data = LFQueryBuilder(backend_data, row_index_col)
        self._backend_lf: Optional[LFQueryBuilder] = backend_data
        self._scalable_traces: Dict[str, AbstractScalableTrace] = {}  # key = uuid
        # Note: selections will only be used & populated when backend_data is not None
        self._front_end_selections: List[Selection] = []
        self._print_verbose = verbose

        # Given figure should always be a BaseFigure that is not wrapped by
        # a scalable-figure class
        assert isinstance(figure, BaseFigure)
        assert not issubclass(type(figure), AbstractScalableFigure)
        self._figure_class = figure.__class__

        if convert_existing_traces:
            # call __init__ with the correct layout and set the `_grid_ref` of the
            # to-be-converted figure
            f_ = self._figure_class(layout=figure.layout)
            f_._grid_str = figure._grid_str
            f_._grid_ref = figure._grid_ref
            super().__init__(f_)

            # make sure that the UIDs of these traces do not get adjusted
            self._data_validator.set_uid = False
            self.add_traces(figure.data)
        else:
            super().__init__(figure)
            self._data_validator.set_uid = False

        # A list of al xaxis and yaxis string names
        # e.g., "xaxis", "xaxis2", "xaxis3", .... for _xaxis_list
        self._xaxis_list = self._re_matches(
            re.compile(r"xaxis\d*"), self._layout.keys()
        )
        self._yaxis_list = self._re_matches(
            re.compile(r"yaxis\d*"), self._layout.keys()
        )
        # edge case: an empty `go.Figure()` does not yet contain axes keys
        if not len(self._xaxis_list):
            assert not len(self._yaxis_list)
            # TODO: what if not xy axis is present?
            self._xaxis_list = ["xaxis"]
            self._yaxis_list = ["yaxis"]

        # Make sure to reset the layout its range
        # self.update_layout(
        #     {
        #         axis: {"autorange": None, "range": None}
        #         for axis in self._xaxis_list + self._yaxis_list
        #     }
        # )

    def _print(self, *values):
        """Helper method for printing if ``verbose`` is set to True."""
        if self._print_verbose:
            print(*values)

    @staticmethod
    def _add_trace_to_add_traces_kwargs(kwargs: dict) -> dict:
        """Convert the `add_trace` kwargs to the `add_traces` kwargs."""
        # The keywords that need to be converted to a list
        convert_keywords = ["row", "col", "secondary_y"]

        updated_kwargs = {}  # The updated kwargs (from `add_trace` to `add_traces`)
        for keyword in convert_keywords:
            value = kwargs.pop(keyword, None)
            if value is not None:
                updated_kwargs[f"{keyword}s"] = [value]
            else:
                updated_kwargs[f"{keyword}s"] = None

        return {**kwargs, **updated_kwargs}

    def add_trace(self, trace, **kwargs):
        # To comply with the plotly data input acceptance behavior
        if isinstance(trace, (list, tuple)):
            raise ValueError("Trace must be either a dict or a BaseTraceType")
        # Validate the trace and convert to a trace object
        if not isinstance(trace, BaseTraceType):
            trace = self._data_validator.validate_coerce(trace)[0]
        assert isinstance(trace, BaseTraceType)

        # Add a UUID, as each (even the non-scalable traces), must contain this
        # key for comparison. If the trace already has a UUID, we will keep it.
        uuid_str = str(uuid4()) if trace.uid is None else trace.uid
        trace.uid = uuid_str

        if trace.plotly_name.startswith("[SCALABLE] "):
            assert isinstance(trace, AbstractScalableTrace)
            self._print("Adding a scalable trace", trace["uid"])
            trace._validate_figure_data(self._backend_lf)
            self._scalable_traces[trace["uid"]] = trace
        elif trace.plotly_name in _SCALABLE_TRACES:
            assert not isinstance(trace, AbstractScalableTrace)
            self._print("Creating a scalable trace", trace["uid"])
            trace = _SCALABLE_TRACES[trace.plotly_name](**trace._props)
            assert isinstance(trace, AbstractScalableTrace)
            trace.uid = uuid_str  # TODO: check if this is needed
            trace._validate_figure_data(self._backend_lf)
            self._scalable_traces[trace["uid"]] = trace
        return super().add_traces(
            [trace], **AbstractScalableFigure._add_trace_to_add_traces_kwargs(kwargs)
        )

    def add_traces(self, data, **kwargs):
        # Plotly its add_traces also allows non list-like data (e.g. a single trace)
        if not isinstance(data, (list, tuple)):
            data = [data]

        # Convert each trace into a BaseTraceType object
        data = [
            (
                self._data_validator.validate_coerce(trace)[0]
                if not isinstance(trace, BaseTraceType)
                else trace
            )
            for trace in data
        ]

        # TODO: THIS IS DIFFERENT FROM PLOTLY-RESAMPLER
        for trace in data:
            self.add_trace(trace, **kwargs)

        return self

    @staticmethod
    def _get_trace_axes(trace: BaseTraceType) -> Tuple[str, str]:
        """Get the x and y axis anchor of the trace.

        Parameters
        ----------
        trace: BaseTraceType
            The trace for which the x and y axis anchor will be returned.

        Returns
        -------
        Optional[Tuple[str, str]]:
            A tuple with the x and y axis anchor of the trace. If the trace does not
            have an x and y axis anchor, None will be returned.
        """
        # TODO: coupling with supported axes => perhaps rename this method
        if hasattr(trace, "xaxis") and hasattr(trace, "yaxis"):
            return trace["xaxis"] or "x", trace["yaxis"] or "y"
        return None

    @staticmethod
    def _get_selection_range(
        selection_dict, prefix: Optional[str] = None
    ) -> Dict[str, Tuple[float, float]]:
        """Get the x and y range of the selection.

        Parameters
        ----------
        selection_dict: Dict[str, Any]
            A dict containing the selection data.
        prefix: Optional[str]
            The prefix of the selection keys.

        Returns
        -------
        Tuple[Tuple[float, float], Tuple[float, float]]:
            A tuple with the x and y range of the selection.
        """
        if prefix is None:
            prefix = ""

        # Iterate over x and y together  # TODO: improve coupling with supported axes
        ranges = {}
        for axis in ["x", "y"]:
            ranges[axis] = tuple(
                sorted(
                    [
                        selection_dict[f"{prefix}{axis}0"],
                        selection_dict[f"{prefix}{axis}1"],
                    ]
                )
            )
        return ranges

    def _get_selections(self) -> Dict[Tuple[str, str], Dict[str, Tuple[float, float]]]:
        """Get the selections for each subplot.

        Returns
        -------
        Dict[Tuple[str, str], Dict[str, Tuple[float, float]]]:
            A dict with the subplot its x and y anchor as key and as value a dict with
            the x and y range of the selection.
        """
        selections = {}
        for selection in self._front_end_selections:
            x_ref, y_ref = selection.x_ref, selection.y_ref
            x_range, y_range = selection.x_range, selection.y_range
            selections[(x_ref, y_ref)] = {"x": x_range, "y": y_range}
        return selections

    def _construct_update_data(
        self,
        relayout_data: dict,
        force_update: bool = False,
    ) -> Union[List[dict], None]:
        """Construct the to-be-updated front-end data, based on the layout change.

        Parameters
        ----------
        relayout_data: dict
            A dict containing the ``relayoutData`` (i.e., the changed layout data) of
            the corresponding front-end graph.
        force_update: bool
            If True, all scalable traces will be updated. If False, only the traces that
            are affected by the front-end event will be updated.

        Returns
        -------
        List[dict]:
            A list of dicts, where each dict-item is a representation of a trace its
            *data* properties which are affected by the front-end layout change. |br|
            In other words, only traces which need to be updated will be sent to the
            front-end. Additionally, each trace-dict withholds the *index* of its
            corresponding position in the ``figure[data]`` array with the ``index``-key
            in each dict.

        """
        if relayout_data or force_update:
            # flatten the possibly nested dict using '.' as separator
            # relayout_data = nested_to_record(relayout_data, sep=".")
            self._print("-" * 100 + "\n", "changed layout", relayout_data)

            cl_k = list(relayout_data.keys())

            # ----------------------- ZOOMING & PANNING -----------------------
            ## -------------- Classic axis range update --------------
            update_range = {}  # key = axis anchor, value = (start, stop)
            anchors = self._layout_axes_to_trace_axes_mapping()
            for axis in ["xaxis", "yaxis"]:  # TODO: support more axes?
                # 1. Base case - there is an axis-range specified in the front-end
                start_matches = self._re_matches(
                    re.compile(rf"{axis}\d*.range\[0]"), cl_k
                )
                stop_matches = self._re_matches(
                    re.compile(rf"{axis}\d*.range\[1]"), cl_k
                )

                if start_matches and stop_matches:
                    for t_start_key, t_stop_key in zip(start_matches, stop_matches):
                        # Check if the axis<NUMB> part of axis<NUMB>.[0-1] matches
                        # => could be xaxis, xaxis2, xaxis3, ... (or yaxis, yaxis2, ...)
                        axis_match = t_start_key.split(".")[0]
                        assert axis_match == t_stop_key.split(".")[0]
                        for anchor in anchors[axis_match]:
                            update_range[anchor] = (
                                relayout_data[t_start_key],
                                relayout_data[t_stop_key],
                            )

                # 2. The user clicked on either autorange | reset axes
                autorange_matches = self._re_matches(
                    re.compile(rf"{axis}\d*.autorange"), cl_k
                )
                spike_matches = self._re_matches(
                    re.compile(rf"{axis}\d*.showspikes"), cl_k
                )
                # 2.1 Reset-axes -> autorange & reset to the global data view
                if autorange_matches and spike_matches:  # when both are not empty
                    for autorange_key in autorange_matches:
                        if relayout_data[autorange_key]:
                            axis_match = autorange_key.split(".")[0]
                            for anchor in anchors[axis_match]:
                                update_range[anchor] = None
                # TODO -> this is hotfixed now via the reset axis button
                # # 2.1. Autorange -> do nothing, the autorange will be applied on the
                # #      current front-end view
                # elif (
                #     autorange_matches and not spike_matches
                # ):  # when only autorange is not empty
                #     # PreventUpdate returns a 204 status code response on the
                #     # relayout post request
                #     return None

            # --------------- (scatter)Map-based traces ----------
            # NOTE: We need to first check for the center (as the ._derived suffix)
            #       is more specific than the center itself
            for map_ in self._re_matches(re.compile(r"map\d*\.center"), cl_k):
                update_range[map_.split(".")[0]] = relayout_data[map_]
            for map_ in self._re_matches(re.compile(r"map\d*\._derived"), cl_k):
                # note: the `._derived` suffix is used for coordinates changes
                update_range[map_.rstrip("._derived")] = relayout_data[map_]

            # ----------------------- SELECTION -----------------------
            # Get / update the front-end selections
            selection_matches = self._re_matches(
                re.compile(r"selections\[\d+\]\.[xy][01]"), cl_k
            )
            # Traces that need to be updated due to filtering changes (due to selection
            # changes)
            filtered_traces = set()

            if "selections" in cl_k and self._backend_lf is not None:
                # Case 1: 'selections' is in relayout_data => all front-end selections
                # are included => we can full update the _front_end_selections
                assert len(selection_matches) == 0
                if not relayout_data["selections"]:  # the selections have been reset
                    # Store which traces were being filtered
                    for selection in self._front_end_selections:
                        selection_axes = (selection.x_ref, selection.y_ref)
                        # Find all traces that are NOT in this selection
                        for trace in self.data:
                            uuid = trace["uid"]
                            tr_axes = self._get_trace_axes(trace)
                            # Only update traces that are not in the current selection
                            # (those that were being filtered by the selection)
                            if (
                                uuid in self._scalable_traces
                                and tr_axes is not None
                                and tr_axes != selection_axes
                            ):
                                filtered_traces.add(uuid)

                    # Clear the selections
                    self._front_end_selections = []
                    del relayout_data["selections"]
                    assert len(relayout_data) == 0

                # there are one or more selections
                else:
                    selections = []
                    for selection in relayout_data["selections"]:
                        x_ref, y_ref = selection["xref"], selection["yref"]
                        if selection["type"] == "rect":
                            ranges = self._get_selection_range(selection)
                            selections += [
                                Selection(x_ref, y_ref, ranges["x"], ranges["y"])
                            ]
                    self._front_end_selections = selections
            elif selection_matches:
                # Case 2: only specific selections are updated
                # -> here we assume that only 1 selection is updated at a time
                assert len(selection_matches) == 4
                sel_idx = int(selection_matches[0].split("[")[1].split("]")[0])
                prefix = f"selections[{sel_idx}]."
                assert all(
                    sel_match.startswith(prefix) for sel_match in selection_matches
                ), "Selections are not properly formatted"
                ranges = self._get_selection_range(relayout_data, prefix)
                self._front_end_selections[sel_idx].x_range = ranges["x"]
                self._front_end_selections[sel_idx].y_range = ranges["y"]

            # TODO: might require some processing (refinement) of the selection
            # Update the backend data based on the selection
            selections = self._get_selections()
            filter_exprs: List[pl.Expr] = []
            assert None not in selections, "Selections are not properly formatted"
            if selections:
                self._print("selections", selections)
                for trace in self.data:
                    uuid = trace["uid"]
                    tr_axes = self._get_trace_axes(trace)
                    if uuid in self._scalable_traces and tr_axes in selections:
                        # Store the filter expressions
                        filter_exprs += self._scalable_traces[uuid].filter_selection(
                            selections[tr_axes]
                        )

                # Also identify traces that need to be updated due to filtering
                for trace in self.data:
                    uuid = trace["uid"]
                    tr_axes = self._get_trace_axes(trace)
                    # Traces that are not in the current selection but are scalable
                    # need to be updated as they are filtered by the selection
                    if (
                        uuid in self._scalable_traces
                        and tr_axes is not None
                        and tr_axes not in selections
                    ):
                        filtered_traces.add(uuid)

            # ----------------------- CONSTRUCT UPDATE DATA -----------------------
            update_data_list = [relayout_data]

            self._print("update range", update_range)
            t_start_agg_loop = time.perf_counter()
            agg_specs: List[AggregationSpec] = []
            for trace_idx, trace in enumerate(self.data):
                uuid = trace["uid"]
                tr_axes = self._get_trace_axes(trace)
                # TODO -> might need to be refactored
                if tr_axes is None and "map" in trace.__class__.__name__.lower():
                    if trace["subplot"] in update_range:
                        tr_axes = (trace["subplot"],)

                tr_axes = tuple() if tr_axes is None else tr_axes

                tr_update_axes = [tr_ax for tr_ax in tr_axes if tr_ax in update_range]

                if uuid in self._scalable_traces:
                    # Determine if we need to update due to zoom/pan or selection
                    # TODO: ideally front-end callbacks are not sent when no zoom_update is allowed
                    needs_update_due_to_zoom = (
                        len(tr_update_axes) > 0
                        and self._scalable_traces[uuid]._update_on_zoom
                    )
                    needs_update_due_to_filter = uuid in filtered_traces

                    if (
                        force_update
                        or needs_update_due_to_zoom
                        or needs_update_due_to_filter
                    ):
                        # For zoom/pan events, collect the axis range updates
                        update_range_trace = {}
                        if needs_update_due_to_zoom:
                            assert len(tr_update_axes) > 0
                            if "map" in trace.type.lower():
                                k = "map" if trace.subplot is None else trace.subplot
                                update_range_trace: dict = update_range[k]
                                print("update range trace", update_range_trace)
                            else:
                                update_range_trace = {
                                    # axis[0] is used in ScalableTrace to determine the axis
                                    # -> e.g. "x" and/or "y" (xy subplot)
                                    axis[0]: update_range[axis]
                                    for axis in tr_update_axes
                                }

                        # Fetch the updated data from the ScalableTrace
                        t_start = time.perf_counter()
                        # TODO: calculation of length could be done once instead of independently for each trace
                        agg_specs += [
                            self._scalable_traces[uuid].get_aggregation_spec(
                                update_range=update_range_trace,
                            )
                        ]
                        t_end = time.perf_counter()
                        self._print(
                            f"[{trace_idx:2d}] {trace.type:10s} - get agg_spec time:",
                            t_end - t_start,
                        )
            t_end_agg_loop = time.perf_counter()
            self._print(f"Total get agg_spec time: {t_end_agg_loop - t_start_agg_loop}")

            if len(agg_specs) == 0:  # No traces need to be updated
                return update_data_list

            # ----------------------- AGGREGATE DATA -----------------------
            t_start = time.perf_counter()
            if self._backend_lf is None:
                # Each trace contains data (pl.Series)
                # => which are lazy aggregated using a LazyFrame
                assert all(agg_spec.is_lf() for agg_spec in agg_specs)
                assert len(filter_exprs) == 0, "Filtering is not supported without LF"
                df_agg = pl.concat(
                    pl.collect_all([agg_spec.lf for agg_spec in agg_specs]),
                    how="horizontal",
                )
            else:
                df_agg = self._backend_lf.aggregate(filter_exprs, agg_specs)
            t_end = time.perf_counter()
            self._print(f"LFQueryBuilder.aggregate time: {t_end - t_start}")

            # ----------------------- PARSE AGGREGATED DATA -----------------------
            t_start = time.perf_counter()
            for trace_idx, trace in enumerate(self.data):
                uuid = trace["uid"]
                if uuid in self._scalable_traces and uuid in df_agg.columns:
                    update_data = self._scalable_traces[uuid]._to_update(
                        df_agg, trace_idx=trace_idx
                    )
                    update_data["index"] = trace_idx
                    update_data_list.append(update_data)
            t_end = time.perf_counter()
            self._print(f"Total update time: {t_end - t_start}")

            return update_data_list

        return None

    def _layout_axes_to_trace_axes_mapping(self) -> Dict[str, List[str]]:
        """Construct a dict which maps the layout axis keys to the trace axis keys.

        Returns
        -------
        Dict[str, List[str]]
            A dict with the layout axis values as keys and the trace its corresponding
            axis anchor value - for both the xaxes and yaxes.

        """
        # edge case: an empty `go.Figure()` does not yet contain axes keys
        if self._grid_ref is None:
            return {"xaxis": ["x"], "yaxis": ["y"]}

        mapping_dict = {}
        for sub_plot in itertools.chain.from_iterable(self._grid_ref):  # flatten
            sub_plot = [] if sub_plot is None else sub_plot
            for axes in sub_plot:  # NOTE: you can have multiple axes in a subplot
                if axes.subplot_type != "xy":  # TODO: do we want support other types?
                    continue
                # TODO: tight coupling with the supported axes
                layout_xaxes = axes.layout_keys[0]
                trace_xaxes = axes.trace_kwargs["xaxis"]
                layout_yaxes = axes.layout_keys[1]
                trace_yaxes = axes.trace_kwargs["yaxis"]

                # append the trace xaxis to the layout xaxis key its value list
                mapping_dict.setdefault(layout_xaxes, []).append(trace_xaxes)
                # append the trace yaxis to the layout yaxis key its value list
                mapping_dict.setdefault(layout_yaxes, []).append(trace_yaxes)
        return mapping_dict

    @staticmethod
    def _re_matches(regex: re.Pattern, strings: Iterable[str]) -> List[str]:
        """Returns all the items in ``strings`` which regex.match(es) ``regex``."""
        matches = []
        for item in strings:
            m = regex.match(item)
            if m is not None:
                matches.append(m.string)
        return sorted(matches)
