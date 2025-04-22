import polars as pl
import numpy as np
import plotly.graph_objects as go

from .scalable_trace_interface import AbstractScalableTrace
from .utils import range_to_idx
from ..LF import LFQueryBuilder

from typing import Optional, List, Dict, Tuple


class ScalableBar(AbstractScalableTrace, go.Bar):
    """Scalable bar trace."""

    def __init__(self, **kwargs):
        # we log the labels here to be able to filter when they are non-numeric
        # -> see get_filter_backend_data_keys & filter_selection
        self._labels = None
        super().__init__(update_on_zoom=False, **kwargs)

    @property
    def get_backend_data_keys(self):
        return ["x", "y"]

    @property
    def get_label_key(self) -> str:
        """Return the single key that represents the labels of the barplot.

        Notes
        -----
        Conceptually we view a barplot as a chart with a label axis and a value axis.
        Which axis is which depends on the orientation of the barplot:
        - The label axis is the axis that contains the names / indices at the base of
          the bars.
        - The value axis is the axis that makes up the height of the bars.

        The key to filter on is the label axis.
        """
        if self.orientation == "h":  # bars are horizontal (non default)
            return "y"
        # bars are vertical (default)
        assert self.orientation is None or self.orientation == "v"
        return "x"

    def _validate_figure_data_trace(self, data: Optional[LFQueryBuilder]):
        assert "x" in self._backend_data, "x should be provided"
        assert "y" in self._backend_data, "y should be provided"

    def get_filter_backend_data_keys(self) -> List[str]:
        return [self.get_label_key]

    # Note: this override is needed to deal with non-numeric data on the label axis
    def filter_selection(
        self,
        selection_range: Dict[str, Tuple[float, float]],
    ) -> List[pl.Expr]:
        assert self._labels is not None, "No labels found"
        if np.issubdtype(self._labels.dtype, np.number):
            # TODO: should be tested
            # data is numeric => we can use the super filter_selection
            return super().filter_selection(selection_range)
        # data is non-numeric => select the labels and use is_in to filter
        key = self.get_filter_backend_data_keys()[0]
        # since the front-end selection are floats indicating the range, we need to
        # convert them to indices to retrieve the labels associated with the selection
        start, end = range_to_idx(*selection_range[key])
        return [pl.col(self._backend_data[key]).is_in(self._labels[start:end])]

    def _get_agg_expr(self, update_range: Dict[str, Tuple[float, float]]) -> pl.Expr:
        expr = pl.col([self.resolve_data_column("x"), self.resolve_data_column("y")])

        # 1. filter the data
        # TODO handle update_range properly => does not support zooming
        assert not update_range, "Bar plot does not support zooming"

        # 2. aggregate the data
        # no-op - just sort on the label axis
        label_col: str = self.resolve_data_column(self.get_label_key)
        expr = expr.sort_by(label_col)

        # 3. store the aggregated data in a horizontal array of structs
        expr = pl.struct(expr).alias(self.uid).reshape((1, -1))

        return expr

    def _to_update(self, df_agg: pl.DataFrame, **kwargs) -> Dict[str, list]:
        data = df_agg[self.uid].item().struct.unnest()

        # 3. store and return the data with the correct props for the front-end update
        label_col: str = self.resolve_data_column(self.get_label_key)
        self._labels = data[label_col].to_numpy()  # store labels (for selection filter)

        return {
            "x": data[self.resolve_data_column("x")].to_numpy(),
            "y": data[self.resolve_data_column("y")].to_numpy(),
        }
