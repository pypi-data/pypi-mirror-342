import polars as pl
import plotly.graph_objects as go

from .scalable_trace_interface import AbstractScalableTrace
from .utils import range_to_idx
from ..LF import LFQueryBuilder

from typing import Optional, List, Dict, Tuple


# TODO: in an ideal world this will automatically wrap the go.Scatter class (using a register decorator)
# TODO: aggregation should be loosely coupled as well
class ScalableScatter1DMixin:
    """Mixin class for scalable sequential/time series scatter traces."""

    def __init__(self, nb_points: int = 1000, **kwargs):
        self._nb_points = nb_points
        super().__init__(**kwargs)

    @property
    def get_backend_data_keys(self):
        return ["x", "y"]

    def _validate_figure_data_trace(self, data: Optional[LFQueryBuilder]):
        # validate the trace kwargs using the stored keys and data (from the figure)
        if "y" not in self._backend_data:
            raise ValueError("y should be provided")
        if data is not None and self._backend_contains_string():
            # Figure data is provided and backend data contains strings (col names)
            x_col: str = self._backend_data.get("x", data.row_index_col)
            assert isinstance(x_col, str), "x should be a string"
            data.check_sorted(x_col)  # check if the column is sorted (and set_sorted)
            if "x" not in self._backend_data:
                self._backend_data["x"] = x_col
                # NOTE: no need to log dtype as this is done in _validate_figure_data
                # after calling this function
        elif "x" in self._backend_data:
            # x is provided in the backend data => must be a Series
            s: pl.Series = self._backend_data["x"]
            assert isinstance(s, pl.Series), "x should be a Series"
            assert s.is_sorted(), "x should be sorted"
            self._backend_data["x"] = self._backend_data["x"].set_sorted()
        else:
            # backend data contains series, but x is not provided => .with_row_index
            # dtype is logged here as no "x" property is set and thus will not be
            # logged in _validate_figure_data
            self._dtypes["x"] = pl.get_index_type()

    def get_filter_backend_data_keys(self) -> List[str]:
        return ["x", "y"]

    def _to_ldf(self) -> pl.LazyFrame:
        if "x" in self._backend_data:
            return super()._to_ldf()
        # x is not provided in the backend data => use .with_row_index
        return super()._to_ldf().with_row_index(name="x")  # TODO: more efficient?

    def _get_agg_expr(self, update_range: Dict[str, Tuple[float, float]]) -> pl.Expr:
        # => TODO: explore using .filter instead of search_sorted (on true lazy frames)
        filter_range = update_range.get("x")

        x_col: str = self.resolve_data_column("x")
        expr = pl.col([x_col, self.resolve_data_column("y")])

        # 1. filter the data (if needed) & get the length of the (filtered) data
        length = None
        if filter_range:
            # Basic O(n) solution
            # data = data.filter(
            #     *super()._get_filter_expr("x", *filter_range)
            # )
            # -> Can be 5x faster by using searchsorted + slicing => O(1/5n)
            # -> Which can be made even much faster when using the same idx type for the
            #    search values in searchsorted => log(n) complexity
            x_dtype: pl.Dtype = self._dtypes["x"]
            if x_dtype.is_integer():
                filter_range = range_to_idx(*filter_range)
            search_elements = pl.Series(filter_range).cast(x_dtype, strict=True)
            slice_idx = pl.col(x_col).search_sorted(search_elements)
            length = slice_idx.diff(null_behavior="drop").get(0)
            expr = expr.slice(slice_idx.get(0), length=length)
        else:
            length = pl.len()
        assert length is not None

        # 2. aggregate the data
        nb_points = pl.min_horizontal(
            [pl.lit(self._nb_points, dtype=pl.get_index_type()), length]
        )
        selection_idx = pl.int_range(nb_points).cast(dtype=pl.Float32)
        expr = expr.gather(
            (selection_idx * (length / nb_points)).cast(pl.get_index_type())
        )

        # 3. store the aggregated data in a horizontal array of structs
        expr = pl.struct(expr).alias(self.uid).reshape((1, -1))

        return expr

    def _to_update(self, df_agg: pl.DataFrame, **kwargs) -> Dict[str, list]:
        df_agg = df_agg[self.uid].item().struct.unnest()
        return {
            "x": df_agg.to_series(0).to_numpy(),
            "y": df_agg.to_series(1).to_numpy(),
        }


class ScalableScatter1D(ScalableScatter1DMixin, AbstractScalableTrace, go.Scatter):
    """Scalable sequential / time series scatter trace."""


class ScalableScattergl1D(ScalableScatter1DMixin, AbstractScalableTrace, go.Scattergl):
    """Scalable sequential / time series scattergl trace."""


