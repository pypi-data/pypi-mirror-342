import pytest

import plotly.graph_objects as go
import numpy as np
import pandas as pd
import polars as pl
import pyarrow as pa
# import duckdb

from plotly_flex import ScalableFigure
from plotly_flex.trace import ScalableScatter1D, ScalableScattergl1D

from .utils import get_trace_update

DATA_LENGTH = 200
NB_POINTS_LIMIT = 50

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
    # x_np, y_np = np.array(x), np.array(y)
    data_list = [pl.LazyFrame({"x": x, "y": y})]
    if not only_polars_lazy:
        data_list += [
            pl.DataFrame({"x": x, "y": y}),
            pd.DataFrame({"x": x, "y": y}),
            pa.Table.from_pydict({"x": pa.array(x), "y": pa.array(y)}),
        ]
        # TODO: narwhals duckdb support is not yet ready I guess?
        # duckdb.sql("SELECT x_np.column0 as x, y_np.column0 as y FROM x_np, y_np"),
    return data_list


@pytest.mark.parametrize("x", _generate_x())
@pytest.mark.parametrize("y", _generate_y())
@pytest.mark.parametrize("ScatterClass", [ScalableScatter1D, ScalableScattergl1D])
def test_scatter_x_y_materialized(x, y, ScatterClass):
    """Test the aggregate_data method of ScalableScatter / ScalableScattergl.

    The x and y arguments are materialized (arrays or series).
    """
    # Case 1: list smaller than nb_points
    # -- 1.1 x and y
    trace = ScatterClass(x=x, y=y, uid="some_uid")
    assert trace.x is None and trace.y is None
    trace_data = get_trace_update(trace, None, {})
    assert np.allclose(trace_data["x"], X)
    assert np.allclose(trace_data["y"], Y)
    # -- 1.2 only y
    trace = ScatterClass(y=y, uid="some_uid")
    assert trace.x is None and trace.y is None
    trace_data = get_trace_update(trace, None, {})
    assert np.allclose(trace_data["x"], X)
    assert np.allclose(trace_data["y"], Y)
    # Case 2: list larger than nb_points
    # -- 2.1 x and y
    trace = ScatterClass(x=x, y=y, nb_points=NB_POINTS_LIMIT, uid="some_uid")
    assert trace.x is None and trace.y is None
    trace_data = get_trace_update(trace, None, {})
    assert np.allclose(trace_data["x"], X[::4])  # TODO: only correct for every_nth
    assert np.allclose(trace_data["y"], Y[::4])
    # -- 2.2 only y
    trace = ScatterClass(y=y, nb_points=NB_POINTS_LIMIT, uid="some_uid")
    assert trace.x is None and trace.y is None
    trace_data = get_trace_update(trace, None, {})
    assert np.allclose(trace_data["x"], X[::4])
    assert np.allclose(trace_data["y"], Y[::4])


# ScalableTrace aggregate_data method is not implemented for non-polars data
@pytest.mark.parametrize("data", _generate_data(only_polars_lazy=True))
@pytest.mark.parametrize("ScatterClass", [ScalableScatter1D, ScalableScattergl1D])
def test_scatter_data(data, ScatterClass):
    """Test the aggregate_data method of ScalableScatter / ScalableScattergl.

    The x and y arguments are keys (strings) of the data (DataFrame or LazyFrame).
    """
    # Case 1: dataframe smaller than nb_points
    # -- 1.1 x and y
    trace = ScatterClass(x="x", y="y", uid="some_uid")
    assert trace.x is None and trace.y is None
    trace_data = get_trace_update(trace, data, {})
    assert np.allclose(trace_data["x"], X)
    assert np.allclose(trace_data["y"], Y)
    # -- 1.2 only y
    trace = ScatterClass(y="y", uid="some_uid")
    assert trace.x is None and trace.y is None
    trace_data = get_trace_update(trace, data, {})
    assert np.allclose(trace_data["x"], X)
    assert np.allclose(trace_data["y"], Y)
    # Case 2: dataframe larger than nb_points
    # -- 2.1 x and y
    trace = ScatterClass(x="x", y="y", nb_points=NB_POINTS_LIMIT, uid="some_uid")
    assert trace.x is None and trace.y is None
    trace_data = get_trace_update(trace, data, {})
    assert np.allclose(trace_data["x"], X[::4])  # TODO: only correct for every_nth
    assert np.allclose(trace_data["y"], Y[::4])
    # -- 2.2 only y
    trace = ScatterClass(y="y", nb_points=NB_POINTS_LIMIT, uid="some_uid")
    assert trace.x is None and trace.y is None
    trace_data = get_trace_update(trace, data, {})
    assert np.allclose(trace_data["x"], X[::4])
    assert np.allclose(trace_data["y"], Y[::4])


