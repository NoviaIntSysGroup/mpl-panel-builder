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

import yaml
from matplotlib.axes import Axes

# Add the project root to sys.path to allow importing helpers module
sys.path.append(str(Path(__file__).parent.parent.parent.absolute()))
from examples.helpers import get_logger, get_project_root
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


# Example specific helper functions
def _plot_fun(ax: Axes) -> None:
    """Plot a simple function.

    Args:
        ax: Axes to plot the sinusoid on.
    """

    x = [0, 4]
    y = x
    ax.plot(x, y, label="$y=x$")
    ax.set(xlim=[0, 4], ylim=[0, 4])

class DebugPanel(PanelBuilder):
    # Required class attributes
    _panel_name = "debug_panel"
    _n_rows = 2
    _n_cols = 2

    def build_panel(self) -> None:

        ax = self.axs[0][0]
        _plot_fun(ax)
        ax.set(
            xticks=[],
            yticks=[],
        )
        self.draw_scale_bar(ax, 1, "1 cm", "y")
        
        ax = self.axs[0][1]
        _plot_fun(ax)
        ax.set(
            xticks=[],
            yticks=[],
        )

        ax = self.axs[1][0]
        _plot_fun(ax)
        ax.set(
            xlabel="X axis (cm)",
            ylabel="Y axis (cm)",
            xticks=[0, 1, 2, 3, 4],
            yticks=[0, 1, 2, 3, 4],
        )

        ax = self.axs[1][1]
        _plot_fun(ax)
        ax.set(
            xticks=[],
            yticks=[],
        )
        self.draw_scale_bar(ax, 1, "1 cm", "x")

if __name__ == "__main__":
    logger.info("Creating panel with class: %s", DebugPanel.__name__)
    builder = DebugPanel(config)
    fig = builder()
    logger.info("Panel created and saved to %s", config["panel_output"]["directory"])
    