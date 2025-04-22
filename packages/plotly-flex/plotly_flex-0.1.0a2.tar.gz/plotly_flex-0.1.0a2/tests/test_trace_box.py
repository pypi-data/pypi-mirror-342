import pytest

import plotly.graph_objects as go
import numpy as np
import pandas as pd
import polars as pl
import pyarrow as pa

from plotly_flex import ScalableFigure
from plotly_flex.trace import ScalableBox

from .utils import get_trace_update

DATA_LENGTH = 200

ARR = list(range(DATA_LENGTH))


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
def test_box_x_y_materialized(arr):
    """Test the aggregate_data method of ScalableBox.

    The x and y arguments are materialized (arrays or series).
    """
    # Case 1: passing x
    trace = ScalableBox(x=arr, uid="some_uid")
    assert trace.x is None and trace.y is None
    trace_data = get_trace_update(trace, None, {}, trace_idx=0)
    assert trace_data["orientation"] == "h"
    assert trace_data["lowerfence"] == [0]
    assert trace_data["upperfence"] == [DATA_LENGTH - 1]
    assert trace_data["median"] == [(DATA_LENGTH - 1) / 2]
    # Case 2: passing y
    trace = ScalableBox(y=arr, uid="some_uid")
    assert trace.x is None and trace.y is None
    trace_data = get_trace_update(trace, None, {}, trace_idx=0)
    assert trace_data["orientation"] == "v"
    assert trace_data["lowerfence"] == [0]
    assert trace_data["upperfence"] == [DATA_LENGTH - 1]
    assert trace_data["median"] == [(DATA_LENGTH - 1) / 2]


# ScalableTrace aggregate_data method is not implemented for non-polars data
@pytest.mark.parametrize("data", _generate_data(only_polars_lazy=True))
def test_box_data(data):
    """Test the aggregate_data method of ScalableBox.

    The x and y arguments are keys (strings) of the data (DataFrame or LazyFrame).
    """
    # Case 1: passing x
    trace = ScalableBox(x="arr", uid="some_uid")
    assert trace.x is None and trace.y is None
    trace_data = get_trace_update(trace, data, {}, trace_idx=0)
    assert trace_data["orientation"] == "h"
    assert trace_data["lowerfence"] == [0]
    assert trace_data["upperfence"] == [DATA_LENGTH - 1]
    assert trace_data["median"] == [(DATA_LENGTH - 1) / 2]
    # Case 2: passing y
    trace = ScalableBox(y="arr", uid="some_uid")
    assert trace.x is None and trace.y is None
    trace_data = get_trace_update(trace, data, {}, trace_idx=0)
    assert trace_data["orientation"] == "v"
    assert trace_data["lowerfence"] == [0]
    assert trace_data["upperfence"] == [DATA_LENGTH - 1]
    assert trace_data["median"] == [(DATA_LENGTH - 1) / 2]


@pytest.mark.parametrize("arr", _generate_arr())
@pytest.mark.parametrize("BoxClass", [go.Box, ScalableBox])
def test_box_scalable_figure_x_y_materialized(arr, BoxClass):
    """Test the ScalableFigure with ScalableBox.

    The x and y arguments are materialized (arrays or series).
    """
    # Case 1: passing x
    fig = ScalableFigure()
    fig.add_trace(BoxClass(x=arr))
    assert len(fig._scalable_traces) == 1 and len(fig.data) == 1
    assert fig.data[0].x is None and fig.data[0].y is None
    trace_data = fig._construct_update_data({}, force_update=True)[1:]
    assert len(trace_data) == 1
    assert trace_data[0]["orientation"] == "h"
    assert trace_data[0]["lowerfence"] == [0]
    assert trace_data[0]["upperfence"] == [DATA_LENGTH - 1]
    assert trace_data[0]["median"] == [(DATA_LENGTH - 1) / 2]
    # Case 2: passing y
    fig = ScalableFigure()
    fig.add_trace(BoxClass(y=arr))
    assert len(fig._scalable_traces) == 1 and len(fig.data) == 1
    assert fig.data[0].x is None and fig.data[0].y is None
    trace_data = fig._construct_update_data({}, force_update=True)[1:]
    assert len(trace_data) == 1
    assert trace_data[0]["orientation"] == "v"
    assert trace_data[0]["lowerfence"] == [0]
    assert trace_data[0]["upperfence"] == [DATA_LENGTH - 1]
    assert trace_data[0]["median"] == [(DATA_LENGTH - 1) / 2]


