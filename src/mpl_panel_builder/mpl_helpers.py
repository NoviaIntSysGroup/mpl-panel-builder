"""Helper functions for matplotlib."""

from typing import cast

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from numpy.typing import NDArray


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
