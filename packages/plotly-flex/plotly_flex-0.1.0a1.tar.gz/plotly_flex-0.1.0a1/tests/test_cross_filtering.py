import pytest
import polars as pl
import numpy as np

from plotly.subplots import make_subplots
from plotly_flex import ScalableFigure
from plotly_flex.trace import ScalableScatter1D, ScalableHistogram, ScalableBar


# Helper function to create sample data
def create_test_data(n=100):
    return pl.LazyFrame(
        {
            "x": np.arange(n),
            "y": np.random.rand(n) * 10,
            "category": np.random.choice(["A", "B", "C"], n),
            "value": np.random.randint(1, 10, n),
        }
    )


# Helper to set up a figure with traces for cross-filtering
# Returns (fig, trace_names)
def setup_crossfilter_figure(traces, data):
    fig = ScalableFigure(
        make_subplots(rows=1, cols=len(traces)), backend_data=data, verbose=False
    )
    trace_indices = []
    for idx, (trace, row, col) in enumerate(traces):
        fig.add_trace(trace, row=row, col=col)
        trace_indices.append(idx)
    return fig, trace_indices


# Parameterized cross-filtering test
@pytest.mark.parametrize(
    "traces, selection_relayout, expected_update_idx",
    [
        # Scatter select -> Histogram update
        (
            [
                (ScalableScatter1D(x="x", y="y", name="Scatter"), 1, 1),
                (ScalableHistogram(x="y", name="Histogram"), 1, 2),
            ],
            {
                "selections": [
                    {
                        "type": "rect",
                        "xref": "x",
                        "yref": "y",
                        "x0": 100.5,
                        "x1": 300.5,
                        "y0": -1,
                        "y1": 11,
                    }
                ]
            },
            1,
        ),
        # Histogram select -> Scatter update
        (
            [
                (ScalableScatter1D(x="x", y="y", name="Scatter"), 1, 1),
                (ScalableHistogram(x="y", name="Histogram"), 1, 2),
            ],
            {
                "selections": [
                    {
                        "type": "rect",
                        "xref": "x2",
                        "yref": "y2",
                        "x0": 2.1,
                        "x1": 4.9,
                        "y0": 0,
                        "y1": 100,
                    }
                ]
            },
            0,
        ),
        # Bar select -> Scatter update
        (
            [
                (ScalableScatter1D(x="x", y="y", name="Scatter"), 1, 1),
                (ScalableBar(x="x", y="value", name="Bar"), 1, 2),
            ],
            {
                "selections": [
                    {
                        "type": "rect",
                        "xref": "x2",
                        "yref": "y2",
                        "x0": 19.5,
                        "x1": 40.5,
                        "y0": 0,
                        "y1": 10,
                    }
                ]
            },
            0,
        ),
        # Selection outside data range (Scatter select -> Histogram update)
        (
            [
                (ScalableScatter1D(x="x", y="y", name="Scatter"), 1, 1),
                (ScalableHistogram(x="y", name="Histogram"), 1, 2),
            ],
            {
                "selections": [
                    {
                        "type": "rect",
                        "xref": "x",
                        "yref": "y",
                        "x0": 2000,
                        "x1": 3000,
                        "y0": -1,
                        "y1": 11,
                    }
                ]
            },
            1,
        ),
    ],
)
def test_cross_filtering_param(traces, selection_relayout, expected_update_idx):
    data = create_test_data(1000)
    fig, _ = setup_crossfilter_figure(traces, data)
    # Simulate initial load (force update)
    initial_update = fig._construct_update_data({}, force_update=True)
    assert len(initial_update) == len(traces) + 1
    # Simulate selection event
    filtered_update = fig._construct_update_data(selection_relayout)
    # Check that _front_end_selections is updated
    assert len(fig._front_end_selections) == len(selection_relayout["selections"])
    # Expecting update for the correct trace
    assert len(filtered_update) == 2  # relayout + 1 trace
    assert filtered_update[1]["index"] == expected_update_idx
    # Check that data is present
    assert any(k in filtered_update[1] for k in ("x", "labels"))
    assert any(k in filtered_update[1] for k in ("y", "values"))
    # If selection is outside range, y should be all zeros or empty for histogram
    if selection_relayout["selections"][0]["x0"] > 1000:
        if "y" in filtered_update[1] and len(filtered_update[1]["y"]) > 0:
            assert all(count == 0 for count in filtered_update[1]["y"])


# Test multiple selections (Scatter + Histogram -> Bar)
def test_multiple_selections_param():
    data = create_test_data(1000)
    traces = [
        (ScalableScatter1D(x="x", y="y", name="Scatter"), 1, 1),
        (ScalableHistogram(x="y", name="Histogram"), 1, 2),
        (ScalableBar(x="x", y="value", name="Bar"), 1, 3),
    ]
    fig, _ = setup_crossfilter_figure(traces, data)
    selection_relayout = {
        "selections": [
            {
                "type": "rect",
                "xref": "x",
                "yref": "y",
                "x0": 100.5,
                "x1": 300.5,
                "y0": -1,
                "y1": 11,
            },
            {
                "type": "rect",
                "xref": "x2",
                "yref": "y2",
                "x0": 2.1,
                "x1": 4.9,
                "y0": 0,
                "y1": 100,
            },
        ]
    }
    filtered_update = fig._construct_update_data(selection_relayout)
    assert len(fig._front_end_selections) == 2
    assert len(filtered_update) == 2  # relayout + 1 trace
    assert filtered_update[1]["index"] == 2  # Bar trace index
    assert any(k in filtered_update[1] for k in ("x", "labels"))
    assert any(k in filtered_update[1] for k in ("y", "values"))


# Test empty selection event (no active selection)
def test_empty_selection_event():
    data = create_test_data(1000)
    traces = [
        (ScalableScatter1D(x="x", y="y", name="Scatter"), 1, 1),
        (ScalableHistogram(x="y", name="Histogram"), 1, 2),
    ]
    fig, _ = setup_crossfilter_figure(traces, data)
    selection_relayout = {"selections": []}
    update = fig._construct_update_data(selection_relayout)
    assert len(update) == 1
    assert update[0] == selection_relayout