# When utilizing the ScalableFigure, the data should be converted to polars
@pytest.mark.parametrize("data", _generate_data(only_polars_lazy=False))
def test_box_scalable_figure_data(data):
    """Test the ScalableFigure with ScalableBox.

    The x and y arguments are keys (strings) of the data (DataFrame or LazyFrame).
    """
    # Case 1: passing x
    fig = ScalableFigure(backend_data=data)
    fig.add_trace(ScalableBox(x="arr"))
    assert len(fig._scalable_traces) == 1 and len(fig.data) == 1
    assert fig.data[0].x is None and fig.data[0].y is None
    trace_data = fig._construct_update_data({}, force_update=True)[1:]
    assert len(trace_data) == 1
    assert trace_data[0]["orientation"] == "h"
    assert trace_data[0]["lowerfence"] == [0]
    assert trace_data[0]["upperfence"] == [DATA_LENGTH - 1]
    assert trace_data[0]["median"] == [(DATA_LENGTH - 1) / 2]
    # Case 2: passing y
    fig = ScalableFigure(backend_data=data)
    fig.add_trace(ScalableBox(y="arr"))
    assert len(fig._scalable_traces) == 1 and len(fig.data) == 1
    assert fig.data[0].x is None and fig.data[0].y is None
    trace_data = fig._construct_update_data({}, force_update=True)[1:]
    assert len(trace_data) == 1
    assert trace_data[0]["index"] == 0
    assert trace_data[0]["orientation"] == "v"
    assert trace_data[0]["lowerfence"] == [0]
    assert trace_data[0]["upperfence"] == [DATA_LENGTH - 1]
    assert trace_data[0]["median"] == [(DATA_LENGTH - 1) / 2]


def test_box_scalable_figure_mixed_data():
    """Test the ScalableFigure with ScalableBox.

    The x and y arguments are mixed (arrays and keys of the data).
    """
    # Case 1: passing x
    fig = ScalableFigure(backend_data=pl.LazyFrame({"arr": ARR}))
    fig.add_trace(ScalableBox(x=ARR))
    fig.add_trace(ScalableBox(x="arr"))
    fig.add_trace(go.Box(x=ARR))
    assert len(fig._scalable_traces) == 3 and len(fig.data) == 3
    assert all(trace.x is None and trace.y is None for trace in fig.data)
    trace_data = fig._construct_update_data({}, force_update=True)[1:]
    assert len(trace_data) == 3
    for idx, trace_data in enumerate(trace_data):
        assert trace_data["index"] == idx
        assert trace_data["orientation"] == "h"
        assert trace_data["lowerfence"] == [0]
        assert trace_data["upperfence"] == [DATA_LENGTH - 1]
        assert trace_data["median"] == [(DATA_LENGTH - 1) / 2]
    # Case 2: passing y
    fig = ScalableFigure(backend_data=pl.LazyFrame({"arr": ARR}))
    fig.add_trace(ScalableBox(y=ARR))
    fig.add_trace(ScalableBox(y="arr"))
    fig.add_trace(go.Box(y=ARR))
    assert len(fig._scalable_traces) == 3 and len(fig.data) == 3
    assert all(trace.x is None and trace.y is None for trace in fig.data)
    trace_data = fig._construct_update_data({}, force_update=True)[1:]
    assert len(trace_data) == 3
    for idx, trace_data in enumerate(trace_data):
        assert trace_data["index"] == idx
        assert trace_data["orientation"] == "v"
        assert trace_data["lowerfence"] == [0]
        assert trace_data["upperfence"] == [DATA_LENGTH - 1]
        assert trace_data["median"] == [(DATA_LENGTH - 1) / 2]
