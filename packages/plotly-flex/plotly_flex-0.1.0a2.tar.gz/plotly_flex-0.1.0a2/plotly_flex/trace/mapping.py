from plotly_flex import trace

_SCALABLE_TRACES = {
    "bar": trace.ScalableBar,
    "box": trace.ScalableBox,
    "pie": trace.ScalablePie,
    # TODO: we do not want to wrap these automatically because there are multiple scalable scatter options
    "scatter": trace.ScalableScatter1D,
    "scattergl": trace.ScalableScattergl1D,
    "histogram": trace.ScalableHistogram,
}
