from plotly.basedatatypes import BaseFigure

try:  # Fails when anywidget is not installed
    from plotly.basewidget import BaseFigureWidget
except (ImportError, ModuleNotFoundError):
    BaseFigureWidget = type(None)

from typing import Any

### Checks for the figure type


def is_figure(figure: Any) -> bool:
    """Check if the figure is a plotly go.Figure or a ScalableFigure.

    !!! note

        This method does not use isinstance(figure, go.Figure) as this will not work
        when go.Figure is decorated (after executing the
        ``register_plotly_resampler`` function).

    Parameters
    ----------
    figure : Any
        The figure to check.

    Returns
    -------
    bool
        True if the figure is a plotly go.Figure or a ScalableFigure.
    """
    return isinstance(figure, BaseFigure) and (not isinstance(figure, BaseFigureWidget))


def is_scalable_figure(figure: Any) -> bool:
    """Check if the figure is a ScalableFigure.

    !!! note

        This method will not return True if the figure is a plotly go.Figure.

    Parameters
    ----------
    figure : Any
        The figure to check.

    Returns
    -------
    bool
        True if the figure is a ScalableFigure.
    """
    from plotly_flex import ScalableFigure

    return isinstance(figure, ScalableFigure)
