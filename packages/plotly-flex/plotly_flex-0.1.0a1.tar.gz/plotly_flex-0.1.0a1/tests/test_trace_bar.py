import pytest

import plotly.graph_objects as go
import numpy as np
import pandas as pd
import polars as pl
import pyarrow as pa

from plotly_flex import ScalableFigure
from plotly_flex.trace import ScalableBar

from .utils import get_trace_update

DATA_LENGTH = 200

X = list(range(DATA_LENGTH))
Y = [i**0.5 for i in range(DATA_LENGTH)]


def _generate_x():
    arr = X.copy()
    return [
        arr,
        np.array(arr),
        pd.Series(arr),
        pd.Series(arr).index,
        pd.Series(arr).values,
        pl.Series("x", arr),
    ]


def _generate_y():
    arr = Y.copy()
    return [
        arr,
        np.array(arr),
        pd.Series(arr),
        pd.Series(arr).values,
        pl.Series("y", arr),
    ]


def _generate_data(only_polars_lazy: bool):
    x, y = X.copy(), Y.copy()
    data_list = [pl.LazyFrame({"x": x, "y": y})]
    if not only_polars_lazy:
        data_list += [
            pl.DataFrame({"x": x, "y": y}),
            pd.DataFrame({"x": x, "y": y}),
            pa.Table.from_pydict({"x": pa.array(x), "y": pa.array(y)}),
        ]
    return data_list


@pytest.mark.parametrize("x", _generate_x())
@pytest.mark.parametrize("y", _generate_y())
def test_bar_x_y_materialized(x, y):
    """Test the aggregate_data method of ScalableBar.

    The x and y arguments are materialized (arrays or series).
    """
    # Case 1: vertical bar
    trace = ScalableBar(x=x, y=y, uid="some_uid")
    assert trace.x is None and trace.y is None
    trace_data = get_trace_update(trace, None, {})
    assert np.allclose(trace_data["x"], X)
    assert np.allclose(trace_data["y"], Y)
    # Case 2: horizontal bar
    trace = ScalableBar(x=y, y=x, orientation="h", uid="some_uid")
    assert trace.x is None and trace.y is None
    trace_data = get_trace_update(trace, None, {})
    assert np.allclose(trace_data["x"], Y)
    assert np.allclose(trace_data["y"], X)


# ScalableBar aggregate_data method is not implemented for non-polars data
@pytest.mark.parametrize("data", _generate_data(only_polars_lazy=True))
def test_bar_data(data):
    """Test the aggregate_data method of ScalableBar.

    The x and y arguments are keys (strings) of the data (DataFrame or LazyFrame).
    """
    # Case 1: vertical bar
    trace = ScalableBar(x="x", y="y", uid="some_uid")
    assert trace.x is None and trace.y is None
    trace_data = get_trace_update(trace, data, {})
    assert np.allclose(trace_data["x"], X)
    assert np.allclose(trace_data["y"], Y)
    # Case 2: horizontal bar
    trace = ScalableBar(x="y", y="x", orientation="h", uid="some_uid")
    assert trace.x is None and trace.y is None
    trace_data = get_trace_update(trace, data, {})
    assert np.allclose(trace_data["x"], Y)
    assert np.allclose(trace_data["y"], X)


@pytest.mark.parametrize("x", _generate_x())
@pytest.mark.parametrize("y", _generate_y())
@pytest.mark.parametrize("BarClass", [go.Bar, ScalableBar])
def test_bar_scalable_figure_x_y_materialized(x, y, BarClass):
    """Test the ScalableFigure with ScalableBar.

    The x and y arguments are materialized (arrays or series).
    """
    # Case 1: vertical bar
    fig = ScalableFigure()
    fig.add_trace(BarClass(x=x, y=y))
    assert len(fig._scalable_traces) == 1 and len(fig.data) == 1
    assert fig.data[0].x is None and fig.data[0].y is None
    trace_data = fig._construct_update_data({}, force_update=True)[1:]
    assert len(trace_data) == 1
    assert trace_data[0]["index"] == 0
    assert np.allclose(trace_data[0]["x"], X)
    assert np.allclose(trace_data[0]["y"], Y)
    # Case 2: horizontal bar
    fig = ScalableFigure()
    fig.add_trace(BarClass(x=y, y=x, orientation="h"))
    assert len(fig._scalable_traces) == 1 and len(fig.data) == 1
    assert fig.data[0].x is None and fig.data[0].y is None
    trace_data = fig._construct_update_data({}, force_update=True)[1:]
    assert len(trace_data) == 1
    assert trace_data[0]["index"] == 0
    assert np.allclose(trace_data[0]["x"], Y)
    assert np.allclose(trace_data[0]["y"], X)


