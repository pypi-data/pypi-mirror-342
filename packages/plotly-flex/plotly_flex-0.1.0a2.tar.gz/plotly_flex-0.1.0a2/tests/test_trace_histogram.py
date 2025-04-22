import pytest
import random

import plotly.graph_objects as go
import numpy as np
import pandas as pd
import polars as pl
import pyarrow as pa

from plotly_flex import ScalableFigure
from plotly_flex.trace import ScalableHistogram

from .utils import get_trace_update

DATA_LENGTH = 200

ARR = [random.random() for _ in range(DATA_LENGTH)]


def _generate_arr():
    arr = ARR.copy()
    return [
        arr,
        np.array(arr),
        pd.Series(arr),
        pd.Series(arr).values,
        pl.Series("arr", arr),
    ]


def _generate_data(only_polars_lazy: bool):
    arr = ARR.copy()
    data_list = [pl.LazyFrame({"arr": arr})]
    if not only_polars_lazy:
        data_list += [
            pl.DataFrame({"arr": arr}),
            pd.DataFrame({"arr": arr}),
            pa.Table.from_pydict({"arr": pa.array(arr)}),
        ]
    return data_list


@pytest.mark.parametrize("arr", _generate_arr())
def test_histogram_x_y_materialized(arr):
    """Test the aggregate_data method of ScalableHistogram.

    The x and y arguments are materialized (arrays or series).
    """
    # Case 1: passing x
    trace = ScalableHistogram(x=arr, bins=50, uid="some_uid")
    assert trace.x is None and trace.y is None
    trace_data = get_trace_update(trace, None, {})
    assert len(trace_data["x"]) == 50
    assert all(trace_data["x"][1:] > trace_data["x"][:-1])  # monotonically increasing
    assert len(trace_data["y"]) == 50
    assert sum(trace_data["y"]) == DATA_LENGTH  # sum of the counts
    # Case 2: passing y
    trace = ScalableHistogram(y=arr, bins=50, uid="some_uid")
    assert trace.x is None and trace.y is None
    trace_data = get_trace_update(trace, None, {})
    assert len(trace_data["y"]) == 50
    assert all(trace_data["y"][1:] > trace_data["y"][:-1])  # monotonically increasing
    assert len(trace_data["x"]) == 50
    assert sum(trace_data["x"]) == DATA_LENGTH  # sum of the counts


# ScalableTrace aggregate_data method is not implemented for non-polars data
@pytest.mark.parametrize("data", _generate_data(only_polars_lazy=True))
def test_histogram_data(data):
    """Test the aggregate_data method of ScalableHistogram.

    The x and y arguments are keys (strings) of the data (DataFrame or LazyFrame).
    """
    # Case 1: passing x
    trace = ScalableHistogram(x="arr", bins=50, uid="some_uid")
    assert trace.x is None and trace.y is None
    trace_data = get_trace_update(trace, data, {})
    assert len(trace_data["x"]) == 50
    assert all(trace_data["x"][1:] > trace_data["x"][:-1])  # monotonically increasing
    assert len(trace_data["y"]) == 50
    assert sum(trace_data["y"]) == DATA_LENGTH  # sum of the counts
    # Case 2: passing y
    trace = ScalableHistogram(y="arr", bins=50, uid="some_uid")
    assert trace.x is None and trace.y is None
    trace_data = get_trace_update(trace, data, {})
    assert len(trace_data["y"]) == 50
    assert all(trace_data["y"][1:] > trace_data["y"][:-1])  # monotonically increasing
    assert len(trace_data["x"]) == 50
    assert sum(trace_data["x"]) == DATA_LENGTH  # sum of the counts


@pytest.mark.parametrize("arr", _generate_arr())
@pytest.mark.parametrize("HistogramClass", [go.Histogram, ScalableHistogram])
def test_histogram_scalable_figure_x_y_materialized(arr, HistogramClass):
    """Test the ScalableFigure with ScalableHistogram.

    The x and y arguments are materialized (arrays or series).
    """
    # Case 1: passing x
    fig = ScalableFigure()
    fig.add_trace(HistogramClass(x=arr))
    assert len(fig._scalable_traces) == 1 and len(fig.data) == 1
    assert fig.data[0].x is None and fig.data[0].y is None
    trace_data = fig._construct_update_data({}, force_update=True)[1:]
    assert len(trace_data) == 1
    assert trace_data[0]["index"] == 0
    assert len(trace_data[0]["x"]) == 20
    assert all(trace_data[0]["x"][1:] > trace_data[0]["x"][:-1])
    assert len(trace_data[0]["y"]) == 20
    assert sum(trace_data[0]["y"]) == DATA_LENGTH
    # Case 2: passing y
    fig = ScalableFigure()
    fig.add_trace(HistogramClass(y=arr))
    assert len(fig._scalable_traces) == 1 and len(fig.data) == 1
    assert fig.data[0].x is None and fig.data[0].y is None
    trace_data = fig._construct_update_data({}, force_update=True)[1:]
    assert len(trace_data) == 1
    assert trace_data[0]["index"] == 0
    assert len(trace_data[0]["y"]) == 20
    assert all(trace_data[0]["y"][1:] > trace_data[0]["y"][:-1])
    assert len(trace_data[0]["x"]) == 20