@pytest.mark.parametrize("x", _generate_x())
@pytest.mark.parametrize("y", _generate_y())
@pytest.mark.parametrize(
    "ScatterClass", [go.Scatter, ScalableScatter1D, go.Scattergl, ScalableScattergl1D]
)
def test_scatter_scalable_figure_x_y_materialized(x, y, ScatterClass):
    """Test the ScalableFigure with ScalableScatter / ScalableScattergl.

    The x and y arguments are materialized (arrays or series).
    """
    # Case 1: list smaller than nb_points
    # -- 1.1 x and y
    fig = ScalableFigure()
    fig.add_trace(ScatterClass(x=x, y=y))
    assert len(fig._scalable_traces) == 1 and len(fig.data) == 1
    assert fig.data[0].x is None and fig.data[0].y is None
    trace_data = fig._construct_update_data({}, force_update=True)[1:]
    assert len(trace_data) == 1
    assert trace_data[0]["index"] == 0
    assert np.allclose(trace_data[0]["x"], X)
    assert np.allclose(trace_data[0]["y"], Y)
    # -- 1.2 only y
    fig = ScalableFigure()
    fig.add_trace(ScatterClass(y=y))
    assert len(fig._scalable_traces) == 1 and len(fig.data) == 1
    assert fig.data[0].x is None and fig.data[0].y is None
    trace_data = fig._construct_update_data({}, force_update=True)[1:]
    assert len(trace_data) == 1
    assert trace_data[0]["index"] == 0
    assert np.allclose(trace_data[0]["x"], X)
    assert np.allclose(trace_data[0]["y"], Y)
    # Case 2: list larger than nb_points
    if ScatterClass in [ScalableScatter1D, ScalableScattergl1D]:
        # -- 2.1 x and y
        fig = ScalableFigure()
        fig.add_trace(ScatterClass(x=x, y=y, nb_points=NB_POINTS_LIMIT))
        assert len(fig._scalable_traces) == 1 and len(fig.data) == 1
        assert fig.data[0].x is None and fig.data[0].y is None
        trace_data = fig._construct_update_data({}, force_update=True)[1:]
        assert len(trace_data) == 1
        assert trace_data[0]["index"] == 0
        assert np.allclose(trace_data[0]["x"], X[::4])
        assert np.allclose(trace_data[0]["y"], Y[::4])
        # -- 2.2 only y
        fig = ScalableFigure()
        fig.add_trace(ScatterClass(y=y, nb_points=NB_POINTS_LIMIT))
        assert len(fig._scalable_traces) == 1 and len(fig.data) == 1
        assert fig.data[0].x is None and fig.data[0].y is None
        trace_data = fig._construct_update_data({}, force_update=True)[1:]
        assert len(trace_data) == 1
        assert trace_data[0]["index"] == 0
        assert np.allclose(trace_data[0]["x"], X[::4])
        assert np.allclose(trace_data[0]["y"], Y[::4])