# When utilizing the ScalableFigure, the data should be converted to polars
@pytest.mark.parametrize("data", _generate_data(only_polars_lazy=False))
def test_bar_scalable_figure_data(data):
    """Test the ScalableFigure with ScalableBar.

    The x and y arguments are keys (strings) of the data (DataFrame or LazyFrame).
    """
    # Case 1: vertical bar
    fig = ScalableFigure(backend_data=data)
    fig.add_trace(ScalableBar(x="x", y="y"))
    assert len(fig._scalable_traces) == 1 and len(fig.data) == 1
    assert fig.data[0].x is None and fig.data[0].y is None
    trace_data = fig._construct_update_data({}, force_update=True)[1:]
    assert len(trace_data) == 1
    assert trace_data[0]["index"] == 0
    assert np.allclose(trace_data[0]["x"], X)
    assert np.allclose(trace_data[0]["y"], Y)
    # Case 2: horizontal bar
    fig = ScalableFigure(backend_data=data)
    fig.add_trace(ScalableBar(x="y", y="x", orientation="h"))
    assert len(fig._scalable_traces) == 1 and len(fig.data) == 1
    assert fig.data[0].x is None and fig.data[0].y is None
    trace_data = fig._construct_update_data({}, force_update=True)[1:]
    assert len(trace_data) == 1
    assert trace_data[0]["index"] == 0
    assert np.allclose(trace_data[0]["x"], Y)
    assert np.allclose(trace_data[0]["y"], X)


def test_bar_scalable_figure_mixed_data():
    """Test the ScalableFigure with ScalableBar.

    The x and y arguments are mixed (materialized and keys of the data).
    """
    # Case 1: vertical bar
    fig = ScalableFigure(backend_data=pl.DataFrame({"x": X, "y": Y}))
    fig.add_trace(ScalableBar(x=X, y=Y))
    fig.add_trace(ScalableBar(x="x", y="y"))
    fig.add_trace(go.Bar(x=X, y=Y))
    assert len(fig._scalable_traces) == 3 and len(fig.data) == 3
    assert all(trace.x is None and trace.y is None for trace in fig.data)
    trace_data = fig._construct_update_data({}, force_update=True)[1:]
    assert len(trace_data) == 3
    for idx, trace_data in enumerate(trace_data):
        assert trace_data["index"] == idx
        assert np.allclose(trace_data["x"], X)
        assert np.allclose(trace_data["y"], Y)
    # Case 2: horizontal bar
    fig = ScalableFigure(backend_data=pl.DataFrame({"x": X, "y": Y}))
    fig.add_trace(ScalableBar(x=Y, y=X, orientation="h"))
    fig.add_trace(ScalableBar(x="y", y="x", orientation="h"))
    fig.add_trace(go.Bar(x=Y, y=X, orientation="h"))
    assert len(fig._scalable_traces) == 3 and len(fig.data) == 3
    assert all(trace.x is None and trace.y is None for trace in fig.data)
    trace_data = fig._construct_update_data({}, force_update=True)[1:]
    assert len(trace_data) == 3
    for idx, trace_data in enumerate(trace_data):
        assert trace_data["index"] == idx
        assert np.allclose(trace_data["x"], Y)
        assert np.allclose(trace_data["y"], X)
