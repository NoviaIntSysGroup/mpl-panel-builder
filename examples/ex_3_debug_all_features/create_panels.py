"""This example shows how to use and visually debug all the features using the
new function-based API.

The script utilizes the debug feature to draw a grid with fixed spacing over the
entire figure. This is useful for quickly checking that each element is placed
correctly. This panel utilizes the grid to debug and verify that all features
work as intended. 

The script demonstrates:
- DebugPanel: 2 by 2 panel with various features
- Scale bars, annotations, colorbars, and gridlines
"""

from pathlib import Path
from typing import Literal

import numpy as np
from matplotlib.axes import Axes
from matplotlib.cm import ScalarMappable

import mpl_panel_builder as mpb
from mpl_panel_builder.features import (
    add_annotation,
    add_colorbar,
    draw_gridlines,
    draw_x_scale_bar,
    draw_y_scale_bar,
)
from mpl_panel_builder.helpers import adjust_axes_size
from mpl_panel_builder.helpers.examples import get_logger, get_repo_root

# Simple setup
example_name = Path(__file__).parent.name
output_dir = get_repo_root() / "outputs" / example_name
output_dir.mkdir(parents=True, exist_ok=True)
current_dir = Path(__file__).parent
(output_dir / "panels").mkdir(parents=True, exist_ok=True)
logger = get_logger(example_name)

# Example specific helper functions
def _get_xy_data() -> tuple[np.ndarray, np.ndarray]:
    """Generate x and y data for plotting.
    
    Returns:
        A tuple containing (x, y) arrays where x is a linear space from 0 to 4
        with 101 points, and y equals x.
    """
    x = np.linspace(0, 4, 101)
    y = x
    return x, y

def _plot_fun(ax: Axes) -> None:
    """Plot a simple function.

    Args:
        ax: Axes to plot on.
    """
    x, y = _get_xy_data()
    ax.plot(x, y, label="$y=x$")
    ax.set(xlim=[x.min(), x.max()], ylim=[y.min(), y.max()])

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

# Create debug panel with all features
def create_debug_panel() -> None:
    """Create debug panel with all features."""
    
    # Create the panel
    logger.info("Creating debug panel...")
    import yaml
    with open(current_dir / "config.yaml") as f:
        config = yaml.safe_load(f)
    mpb.configure(config)
    mpb.set_rc_style()
    fig, axs = mpb.create_panel(rows=2, cols=2)
        
    # Top left
    ax = axs[0][0]
    _plot_fun(ax)
    ax.set(
        xticks=[],
        yticks=[],
    )
    # Test y scale bar
    draw_y_scale_bar(ax, 1, "1 cm")
    # Test annotation
    add_annotation(ax, "NW", loc="northwest", bg_color="lightgrey")
    add_annotation(ax, "NE", loc="northeast", bg_color="lightgrey")
    add_annotation(ax, "SW", loc="southwest", bg_color="lightgrey")
    add_annotation(ax, "SE", loc="southeast", bg_color="lightgrey")

    # Top right
    ax = axs[0][1]
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
        cbar = add_colorbar(ax, scatter, pos, shrink_axes=False)
        # Remove colorbar outline
        cbar.outline.set_visible(False) # type: ignore
        # Remove tick lines
        cbar.ax.tick_params(length=0)

    # Bottom left
    ax = axs[1][0]
    _plot_fun(ax)
    ax.set(
        xlabel="X axis (cm)",
        ylabel="Y axis (cm)",
        xticks=[0, 1, 2, 3, 4],
        yticks=[0, 1, 2, 3, 4],
    )

    # Bottom right
    ax = axs[1][1]
    _plot_fun(ax)
    ax.set(
        xticks=[],
        yticks=[],
    )
    # Test x scale bar
    draw_x_scale_bar(ax, 1, "1 cm")
    
    # Add debug gridlines
    draw_gridlines(fig)
    
    panel_path = output_dir / "panels" / "debug_panel"
    mpb.save_panel(fig, str(panel_path))
    logger.info(f"Debug panel saved to: {panel_path.with_suffix('.pdf').resolve()}")

if __name__ == "__main__":
    create_debug_panel()
    
