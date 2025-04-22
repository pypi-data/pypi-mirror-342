import pytest
import plotly.graph_objects as go

from plotly_flex import ScalableFigure  # , ScalableFigureWidget
from plotly_flex.utils import (
    is_figure,
    is_scalable_figure,
)


@pytest.mark.parametrize(
    "obj",
    [
        go.Figure(),
        go.Figure({"type": "scatter", "y": [1, 2, 3]}),
        ScalableFigure(),
        ScalableFigure({"type": "scatter", "y": [1, 2, 3]}),
    ],
)
def test_is_figure(obj):
    assert is_figure(obj)


@pytest.mark.parametrize(
    "obj",
    [
        go.FigureWidget(),
        None,
        {"type": "scatter", "y": [1, 2, 3]},
        go.Scatter(y=[1, 2, 3]),
    ],
)
def test_not_is_figure(obj):
    assert not is_figure(obj)


def test_is_scalable_figure():
    fig_dict = {"type": "scatter", "y": [1, 2, 3]}
    assert is_scalable_figure(ScalableFigure())
    assert is_scalable_figure(ScalableFigure(fig_dict))
    assert not is_scalable_figure(go.Figure())
    assert not is_scalable_figure(go.Figure(fig_dict))
    assert not is_scalable_figure(go.FigureWidget())
    assert not is_scalable_figure(None)
    assert not is_scalable_figure(fig_dict)
    assert not is_scalable_figure(go.Scatter(y=[1, 2, 3]))
