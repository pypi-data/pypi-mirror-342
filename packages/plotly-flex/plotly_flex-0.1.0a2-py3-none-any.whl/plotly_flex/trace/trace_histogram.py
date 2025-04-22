import polars as pl
import plotly.graph_objects as go

from .scalable_trace_interface import AbstractScalableTrace
from ..LF import LFQueryBuilder

from typing import List, Optional, Dict, Tuple


class ScalableHistogram(AbstractScalableTrace, go.Bar):
    """Scalable histogram trace."""

    _HISTNORM_OPTIONS = [
        "count",
        "percent",
        "probability",
        "density",
        "probability density",
    ]

    def __init__(
        self, bins: int | List[float] = 20, histnorm: Optional[str] = None, **kwargs
    ):
        """Create a scalable histogram trace.

        Parameters
        ----------
        bins : int | List[float]
            Number of bins or bin edges.
        histnorm : Optional[str]
            Normalization mode for the histogram trace. One of "count", "percent",
            "probability", "density", "probability density". Default is "count".
        **kwargs
            go.Bar keyword arguments - must at least provide x or y.

        """
        self._bins = bins
        histnorm = "count" if histnorm is None else histnorm
        assert histnorm in ScalableHistogram._HISTNORM_OPTIONS
        self._histnorm = histnorm
        super().__init__(**kwargs)

    @property
    def get_backend_data_keys(self):
        return ["x", "y"]

    @property
    def get_prop_key(self) -> str:
        # Get the key that is used for the histogram plot
        if "x" in self._backend_data:
            assert "y" not in self._backend_data
            return "x"
        elif "y" in self._backend_data:
            return "y"
        raise ValueError("No data found for the histogram")

    def get_filter_backend_data_keys(self) -> List[str]:
        return [self.get_prop_key]

    def _validate_figure_data_trace(self, data: Optional[LFQueryBuilder]):
        # validate the trace kwargs using the stored keys and data (from the figure)
        if not ("x" in self._backend_data or "y" in self._backend_data):
            raise ValueError("Either x or y should be provided")
        if "x" in self._backend_data and "y" in self._backend_data:
            raise ValueError("Not both x and y should be provided")

    def _get_agg_expr(self, update_range: Dict[str, Tuple[float, float]]) -> pl.Expr:
        prop_key: str = self.get_prop_key  # either x or y
        filter_range = update_range.get(prop_key)

        data_col: str = self.resolve_data_column(prop_key)
        expr = pl.col(data_col)

        # 1. filter the data
        if filter_range:
            expr = expr.filter(
                *super()._get_filter_expr(
                    data_col, self._dtypes[prop_key], *filter_range
                )
            )

        # 2. aggregate the data
        expr = expr.hist(
            bin_count=self._bins, include_category=True, include_breakpoint=True
        )

        # 3. store the aggregated data in a horizontal array of structs
        expr = pl.struct(expr).alias(self.uid).reshape((1, -1))

        return expr

    def _to_update(self, df_agg: pl.DataFrame, **kwargs) -> Dict[str, list]:
        prop_key = self.get_prop_key  # either x or y

        df_agg = df_agg[self.uid].item().struct.unnest()
        df_hist = (
            df_agg[self.resolve_data_column(prop_key)]
            .struct.unnest()
            .with_columns(pl.col("breakpoint") - pl.col("breakpoint").diff().mean() / 2)
            .rename({"breakpoint": "center"})
        )

        # -- normalize the counts (if needed)
        bin_width = df_hist["center"].diff().drop_nulls().mean()
        total = df_hist["count"].sum()
        if self._histnorm == "percent":
            df_hist = df_hist.with_columns(pl.col("count") / total * 100)
        elif self._histnorm == "probability":
            df_hist = df_hist.with_columns(pl.col("count") / total)
        elif self._histnorm == "density":
            df_hist = df_hist.with_columns(pl.col("count") / (bin_width))
        elif self._histnorm == "probability density":
            df_hist = df_hist.with_columns(pl.col("count") / (total * bin_width))

        # 3. store and return the data with the correct props for the front-end update
        data = {}
        if prop_key == "x":
            data["x"] = df_hist["center"].to_numpy()
            data["y"] = df_hist["count"].to_numpy()
        else:
            assert prop_key == "y"
            data["x"] = df_hist["count"].to_numpy()
            data["y"] = df_hist["center"].to_numpy()
            data["orientation"] = "h"
        data["hoverinfo"] = "y+text"
        data["hovertext"] = df_hist["category"].to_numpy()

        return data
