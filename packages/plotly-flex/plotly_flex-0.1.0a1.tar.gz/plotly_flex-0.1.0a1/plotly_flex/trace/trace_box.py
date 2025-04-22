import polars as pl
import plotly.graph_objects as go

from .scalable_trace_interface import AbstractScalableTrace
from ..LF import LFQueryBuilder

from typing import Optional, List, Dict, Tuple


class ScalableBox(AbstractScalableTrace, go.Box):
    """Scalable box trace."""

    def __init__(self, **kwargs):
        super().__init__(update_on_zoom=False, **kwargs)

    @property
    def get_backend_data_keys(self):
        return ["x", "y"]

    @property
    def get_prop_key(self) -> str:
        # Get the key that is used for the box plot
        if "x" in self._backend_data:
            assert "y" not in self._backend_data
            return "x"
        elif "y" in self._backend_data:
            return "y"
        raise ValueError("No data found for the box plot")

    def get_filter_backend_data_keys(self) -> List[str]:
        return [self.get_prop_key]

    def _validate_figure_data_trace(self, data: Optional[LFQueryBuilder]):
        if not ("x" in self._backend_data or "y" in self._backend_data):
            raise ValueError("Either x or y should be provided")
        if "x" in self._backend_data and "y" in self._backend_data:
            raise ValueError("Not both x and y should be provided")

    def get_name(self, trace_idx: int) -> str:
        return self.name if self.name is not None else f"trace {trace_idx}"

    def _get_agg_expr(self, update_range: Dict[str, Tuple[float, float]]) -> pl.Expr:
        prop_key: str = self.get_prop_key  # either x or y

        expr = pl.col(self.resolve_data_column(prop_key))

        # 1. filter the data
        # TODO: handle update_range properly => does not support zooming
        assert not update_range, "Box plot does not support zooming"

        # 2. aggregate the data
        expr = [
            expr.min().alias("min"),
            expr.quantile(0.25).alias("q1"),
            expr.median().alias("median"),
            expr.quantile(0.75).alias("q3"),
            expr.max().alias("max"),
        ]

        # 3. store the aggregated data in a horizontal array of structs
        expr = pl.struct(expr).alias(self.uid).reshape((1, -1))

        return expr

    def _to_update(
        self, df_agg: pl.DataFrame, trace_idx: int, **kwargs
    ) -> Dict[str, list]:
        stats: Dict[str, float] = df_agg[self.uid].item().item()

        iqr = stats["q3"] - stats["q1"]
        data = {
            "lowerfence": [max(stats["q1"] - 1.5 * iqr, stats["min"])],
            "q1": [stats["q1"]],
            "median": [stats["median"]],
            "q3": [stats["q3"]],
            "upperfence": [min(stats["q3"] + 1.5 * iqr, stats["max"])],
        }

        prop_key = self.get_prop_key  # either x or y
        if prop_key == "x":
            # for some reason this requres fig.update_xaxes(type="linear") to correctly
            # display the lower whisker
            data["orientation"] = "h"
            data["y0"] = self.get_name(trace_idx)
        else:
            assert prop_key == "y"
            data["orientation"] = "v"
            data["x0"] = self.get_name(trace_idx)

        return data
