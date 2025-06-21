"""Helper functions for matplotlib."""

from typing import Literal, cast

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from numpy.typing import NDArray


def cm_to_inches(cm: float) -> float:
    """Convert centimeters to inches.
    
    Args:
        cm: The value in centimeters.
    """
    return cm / 2.54

def inches_to_cm(inch: float) -> float:
    """Convert inches to centimeters.
    
    Args:
        inch: The value in inches.
    """
    return inch * 2.54

def cm_to_pt(cm: float) -> float:
    """Convert centimeters to points.
    
    Args:
        cm: The value in centimeters.
    """
    return cm_to_inches(cm) * 72

def pt_to_cm(pt: float) -> float:
    """Convert points to centimeters.

    A point is 1/72 of an inch.

    Args:
        pt: The value in points.

    Returns:
        The value in centimeters.
    """
    return inches_to_cm(pt / 72)


def cm_to_rel(fig: Figure, cm: float, dim: Literal["width", "height"]) -> float:
    """Convert centimeters to relative coordinates.
    
    This is a simple conversion factor.

    Args:
        fig: The figure to convert the coordinates for.
        cm: The value in centimeters.
        dim: The dimension to convert to relative coordinates.

    Returns:
        The value in relative coordinates.
    """
    if dim == "width":
        return cm_to_inches(cm) / float(fig.get_size_inches()[0])
    elif dim == "height":
        return cm_to_inches(cm) / float(fig.get_size_inches()[1])
    else:
        raise ValueError(f"Invalid dimension: {dim}")
    
def rel_to_cm(fig: Figure, rel: float, dim: Literal["width", "height"]) -> float:
    """Convert relative coordinates to centimeters.
    
    Args:
        fig: The figure to convert the coordinates for.
        rel: The value in relative coordinates.
        dim: The dimension to convert to centimeters.   

    Returns:
        The value in centimeters.
    """
    if dim == "width":
        return inches_to_cm(rel * float(fig.get_size_inches()[0]))
    elif dim == "height":
        return inches_to_cm(rel * float(fig.get_size_inches()[1]))
    else:
        raise ValueError(f"Invalid dimension: {dim}")

def get_default_colors() -> list[str]:
    """Return the default Matplotlib colors in hex or named format.

    Retrieves the list of default colors used in Matplotlib's property cycle.

    Returns:
        list[str]: A list of color hex codes or named color strings.
    """
    prop_cycle = plt.rcParams["axes.prop_cycle"]
    colors = cast(list[str], prop_cycle.by_key().get("color", []))
    return colors

def get_pastel_colors() -> NDArray[np.float64]:
    """Return a list of 8 pastel colors from the 'Pastel2' colormap.

    Uses Matplotlib's 'Pastel2' colormap to generate 8 RGBA color values.

    Returns:
        NDArray[np.float64]: An array of shape (8, 4), where each row is an
        RGBA color with float64 components.
    """
    cmap = plt.get_cmap("Pastel2")
    colors: NDArray[np.float64] = cmap(np.arange(8))
    return colors

def create_full_figure_axes(fig: Figure) -> Axes:
    """Create an invisible axes covering the entire figure.

    This axes is used to draw or annotate anywhere in the figure using relative
    coordinates.

    Args:
        fig: Figure to add the axes to.

    Returns:
        The created axes.
    """

    ax = fig.add_axes((0.0, 0.0, 1.0, 1.0), facecolor="none", zorder=-1)
    ax.axis("off")
    ax.set(xlim=[0, 1], ylim=[0, 1])
    return ax

def move_yaxis_right(ax: Axes) -> None:
    """Move the y-axis of the given Axes object to the right side.

    This function updates tick marks, label position, and spine visibility to move
    the y-axis from the left to the right of the plot.

    Args:
        ax (Axes): The matplotlib Axes object to modify.

    Returns:
        None
    """
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position("right")
    ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(True)
