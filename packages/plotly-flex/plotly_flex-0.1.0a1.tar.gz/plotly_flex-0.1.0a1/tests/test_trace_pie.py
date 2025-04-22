import pytest

import plotly.graph_objects as go
import numpy as np
import pandas as pd
import polars as pl
import pyarrow as pa

from plotly_flex import ScalableFigure
from plotly_flex.trace import ScalablePie

from .utils import get_trace_update

DATA_LENGTH = 200

LABELS = list(range(DATA_LENGTH))
VALUES = [i**0.5 for i in range(DATA_LENGTH)]


def _generate_labels():
    arr = LABELS.copy()
    return [
        arr,
        np.array(arr),
        pd.Series(arr),
        pd.Series(arr).index,
        pd.Series(arr).values,
        pl.Series("x", arr),
    ]


def _generate_values():
    arr = VALUES.copy()
    return [
        arr,
        np.array(arr),
        pd.Series(arr),
        pd.Series(arr).values,
        pl.Series("y", arr),
    ]


def _generate_data(only_polars_lazy: bool):
    labels, values = LABELS.copy(), VALUES.copy()
    data_list = [pl.LazyFrame({"labels": labels, "values": values})]
    if not only_polars_lazy:
        data_list += [
            pl.DataFrame({"labels": labels, "values": values}),
            pd.DataFrame({"labels": labels, "values": values}),
            pa.Table.from_pydict(
                {"labels": pa.array(labels), "values": pa.array(values)}
            ),
        ]
    return data_list


@pytest.mark.parametrize("labels", _generate_labels())
@pytest.mark.parametrize("values", _generate_values())
def test_pie_labels_values_materialized(labels, values):
    """Test the aggregate_data method of ScalablePie.

    The labels and values arguments are materialized (arrays or series).
    """
    trace = ScalablePie(labels=labels, values=values, uid="some_uid")
    assert trace.labels is None and trace.values is None
    trace_data = get_trace_update(trace, None, {})
    assert np.allclose(trace_data["labels"], LABELS)
    assert np.allclose(trace_data["values"], VALUES)


# ScalablePie aggregate_data method is not implemented for non-polars data
@pytest.mark.parametrize("data", _generate_data(only_polars_lazy=True))
def test_pie_data(data):
    """Test the aggregate_data method of ScalablePie.

    The labels and values arguments are keys (strings) of the data (DataFrame or
    LazyFrame).
    """
    trace = ScalablePie(labels="labels", values="values", uid="some_uid")
    assert trace.labels is None and trace.values is None
    trace_data = get_trace_update(trace, data, {})
    assert np.allclose(trace_data["labels"], LABELS)
    assert np.allclose(trace_data["values"], VALUES)


@pytest.mark.parametrize("labels", _generate_labels())
@pytest.mark.parametrize("values", _generate_values())
@pytest.mark.parametrize("PieClass", [go.Pie, ScalablePie])
def test_pie_scalable_figure_labels_values_materialized(labels, values, PieClass):
    """Test the ScalableFigure with ScalablePie.

    The labels and values arguments are materialized (arrays or series).
    """
    fig = ScalableFigure()
    fig.add_trace(PieClass(labels=labels, values=values))
    assert len(fig._scalable_traces) == 1 and len(fig.data) == 1
    assert fig.data[0].labels is None and fig.data[0].values is None
    trace_data = fig._construct_update_data({}, force_update=True)[1:]
    assert len(trace_data) == 1
    assert trace_data[0]["index"] == 0
    assert np.allclose(trace_data[0]["labels"], LABELS)
    assert np.allclose(trace_data[0]["values"], VALUES)


# When utilizing the ScalableFigure, the data should be converted to polars
@pytest.mark.parametrize("data", _generate_data(only_polars_lazy=False))
def test_pie_scalable_figure_data(data):
    """Test the ScalableFigure with ScalablePie.

    The labels and values arguments are keys (strings) of the data (DataFrame or
    LazyFrame).
    """
    fig = ScalableFigure(backend_data=data)
    fig.add_trace(ScalablePie(labels="labels", values="values"))
    assert len(fig._scalable_traces) == 1 and len(fig.data) == 1
    assert fig.data[0].labels is None and fig.data[0].values is None
    trace_data = fig._construct_update_data({}, force_update=True)[1:]
    assert len(trace_data) == 1
    assert trace_data[0]["index"] == 0
    assert np.allclose(trace_data[0]["labels"], LABELS)
    assert np.allclose(trace_data[0]["values"], VALUES)


def test_pie_scalable_figure_mixed_data():
    """Test the ScalableFigure with ScalablePie.

    The labels and values arguments are mixed (materialized and keys of the data).
    """
    fig = ScalableFigure(
        backend_data=pl.LazyFrame({"labels": LABELS, "values": VALUES})
    )
    fig.add_trace(ScalablePie(labels=LABELS, values=VALUES))
    fig.add_trace(ScalablePie(labels="labels", values="values"))
    fig.add_trace(go.Pie(labels=LABELS, values=VALUES))
    assert len(fig._scalable_traces) == 3 and len(fig.data) == 3
    assert all(trace.labels is None and trace.values is None for trace in fig.data)
    trace_data = fig._construct_update_data({}, force_update=True)[1:]
    assert len(trace_data) == 3
    for idx, trace_data in enumerate(trace_data):
        assert trace_data["index"] == idx
        assert np.allclose(trace_data["labels"], LABELS)
        assert np.allclose(trace_data["values"], VALUES)
