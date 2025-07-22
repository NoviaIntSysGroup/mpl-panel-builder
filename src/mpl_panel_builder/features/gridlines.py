"""Debug gridlines functionality."""

import numpy as np
from matplotlib.figure import Figure

from ..config import get_config


def draw_gridlines(fig: Figure) -> None:
    """Draw debug gridlines on figure.
    
    Args:
        fig: Matplotlib figure to draw gridlines on
    """
    config = get_config()
    gridlines_config = config['features']['gridlines']
    
    # Create a transparent axes covering the entire figure
    ax = fig.add_axes(
        (0.0, 0.0, 1.0, 1.0), 
        frameon=False, 
        aspect="auto", 
        facecolor="none",
        zorder=-10
    )
    
    # Set the axes limits to the figure dimensions from the config
    fig_width_cm = config['panel']['dimensions']['width_cm']
    fig_height_cm = config['panel']['dimensions']['height_cm']
    ax.set_xlim(0, fig_width_cm)
    ax.set_ylim(0, fig_height_cm)
    
    # Draw gridlines at every resolution_cm cm
    delta = gridlines_config['resolution_cm']
    ax.set_xticks(np.arange(0, fig_width_cm, delta))
    ax.set_yticks(np.arange(0, fig_height_cm, delta))
    ax.grid(True, linestyle=":", color='gray', linewidth=0.5, alpha=1)

    # Hide spines
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Hide tick marks
    ax.tick_params(left=False, bottom=False)

    # Hide tick labels
    ax.set_xticklabels([])
    ax.set_yticklabels([])