"""Figure creation and management."""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure as MatplotlibFigure

from ..panel_config import PanelConfig


class FigureManager:
    """Manages figure creation for panels."""

    def __init__(self, config: PanelConfig):
        """Initialize figure manager.
        
        Args:
            config: Panel configuration object.
        """
        self.config = config

    def create_fig(self) -> MatplotlibFigure:
        """Creates a matplotlib figure with the specified size.

        Returns:
            MatplotlibFigure: The created figure object.
        """
        # Get dimensions from config and convert to inches
        dims = self.config.panel_dimensions
        fig_width_in = dims.width_cm / 2.54
        fig_height_in = dims.height_cm / 2.54
        
        # Create the figure
        fig = plt.figure(figsize=(fig_width_in, fig_height_in))
        return fig
    
    def draw_debug_lines(self, fig: MatplotlibFigure) -> None:
        """Draw debug grid lines if enabled in the configuration.
        
        Args:
            fig: The matplotlib figure to draw debug lines on.
        """
        if not self.config.debug_panel.show:
            return
        
        # Create a transparent axes covering the entire figure
        ax = fig.add_axes(
            (0.0, 0.0, 1.0, 1.0), 
            frameon=False, 
            aspect="auto", 
            facecolor="none",
            zorder=-10
        )
        
        # Set the axes limits to the figure dimensions from the config
        fig_width_cm = self.config.panel_dimensions.width_cm
        fig_height_cm = self.config.panel_dimensions.height_cm
        ax.set_xlim(0, fig_width_cm)
        ax.set_ylim(0, fig_height_cm)
        
        # Draw gridlines at every grid_resolution_cm cm
        delta = self.config.debug_panel.grid_resolution_cm
        ax.set_xticks(np.arange(0, fig_width_cm, delta))
        ax.set_yticks(np.arange(0, fig_height_cm, delta))
        ax.grid(True, linestyle=":", alpha=1)

        # Hide spines
        for spine in ax.spines.values():
            spine.set_visible(False)

        # Hide tick marks
        ax.tick_params(left=False, bottom=False)

        # Hide tick labels
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        