# When utilizing the ScalableFigure, the data should be converted to polars
@pytest.mark.parametrize("data", _generate_data(only_polars_lazy=False))
def test_histogram_scalable_figure_data(data):
    """Test the ScalableFigure with ScalableHistogram.

    The x and y arguments are keys (strings) of the data (DataFrame or LazyFrame).
    """
    # Case 1: passing x
    fig = ScalableFigure(backend_data=data)
    fig.add_trace(ScalableHistogram(x="arr"))
    assert len(fig._scalable_traces) == 1 and len(fig.data) == 1
    assert fig.data[0].x is None and fig.data[0].y is None
    trace_data = fig._construct_update_data({}, force_update=True)[1:]
    assert len(trace_data) == 1
    assert trace_data[0]["index"] == 0
    assert len(trace_data[0]["x"]) == 20
    assert all(trace_data[0]["x"][1:] > trace_data[0]["x"][:-1])
    assert len(trace_data[0]["y"]) == 20
    assert sum(trace_data[0]["y"]) == DATA_LENGTH
    # Case 2: passing y
    fig = ScalableFigure(backend_data=data)
    fig.add_trace(ScalableHistogram(y="arr"))
    assert len(fig._scalable_traces) == 1 and len(fig.data) == 1
    assert fig.data[0].x is None and fig.data[0].y is None
    trace_data = fig._construct_update_data({}, force_update=True)[1:]
    assert len(trace_data) == 1
    assert trace_data[0]["index"] == 0
    assert len(trace_data[0]["y"]) == 20
    assert all(trace_data[0]["y"][1:] > trace_data[0]["y"][:-1])
    assert len(trace_data[0]["x"]) == 20
    assert sum(trace_data[0]["x"]) == DATA_LENGTH


def test_histogram_scalable_figure_mixed_data():
    """Test the ScalableFigure with ScalableHistogram.

    The x and y arguments are mixed (arrays and keys of the data).
    """
    # Case 1: passing x
    fig = ScalableFigure(backend_data=pl.LazyFrame({"arr": ARR}))
    fig.add_trace(ScalableHistogram(x=ARR))
    fig.add_trace(ScalableHistogram(x="arr"))
    fig.add_trace(go.Histogram(x=ARR))
    assert len(fig._scalable_traces) == 3 and len(fig.data) == 3
    assert all(trace.x is None and trace.y is None for trace in fig.data)
    trace_data = fig._construct_update_data({}, force_update=True)[1:]
    assert len(trace_data) == 3
    for idx, trace_data in enumerate(trace_data):
        assert trace_data["index"] == idx
        assert len(trace_data["x"]) == 20
        assert all(trace_data["x"][1:] > trace_data["x"][:-1])
        assert len(trace_data["y"])
        assert sum(trace_data["y"]) == DATA_LENGTH
    # Case 2: passing y
    fig = ScalableFigure(backend_data=pl.LazyFrame({"arr": ARR}))
    fig.add_trace(ScalableHistogram(y=ARR))
    fig.add_trace(ScalableHistogram(y="arr"))
    fig.add_trace(go.Histogram(y=ARR))
    assert len(fig._scalable_traces) == 3 and len(fig.data) == 3
    assert all(trace.x is None and trace.y is None for trace in fig.data)
    trace_data = fig._construct_update_data({}, force_update=True)[1:]
    assert len(trace_data) == 3
    for idx, trace_data in enumerate(trace_data):
        assert trace_data["index"] == idx
        assert len(trace_data["y"]) == 20
        assert all(trace_data["y"][1:] > trace_data["y"][:-1])
        assert len(trace_data["x"])
        assert sum(trace_data["x"]) == DATA_LENGTH


@pytest.mark.parametrize(
    "histnorm_value",
    [
        (None, 100),
        ("count", 100),
        ("percent", 20),
        ("probability", 0.2),
        ("density", 1),
        ("probability density", 0.002),
    ],
)
def test_histogram_histnorm(histnorm_value):
    """Test the histnorm argument of ScalableHistogram."""
    histnorm, expected_value = histnorm_value
    x = list(range(500))
    hist = ScalableHistogram(x=x, histnorm=histnorm, bins=5, uid="some_uid")
    trace_data = get_trace_update(hist, None, {})
    assert len(trace_data["x"]) == 5
    assert all(trace_data["x"][1:] > trace_data["x"][:-1])
    assert len(trace_data["y"]) == 5
    assert np.allclose(trace_data["y"], expected_value, atol=1e-2)