# When utilizing the ScalableFigure, the data should be converted to polars
@pytest.mark.parametrize("data", _generate_data(only_polars_lazy=False))
@pytest.mark.parametrize("ScatterClass", [ScalableScatter1D, ScalableScattergl1D])
def test_scatter_scalable_figure_data(data, ScatterClass):
    """Test the ScalableFigure with ScalableScatter / ScalableScattergl.

    The x and y arguments are keys (strings) of the data (DataFrame or LazyFrame).
    """
    # Case 1: dataframe smaller than nb_points
    fig = ScalableFigure(backend_data=data)
    fig.add_trace(ScatterClass(x="x", y="y"))
    assert len(fig._scalable_traces) == 1 and len(fig.data) == 1
    assert fig.data[0].x is None and fig.data[0].y is None
    trace_data = fig._construct_update_data({}, force_update=True)[1:]
    assert len(trace_data) == 1
    assert trace_data[0]["index"] == 0
    assert np.allclose(trace_data[0]["x"], X)
    assert np.allclose(trace_data[0]["y"], Y)
    # Case 2: dataframe larger than nb_points
    fig = ScalableFigure(backend_data=data)
    fig.add_trace(ScatterClass(x="x", y="y", nb_points=NB_POINTS_LIMIT))
    assert len(fig._scalable_traces) == 1 and len(fig.data) == 1
    assert fig.data[0].x is None and fig.data[0].y is None
    trace_data = fig._construct_update_data({}, force_update=True)[1:]
    assert len(trace_data) == 1
    assert trace_data[0]["index"] == 0
    assert np.allclose(trace_data[0]["x"], X[::4])
    assert np.allclose(trace_data[0]["y"], Y[::4])


def test_scatter_scalable_figure_mixed_data():
    """Test the ScalableFigure with ScalableScatter / ScalableScattergl.

    The x and y arguments are mixed (arrays and keys of the data).
    """
    # Case 1: dataframe smaller than nb_points
    fig = ScalableFigure(backend_data=pl.LazyFrame({"x": X, "y": Y}))
    fig.add_trace(ScalableScatter1D(x="x", y="y"))
    fig.add_trace(ScalableScattergl1D(x="x", y="y"))
    fig.add_trace(ScalableScatter1D(y="y"))
    fig.add_trace(ScalableScattergl1D(y="y"))
    fig.add_trace(go.Scatter(x=X, y=Y))
    fig.add_trace(go.Scattergl(x=X, y=Y))
    fig.add_trace(go.Scatter(y=Y))
    fig.add_trace(go.Scattergl(y=Y))
    assert len(fig._scalable_traces) == 8 and len(fig.data) == 8
    assert all(trace.x is None and trace.y is None for trace in fig.data)
    trace_data = fig._construct_update_data({}, force_update=True)[1:]
    assert len(trace_data) == 8
    for idx, trace_data in enumerate(trace_data):
        assert trace_data["index"] == idx
        assert np.allclose(trace_data["x"], X)
        assert np.allclose(trace_data["y"], Y)
    # Case 2: dataframe larger than nb_points
    fig = ScalableFigure(backend_data=pl.LazyFrame({"x": X, "y": Y}))
    fig.add_trace(ScalableScatter1D(x="x", y="y", nb_points=NB_POINTS_LIMIT))
    fig.add_trace(ScalableScattergl1D(x="x", y="y", nb_points=NB_POINTS_LIMIT))
    fig.add_trace(ScalableScatter1D(y="y", nb_points=NB_POINTS_LIMIT))
    fig.add_trace(ScalableScattergl1D(y="y", nb_points=NB_POINTS_LIMIT))
    # cannot set nb_points for go.Scatter and go.Scattergl
    assert len(fig._scalable_traces) == 4 and len(fig.data) == 4
    assert all(trace.x is None and trace.y is None for trace in fig.data)
    trace_data = fig._construct_update_data({}, force_update=True)[1:]
    assert len(trace_data) == 4
    for idx, trace_data in enumerate(trace_data):
        assert trace_data["index"] == idx
        assert np.allclose(trace_data["x"], X[::4])
        assert np.allclose(trace_data["y"], Y[::4])
