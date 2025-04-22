from .scalable_figure_interface import AbstractScalableFigure

import re
import dash
import warnings
import plotly.graph_objects as go
from plotly.basedatatypes import BaseFigure
from pathlib import Path

from .utils import is_figure, is_scalable_figure

from typing import Union, List


class ScalableFigure(AbstractScalableFigure, go.Figure):
    """Data aggregation functionality for ``go.Figure``."""

    def __init__(
        self,
        figure: BaseFigure | dict = None,
        show_dash_kwargs: dict | None = None,
        **kwargs,
    ):
        if is_figure(figure) and not is_scalable_figure(figure):
            # a go.Figure
            # => base case: the figure does not need to be adjusted
            f = figure
        else:
            # Create a new figure object and make sure that the trace uid will not get
            # adjusted when they are added.
            f = go.Figure()  # TODO: replace with code below if we support registering
            # f = self._get_figure_class(go.Figure)()
            f._data_validator.set_uid = False

            if isinstance(figure, BaseFigure):
                # A base figure object, can be;
                # - a go.FigureWidget
                # - a plotly-resampler figure: subclass of AbstractFigureAggregator
                # => we first copy the layout, grid_str and grid ref
                f.layout = figure.layout
                f._grid_str = figure._grid_str
                f._grid_ref = figure._grid_ref
                f.add_traces(figure.data)
            elif isinstance(figure, dict) and (
                "data" in figure or "layout" in figure  # or "frames" in figure  # TODO
            ):
                # A figure as a dict, can be;
                # - a plotly figure as a dict (after calling `fig.to_dict()`)
                # - a pickled (plotly-scalable) figure (after loading a pickled figure)
                # => we first copy the layout, grid_str and grid ref
                f.layout = figure.get("layout")
                f._grid_str = figure.get("_grid_str")
                f._grid_ref = figure.get("_grid_ref")
                f.add_traces(figure.get("data"))
                # TODO: support this
                # `pr_props` is not None when loading a pickled plotly-resampler figure
                f._pr_props = figure.get("pr_props")
                # `f._pr_props`` is an attribute to store properties of a
                # plotly-resampler figure. This attribute is only used to pass
                # information to the super() constructor. Once the super constructor is
                # called, the attribute is removed.

                # f.add_frames(figure.get("frames")) TODO
            elif isinstance(figure, (dict, list)):
                # A single trace dict or a list of traces
                f.add_traces(figure)

        self._show_dash_kwargs = show_dash_kwargs or {}

        super().__init__(f, **kwargs)

        if isinstance(figure, AbstractScalableFigure):
            # TODO: Copy the scalable traces
            raise NotImplementedError("Not yet implemented")

        # The ScalableFigure needs a dash app
        self._app: dash.Dash | None = None
        self._port: int | None = None
        self._host: str | None = None

    def construct_update_data_patch(
        self, relayout_data: dict
    ) -> Union[dash.Patch, dash._callback.NoUpdate]:
        """Construct the Patch of the to-be-updated front-end data, based on the layout
        change.

        Attention
        ---------
        This method is tightly coupled with Dash app callbacks. It takes the front-end
        figure its ``relayoutData`` as input and returns the ``dash.Patch`` which needs
        to be sent to the ``figure`` property for the corresponding ``dcc.Graph``.

        Parameters
        ----------
        relayout_data: dict
            A dict containing the ``relayoutData`` (i.e., the changed layout data) of
            the corresponding front-end graph.

        Returns
        -------
        dash.Patch:
            The Patch object containing the figure updates which needs to be sent to
            the front-end.

        """
        # Manually trigger update when first view is loaded
        # TODO: get Jonas his input on this
        force_update = False
        if len(relayout_data) == 1 and relayout_data.get("autosize") is True:
            self._front_end_selections = []  # TODO: must be reset?
            force_update = True

        update_data = self._construct_update_data(relayout_data, force_update)
        if not isinstance(update_data, list) or len(update_data) <= 1:
            return dash.no_update

        patched_figure = dash.Patch()  # create patch
        for trace in update_data[1:]:  # skip first item as it contains the relayout
            trace_index = trace.pop("index")  # the index of the corresponding trace
            # All the other items are the trace properties which needs to be updated
            for k, v in trace.items():
                # NOTE: we need to use the `patched_figure` as a dict, and not
                # `patched_figure.data` as the latter will replace **all** the
                # data for the corresponding trace, and we just want to update the
                # specific trace its properties.
                patched_figure["data"][trace_index][k] = v
        return patched_figure

    def show_dash(
        self,
        mode=None,
        config: dict | None = None,
        init_dash_kwargs: dict | None = None,
        graph_properties: dict | None = None,
        **kwargs,
    ):
        available_modes = list(dash._jupyter.JupyterDisplayMode.__args__)
        assert mode is None or mode in available_modes, (
            f"mode must be one of {available_modes}"
        )
        graph_properties = {} if graph_properties is None else graph_properties
        assert "config" not in graph_properties  # There is a param for config
        if self["layout"]["autosize"] is True and self["layout"]["height"] is None:
            graph_properties.setdefault("style", {}).update({"height": "100%"})

        # 0. Check if the traces need to be updated when there is a xrange set
        # This will be the case when the users has set a xrange (via the `update_layout`
        # or `update_xaxes` methods`)
        relayout_dict = {}
        for xaxis_str in self._xaxis_list:
            x_range = self.layout[xaxis_str].range
            if x_range:  # when not None
                relayout_dict[f"{xaxis_str}.range[0]"] = x_range[0]
                relayout_dict[f"{xaxis_str}.range[1]"] = x_range[1]
        if relayout_dict:  # when not empty
            self._print("Relayout dict:", relayout_dict)
            update_data = self._construct_update_data(relayout_dict)

            if not self._is_no_update(update_data):  # when there is an update
                with self.batch_update():
                    # First update the layout (first item of update_data)
                    self.layout.update(self._parse_relayout(update_data[0]))

                    # Then update the data
                    for updated_trace in update_data[1:]:
                        trace_idx = updated_trace.pop("index")
                        self.data[trace_idx].update(updated_trace)

        # 1. Construct the Dash app layout
        ASSETS_FOLDER = Path(__file__).parent.joinpath("assets").absolute().__str__()
        EXTERNAL_SCRIPTS = ["https://cdn.jsdelivr.net/npm/lodash/lodash.min.js"]

        init_dash_kwargs = {} if init_dash_kwargs is None else init_dash_kwargs
        init_dash_kwargs["assets_folder"] = init_dash_kwargs.get(
            "assets_folder", ASSETS_FOLDER
        )
        init_dash_kwargs["external_scripts"] = (
            init_dash_kwargs.get("external_scripts", []) + EXTERNAL_SCRIPTS
        )

        # jupyter dash uses a normal Dash app as figure
        app = dash.Dash("local_app", **init_dash_kwargs)

        if "map" in self.layout._props.keys():
            print("map detected -> creating an improved reset axes button")
            config = {} if config is None else config
            config["modeBarButtonsToRemove"] = list(
                set(
                    [
                        "resetviews",
                        "resetscale",
                        *config.get("modeBarButtonsToRemove", []),
                    ]
                )
            )
            config["modeBarButtonsToAdd"] = config.get("modeBarButtonsToAdd", [])

            # add the clientside callback to add the custom modebar button and call the
            # first update so that the figure is updated when the page is loaded
            app.clientside_callback(
                dash.ClientsideFunction(
                    namespace="clientside",
                    function_name="add_reset_axes_modebar_relayout",
                ),
                dash.Output("scalable-figure", "config"),
                dash.Input("url", "href"),  # trigger when the page is loaded
                dash.State("scalable-figure", "id"),
                dash.State("scalable-figure", "config"),
            )

        # fmt: off
        div = dash.html.Div(
            children=[
                dash.dcc.Location(id="url", refresh=False),
                dash.dcc.Graph(
                    id="scalable-figure", figure=self, config=config, **graph_properties
                )
            ],
            style={
                "display": "flex", "flexFlow": "column",
                "height": "95vh", "width": "100%",
            },
        )
        # fmt: on
        app.layout = div

        self.register_update_graph_callback(app, "scalable-figure")

        # 2. Run the app
        if mode == "inline" and "jupyter_height" not in kwargs:
            # If app height is not specified -> re-use figure height for inline dash app
            #  Note: default layout height is 450 (whereas default app height is 650)
            #  See: https://plotly.com/python/reference/layout/#layout-height
            fig_height = self.layout.height if self.layout.height is not None else 450
            kwargs["jupyter_height"] = fig_height + 18

        # kwargs take precedence over the show_dash_kwargs
        kwargs = {**self._show_dash_kwargs, **kwargs}

        # Store the app information, so it can be killed
        self._app = app
        self._host = kwargs.get("host", "127.0.0.1")
        self._port = kwargs.get("port", "8050")

        # function signature is slightly different for the Dash and JupyterDash implementations
        # if self._is_persistent_inline:
        #     app.run(mode=mode, **kwargs)
        # else:
        app.run(jupyter_mode=mode, **kwargs)

    def stop_server(self, warn: bool = True):
        """Stop the running dash-app.

        Parameters
        ----------
        warn: bool
            Whether a warning message will be shown or  not, by default True.

        !!! warning

            This only works if the dash-app was started with [`show_dash`][figure_resampler.figure_resampler.FigureResampler.show_dash].
        """
        if self._app is not None:
            # servers_dict = (
            #     self._app._server_threads
            #     if self._is_persistent_inline
            #     else dash.jupyter_dash._servers
            # )
            servers_dict = dash.jupyter_dash._servers
            old_server = servers_dict.get((self._host, self._port))
            if old_server:
                old_server.shutdown()
            del servers_dict[(self._host, self._port)]
        elif warn:
            warnings.warn(
                "Could not stop the server, either the \n"
                + "\t- 'show-dash' method was not called, or \n"
                + "\t- the dash-server wasn't started with 'show_dash'"
            )

    def register_update_graph_callback(
        self,
        app: dash.Dash,
        graph_id: str,
    ):
        """Register the [`construct_update_data_patch`][figure_resampler.figure_resampler_interface.AbstractFigureAggregator.construct_update_data_patch]
        method as callback function to the passed dash-app.

        Parameters
        ----------
        app: dash.Dash
            The app in which the callback will be registered.
        graph_id:
            The id of the ``dcc.Graph``-component which withholds the to-be resampled
            Figure.

        """

        # As we use the figure again as output, we need to set: allow_duplicate=True
        @app.callback(
            dash.Output(graph_id, "figure", allow_duplicate=True),
            dash.Input(graph_id, "relayoutData"),
            prevent_initial_call=True,
        )
        def update_graph(relayout_data):
            # First filter out dragmode events  # TODO: ideally this happens client-side
            if (
                relayout_data
                and len(relayout_data) == 1
                and "dragmode" in relayout_data
            ):
                return dash.no_update
            # TODO: filter out other events?

            # Then construct the update data patch
            return self.construct_update_data_patch(relayout_data)

    def _parse_relayout(self, relayout_dict: dict) -> dict:
        """Update the relayout object so that the autorange will be set to None when
        there are xy-matches.

        Parameters
        ----------
        relayout_dict : dict
            The relayout dictionary.
        """
        # 1. Create a new dict with additional layout updates for the front-end
        extra_layout_updates = {}

        # 1.1. Set autorange to False for each layout item with a specified x-range
        xy_matches = self._re_matches(
            re.compile(r"[xy]axis\d*.range\[\d+]"), relayout_dict.keys()
        )
        for range_change_axis in xy_matches:
            axis = range_change_axis.split(".")[0]
            extra_layout_updates[f"{axis}.autorange"] = None
        return extra_layout_updates

    @staticmethod
    def _is_no_update(update_data: Union[List[dict], dash._callback.NoUpdate]) -> bool:
        return update_data is dash.no_update

    # ---------------------------

    def _ipython_display_(self):
        # To display the figure inline as a dash app
        self.show_dash(mode="inline")
