import polars as pl


from plotly.basedatatypes import BaseTraceType
from plotly._subplots import _subplot_type_for_trace_type
from abc import ABC, abstractmethod

from .utils import range_to_idx
from ..LF import LFQueryBuilder, AggregationSpec

from typing import Optional, List, Dict, Tuple


class AbstractScalableTrace(BaseTraceType, ABC):
    """Abstract interface for data aggregation functionality for plotly traces."""

    def __init__(
        self, transform: Optional[pl.Expr] = None, update_on_zoom: bool = True, **kwargs
    ):
        self._transform = transform  # TODO: properly implement this (pl.pipe)
        # Ideally we have some front-end js function that does not fire a callback on zoom
        self._update_on_zoom = update_on_zoom  # TODO: properly implement this
        self._dtypes: Dict[str, pl.DataType] = {}  # log dtypes of the backend_data
        # Parse the keywords arguments and store in the backend_data
        self._parse_kwargs(kwargs)
        # Validate the backend kwargs
        self._validate_backend_kwargs()
        # Ensure no duplicate keys in kwargs and backend_data
        assert all(key not in kwargs for key in self.get_backend_data_keys), (
            "Duplicate key(s) in ScalableTrace kwargs and backend_data"
        )
        super().__init__(**kwargs)

        # Set the trace type
        self._subplot_type = _subplot_type_for_trace_type(self.type)  # TODO: not used
        # Update the plotly name as the type cannot be changed
        self._plotly_name = "[SCALABLE] " + self.type

    @property
    @abstractmethod
    def get_backend_data_keys(self):
        """Return the keys of the backend_data (these kwargs will be stored)."""
        raise NotImplementedError

    def resolve_data_column(self, key: str) -> str:
        """Convert a trace property key to its corresponding data column name.

        When working with data in LazyFrames, we need to map between trace properties
        and actual column names (which is stored as value in backend_data).
        When working with data in Series, we use the trace property key as the column
        name.

        Parameters
        ----------
        key : str
            The trace property key from backend_data.

        Returns
        -------
        str
            The actual column name in the data:
            - Returns the stored string value if backend_data contains a string
            - Returns the original key if the backend_data contains a series

        Raises
        ------
        AssertionError
            If the key is not found in backend_data.
        """
        if key in self._backend_data and isinstance(self._backend_data[key], str):
            return self._backend_data[key]
        return key

    def _backend_contains_string(self):
        return any(isinstance(b_value, str) for b_value in self._backend_data.values())

    def _backend_all_string(self):
        return all(isinstance(b_value, str) for b_value in self._backend_data.values())

    def _validate_backend_kwargs(self):
        """Validate the backend_data keys and values."""
        b_keys = self._backend_data.keys()
        # check all keys are in get_backend_data_keys
        assert all(key in self.get_backend_data_keys for key in b_keys), (
            "All backend_data keys should be in get_backend_data_keys"
        )
        # check all keys are not None
        assert all(self._backend_data[key] is not None for key in b_keys), (
            "All backend_data keys should not be None"
        )
        # check either all keys are strings or all keys are array/series like
        if self._backend_contains_string():
            # If any key is of type string, all keys must be of type string
            assert self._backend_all_string(), (
                "Data keys must either all be strings or all be array/series like"
            )
        else:
            # Otherwise, all keys must be array/series like (i.e. not strings)
            assert not any(
                isinstance(self._backend_data[key], str) for key in b_keys
            ), "Data keys must either all be strings or all be array/series like"
            # and all keys must have the same length
            assert len(set(self._backend_data[key].len() for key in b_keys)) == 1, (
                "Data keys must have the same length"
            )

    # This can be extended by the trace specific class to further validate kwargs & data
    def _validate_figure_data(self, data: Optional[LFQueryBuilder]):
        """Validate the backend_data keys and values with the figure data.

        Parameters
        ----------
        data : Optional[LFQueryBuilder]
            The figure data to validate.
        """
        # ----- 1. VALIDATE THE DATA
        assert self.uid is not None, "Trace uid should not be None"
        # Case 1: No figure data provided
        if data is None:
            # When no data is provided, backend data must contain actual series/arrays
            assert not self._backend_contains_string(), (
                "Without figure data, trace props must contain actual series/arrays"
            )
        # Case 2: Figure data is provided and backend contains strings (col names)
        elif self._backend_contains_string():
            # All keys must be strings (column names) if any are strings
            assert self._backend_all_string(), (
                "Mixed trace props data types not allowed: either all strings or series"
            )
            if self._transform is None:  # Case no transform
                # Without transform, all column references must exist in data
                for column_name in self._backend_data.values():
                    assert column_name in data.schema.names(), (
                        f"Column '{column_name}' not found in figure data"
                    )
            else:  # Case with transform
                # With transform, at least filter columns must exist in data
                for key in self.get_filter_backend_data_keys():
                    column_name = self._backend_data[key]
                    assert column_name in data.schema.names(), (
                        f"Filter column '{column_name}' not found in figure data"
                    )
        # Case 3: Figure data is provided but backend contains series/arrays
        # No additional validation needed - this is a valid configuration

        # Additional trace specific validation of the figure data
        self._validate_figure_data_trace(data)

        # ------ 2. STORE THE DATA TYPES
        if data is not None and self._backend_contains_string():
            # Figure data is provided and backend data contains strings (col names)
            schema = data.schema
            for prop_key, col_name in self._backend_data.items():
                if col_name in schema:
                    self._dtypes[prop_key] = schema[col_name]
                else:
                    assert self._transform is not None
        else:
            # Figure data is not provided or backend data contains series
            for prop_key in self._backend_data:
                self._dtypes[prop_key] = self._backend_data[prop_key].dtype

    @abstractmethod
    def _validate_figure_data_trace(self, data: Optional[LFQueryBuilder]):
        """Validate the trace specific figure data.

        Parameters
        ----------
        data : Optional[LFQueryBuilder]
            The figure data to validate.
        """
        raise NotImplementedError

    def _parse_kwargs(self, kwargs: dict):
        """Parse the kwargs of the trace and store it in the backend_data.

        The get_backend_data_keys are stored in the backend_data (if not None).
        These keys can be either strings or array/series like. When strings, the data is
        a DataFrame or LazyFrame and is stored in the AbstractScalableTrace.
        """
        # keys = trace properties; values = data (str or pl.Series)
        self._backend_data: Dict[str, str | pl.Series] = {}

        kwargs.pop("type", None)  # the type is logged in the superclass
        # Store the not None kwargs in the backend_data
        for key in set(kwargs.keys()).intersection(self.get_backend_data_keys):
            if kwargs[key] is not None:
                # TODO: do we want to support pl.Expr?
                s: str | pl.Series = kwargs.pop(key)
                if not isinstance(s, (str, pl.Series)):
                    # s should be in-memory array-like
                    s = pl.Series(s)
                    if s.dtype.is_nested():
                        if s.dtype.shape[1] == 1:
                            s = s.explode()
                        else:
                            raise ValueError("s should be a 1D array")
                self._backend_data[key] = s  # s should be a str or pl.Series

    @abstractmethod
    def get_filter_backend_data_keys(self) -> List[str]:
        """Return the keys of the backend_data that should be filtered on."""
        raise NotImplementedError

    @staticmethod
    def _get_filter_expr(
        col_name: str, col_dtype: pl.DataType, start: int | float, end: int | float
    ) -> List[pl.Expr]:
        """Get the filter expressions for the col based on the start and end values.

        Remark that the col_dtype is used to cast the start and end values to the
        datatype of the column (which results in faster filtering).
        """
        assert isinstance(col_name, str), "col_name should be a string"
        assert start <= end, "start should be less than or equal to end"
        if col_dtype.is_integer():
            start, end = range_to_idx(start, end)
        # TODO: >= or > / <= or < ?
        return [
            pl.col(col_name) >= pl.lit(start, dtype=col_dtype),
            pl.col(col_name) <= pl.lit(end, dtype=col_dtype),
        ]

    def filter_selection(
        self,
        selection_range: Dict[str, tuple[float, float]],
    ) -> List[pl.Expr]:
        """Filter the backend data based on the selection range.

        Parameters
        ----------
        selection_range : Dict[str, tuple[float, float]]
            The selection range for each key. The key should be in the backend_data.

        Returns
        -------
        List[pl.Expr]
            The filter expressions to apply to the data.
        """
        filters = []
        for key in self.get_filter_backend_data_keys():
            assert key in self._backend_data, f"Key {key} not in backend_data"
            filters += self._get_filter_expr(
                self._backend_data[key], self._dtypes[key], *selection_range[key]
            )
        return filters

    def _to_ldf(self) -> pl.LazyFrame:
        """Convert the backend_data to a LazyFrame.

        This should only be called when the backend_data contains series.

        Returns
        -------
        pl.LazyFrame
            The LazyFrame representation of the backend_data.
        """
        return pl.DataFrame(self._backend_data).lazy()

    @abstractmethod
    def _get_agg_expr(
        self,
        update_range: Dict[str, Tuple[float, float]],
    ) -> pl.Expr:
        """Get the aggregation expression based on the figure data and the update range.

        This aggregation expression is used to aggregate the data in the LFQueryBuilder
        in a selection context. The output of this expression should be a single array
        of structs (result of horizontal reshape after converting to a struct). This
        is necessary to allow for execution of different aggregation expressions
        simultaneously (that each can output different number of elements), as each
        array of structs comprises a single column and row.

        Parameters
        ----------
        update_range : Dict[str, Tuple[float, float]]
            The range to update the data on, e.g. {"x": (0.5, 10.5)}. The keys of this
            dict should match the keys of the trace backend_data.
            If no update is needed, an empty dict should be passed.

        Returns
        -------
        pl.Expr
            The aggregation expression used for aggregation, which outputs a single
            array of structs; e.g. array[struct[2], 100] -> 1 array of 100 structs.
            Note that this comprises only a single column and row.
        """
        raise NotImplementedError

    def get_aggregation_spec(
        self, update_range: Dict[str, Tuple[float, float]]
    ) -> AggregationSpec:
        """Get the aggregation spec for the trace based on the update range.

        This function returns an AggregationSpec that defines how the data should be
        aggregated.

        Parameters
        ----------
        update_range : Dict[str, Tuple[float, float]]
            The range to update the data on, e.g. {"x": (0.5, 10.5)}. The keys should
            match the backend_data keys. An empty dict means no zoom / pan action was
            performed.

        Returns
        -------
        AggregationSpec
            The aggregation specification containing either an expression with optional
            transform (for string-based backend) or a LazyFrame (for series-based
            backend).
        """
        if self._backend_contains_string():
            # If backend data contains string => return the aggregation expression
            assert self._backend_all_string(), "Backend data should all be strings"
            return AggregationSpec(
                expr=self._get_agg_expr(update_range), transform=self._transform
            )
        else:
            # If backend data contains series => get them as LazyFrame and aggregate
            return AggregationSpec(
                lf=self._to_ldf().select(self._get_agg_expr(update_range))
            )

    @abstractmethod
    def _to_update(self, df_agg: pl.DataFrame, **kwargs) -> Dict[str, list]:
        """Parse the aggregated data to the front-end format.

        This function transforms the array of structs (output of _get_agg_expr) to the
        front-end format.

        Parameters
        ----------
        df_agg : pl.DataFrame
            The aggregated data. This contains a single column for each trace that
            requires an update - with as column name the uid of the trace.
            This dataframe contains a single row (the aggregated data), which is an
            array of structs (the data for the trace).
        kwargs : dict
            Additional keyword arguments.

        Returns
        -------
        Dict[str, list]
            The aggregated data. This dict contains the keys of the front-end props
            and the values are ndarray-like (which contain the aggregated data).
        """
        raise NotImplementedError
