import polars as pl
import plotly.graph_objects as go

from .scalable_trace_interface import AbstractScalableTrace
from ..LF import LFQueryBuilder

from typing import Optional, List, Dict, Tuple


class ScalablePie(AbstractScalableTrace, go.Pie):
    """Scalable pie trace."""

    def __init__(self, **kwargs):
        super().__init__(update_on_zoom=False, **kwargs)

    @property
    def get_backend_data_keys(self):
        return ["labels", "values"]

    def _validate_figure_data_trace(self, data: Optional[LFQueryBuilder]):
        assert "labels" in self._backend_data, "labels should be provided"
        assert "values" in self._backend_data, "values should be provided"

    def get_filter_backend_data_keys(self) -> List[str]:
        # TODO: pie chart does not allow filtering => return empty list??
        return []

    def _get_agg_expr(self, update_range: Dict[str, Tuple[float, float]]) -> pl.Expr:
        expr = pl.col(
            [self.resolve_data_column("labels"), self.resolve_data_column("values")]
        )

        # 1. filter the data
        # TODO? => you cannot zoom in a pie plot
        assert not update_range, "Pie plot does not support zooming"

        # 2. aggregate the data
        # no-op - # TODO No need to sort as frontend changes the order??

        # 3. store the aggregated data in a horizontal array of structs
        expr = pl.struct(expr).alias(self.uid).reshape((1, -1))

        return expr

    def _to_update(self, df_agg: pl.DataFrame, **kwargs) -> Dict[str, list]:
        data = df_agg[self.uid].item().struct.unnest()

        return {
            "labels": data[self.resolve_data_column("labels")].to_numpy(),
            "values": data[self.resolve_data_column("values")].to_numpy(),
        }