class ScalableScatter2DMixin:
    """Mixin class for scalable scatter traces."""

    def __init__(self, nb_points: int = 1000, **kwargs):
        self._nb_points = nb_points
        super().__init__(**kwargs)

    @property
    def get_backend_data_keys(self):
        return ["x", "y"]

    def _validate_figure_data_trace(self, data: Optional[LFQueryBuilder]):
        # validate the trace kwargs using the stored keys and data (from the figure)
        if "y" not in self._backend_data:
            raise ValueError("y should be provided")
        if "x" not in self._backend_data:
            raise ValueError("x should be provided")

    def get_filter_backend_data_keys(self) -> List[str]:
        return ["x", "y"]

    def _get_agg_expr(
        self,
        update_range: Dict[str, Tuple[float, float]],
    ) -> pl.Expr:
        x_filter_range = update_range.get("x")
        y_filter_range = update_range.get("y")

        x_col: str = self.resolve_data_column("x")
        y_col: str = self.resolve_data_column("y")
        expr = pl.col([x_col, y_col])

        # 1. filter the data (if needed) & get the length of the (filtered) data
        filters = []
        if x_filter_range:
            # Add a small delta for nicer display
            delta = 0.05 * (x_filter_range[1] - x_filter_range[0])
            x_filter_range = [x_filter_range[0] - delta, x_filter_range[1] + delta]
            filters += super()._get_filter_expr(
                x_col, self._dtypes["x"], *x_filter_range
            )
        if y_filter_range:
            # Add a small delta for nicer display
            delta = 0.05 * (y_filter_range[1] - y_filter_range[0])
            y_filter_range = [y_filter_range[0] - delta, y_filter_range[1] + delta]
            filters += super()._get_filter_expr(
                y_col, self._dtypes["y"], *y_filter_range
            )
        if filters:
            expr = expr.filter(*filters)  # Expr.filter must have one or more arguments
        length = expr.len()

        # 2. aggregate the data
        nb_points = pl.min_horizontal(
            [pl.lit(self._nb_points, dtype=pl.get_index_type()), length]
        )
        selection_idx = pl.int_range(nb_points).cast(dtype=pl.Float32)
        expr = expr.gather(
            (selection_idx * (length / nb_points)).cast(pl.get_index_type())
        )

        # 3. store the aggregated data in a horizontal array of structs
        expr = pl.struct(expr).alias(self.uid).reshape((1, -1))

        return expr

    def _to_update(self, df_agg: pl.DataFrame, **kwargs) -> Dict[str, list]:
        df_agg = df_agg[self.uid].item().struct.unnest()
        return {
            "x": df_agg.to_series(0).to_numpy(),
            "y": df_agg.to_series(1).to_numpy(),
        }


class ScalableScatter2D(ScalableScatter2DMixin, AbstractScalableTrace, go.Scatter):
    """Scalable x-y scatter trace."""


class ScalableScattergl2D(ScalableScatter2DMixin, AbstractScalableTrace, go.Scattergl):
    """Scalable x-y scattergl trace."""


class ScalableScatterMap(AbstractScalableTrace, go.Scattermap):
    """Scalable x-y scatter map trace."""

    def __init__(self, nb_points: int = 1000, **kwargs):
        self._nb_points = nb_points
        super().__init__(**kwargs)

    @property
    def get_backend_data_keys(self):
        return ["lat", "lon"]

    def get_filter_backend_data_keys(self) -> List[str]:
        return ["lat", "lon"]

    def _validate_figure_data_trace(self, data: Optional[LFQueryBuilder]):
        # validate the trace kwargs using the stored keys and data (from the figure)
        if "lat" not in self._backend_data:
            raise ValueError("lat should be provided")
        if "lon" not in self._backend_data:
            raise ValueError("lon should be provided")

    def _get_agg_expr(
        self,
        update_range: Dict[str, Tuple[float, float]],
    ) -> pl.Expr:
        def _get_lat_long_range(update) -> Tuple[List | None, List | None]:
            # coordinates = update.get('map._derived', {}).get('coordinates', {})
            coordinates = update.get("coordinates", {})
            print("coordinates", coordinates)
            if not coordinates:
                return None, None
            lon = [c[0] for c in coordinates]
            lat = [c[1] for c in coordinates]
            min_lat, max_lat = min(lat), max(lat)
            min_lon, max_lon = min(lon), max(lon)

            # Add a small delta for nicer display
            dln = 0.05 * (max_lon - min_lon)
            dlt = 0.05 * (max_lat - min_lat)
            return [min_lat - dlt, max_lat + dlt], [min_lon - dln, max_lon + dln]
            # return [min(lat), max(lat)], [min(lon), max(lon)]

        lat_filter_range, lon_filter_range = _get_lat_long_range(update_range)

        lat_col: str = self.resolve_data_column("lat")
        lon_col: str = self.resolve_data_column("lon")
        expr = pl.col([lat_col, lon_col])

        # 1. filter the data (if needed) & get the length of the (filtered) data
        filters = []
        if lat_filter_range:
            filters += self._get_filter_expr(
                lat_col, self._dtypes["lat"], *lat_filter_range
            )
        if lon_filter_range:
            filters += self._get_filter_expr(
                lon_col, self._dtypes["lon"], *lon_filter_range
            )
        if filters:
            expr = expr.filter(*filters)
        length = expr.len()

        # 2. aggregate the data
        nb_points = pl.min_horizontal(
            [pl.lit(self._nb_points, dtype=pl.get_index_type()), length]
        )
        selection_idx = pl.int_range(nb_points).cast(dtype=pl.Float32)
        expr = expr.gather(
            (selection_idx * (length / nb_points)).cast(pl.get_index_type())
        )

        # 3. store the aggregated data in a horizontal array of structs
        expr = pl.struct(expr).alias(self.uid).reshape((1, -1))

        return expr

    def _to_update(self, df_agg: pl.DataFrame, **kwargs) -> Dict[str, list]:
        df_agg = df_agg[self.uid].item().struct.unnest()
        return {
            "lat": df_agg.to_series(0).to_numpy(),
            "lon": df_agg.to_series(1).to_numpy(),
        }
