"""This example shows how to use and visually debug all the features.

The script utilizes the debug feature to draw a grid with fixed spacing over the
entire figure. This is useful for quickly checking that each element is placed
correctly. This panel utilizes the grid to debug and verify that att PanelBuilder
features (methods) work as intended. 

The script defines the following subclass of :class:`PanelBuilder`:
- DebugPanel: 2 by 2 panel with a simple plot
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Literal

import numpy as np
import yaml
from matplotlib.axes import Axes
from matplotlib.cm import ScalarMappable

# Add the project root to sys.path to allow importing helpers module
sys.path.append(str(Path(__file__).parent.parent.parent.absolute()))
from examples.helpers import get_logger, get_project_root
from mpl_panel_builder.mpl_helpers import adjust_axes_size
from mpl_panel_builder.panel_builder import PanelBuilder

logger = get_logger(__name__)

# Define panel configuration
project_root = get_project_root()
current_dir = Path(__file__).parent
example_name = current_dir.name

# Load the configuration
with open(current_dir / "config.yaml") as file:
    config = yaml.safe_load(file)["figures"]

# Correct the panel output directory
config["panel_output"]["directory"] = project_root / "outputs" / example_name / "panels"
# Create the output directory if it doesn't exist
config["panel_output"]["directory"].mkdir(parents=True, exist_ok=True)


def _get_xy_data() -> tuple[np.ndarray, np.ndarray]:
    """Generate x and y data for plotting.
    
    Returns:
        A tuple containing (x, y) arrays where x is a linear space from 0 to 4
        with 101 points, and y equals x.
    """
    x = np.linspace(0, 4, 101)
    y = x
    return x, y

# Example specific helper functions
def _plot_fun(ax: Axes, color: tuple[float, float, float] = (0, 0, 0)) -> None:
    """Plot a simple function.

    Args:
        ax: Axes to plot on.
        color: Color of the plot line. Defaults to black.
    """

    x, y = _get_xy_data()
    ax.plot(x, y, label="$y=x$", color=color)
    ax.set(xlim=[x.min(), x.max()], ylim=[y.min(), y.max()])

# Example specific helper functions
def _scatter_fun(ax: Axes) -> ScalarMappable:
    """Plot a simple scatter plot.

    Args:
        ax: Axes to plot the scatter plot on.

    Returns:
        The scatter plot object (ScalarMappable) for colorbar creation.
    """

    x, y = _get_xy_data()
    scatter = ax.scatter(x, y, 10, y, label="$y=x$")
    ax.set(xlim=[x.min(), x.max()], ylim=[y.min(), y.max()])
    return scatter

class DebugPanel(PanelBuilder):
    # Required class attributes
    _panel_name = "debug_panel"
    _n_rows = 2
    _n_cols = 2

    def build_panel(self) -> None:

        # Top left
        ax = self.axs[0][0]
        _plot_fun(ax, color=self.config.colors.color_1)
        ax.set(
            xticks=[],
            yticks=[],
        )
        # Test y scale bar
        self.draw_y_scale_bar(ax, 1, "1 cm")
        # Test description
        self.draw_description(ax, "NW", loc="northwest", bg_color="lightgrey")
        self.draw_description(ax, "NE", loc="northeast", bg_color="lightgrey")
        self.draw_description(ax, "SW", loc="southwest", bg_color="lightgrey")
        self.draw_description(ax, "SE", loc="southeast", bg_color="lightgrey")

        # Top right
        ax = self.axs[0][1]
        scatter = _scatter_fun(ax)
        ax.set(
            xticks=[],
            yticks=[],
        )
        # Test colorbar functionality
        positions: list[Literal['left', 'right', 'top', 'bottom']] = [
            'left', 'right', 'top', 'bottom'
        ]
        for pos in positions:
            adjust_axes_size(ax, 1, pos)
        for pos in positions:
            cbar = self.add_colorbar(scatter, ax, pos, shrink_axes=False)
            # Remove colorbar outline
            cbar.outline.set_visible(False) # type: ignore
            # Remove tick lines
            cbar.ax.tick_params(length=0)

        # Bottom left
        ax = self.axs[1][0]
        _plot_fun(ax, color=self.config.colors.color_2)
        ax.set(
            xlabel="X axis (cm)",
            ylabel="Y axis (cm)",
            xticks=[0, 1, 2, 3, 4],
            yticks=[0, 1, 2, 3, 4],
        )

        # Bottom right
        ax = self.axs[1][1]
        _plot_fun(ax, color=self.config.colors.color_3)
        ax.set(
            xticks=[],
            yticks=[],
        )
        # Test x scale bar
        self.draw_x_scale_bar(ax, 1, "1 cm")

if __name__ == "__main__":
    logger.info("Creating panel with class: %s", DebugPanel.__name__)
    builder = DebugPanel(config)
    fig = builder()
    logger.info("Panel created and saved to %s", config["panel_output"]["directory"])
    
