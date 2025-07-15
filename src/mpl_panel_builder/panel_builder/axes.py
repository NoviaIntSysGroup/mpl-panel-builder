"""Axes management and layout."""

from matplotlib.axes import Axes as MatplotlibAxes
from matplotlib.figure import Figure as MatplotlibFigure

from ..panel_config import PanelConfig


class AxesManager:
    """Manages axes creation and layout for panels."""

    def __init__(self, config: PanelConfig):
        """Initialize axes manager.
        
        Args:
            config: Panel configuration object.
        """
        self.config = config

    def create_axes(
        self, fig: MatplotlibFigure, n_rows: int, n_cols: int
    ) -> list[list[MatplotlibAxes]]:
        """Creates the grid of axes based on layout configuration.

        Args:
            fig: The matplotlib figure to add axes to.
            n_rows: Number of rows in the axes grid.
            n_cols: Number of columns in the axes grid.

        Returns:
            List[List[MatplotlibAxes]]: Grid of axes.
        """
        num_rows, num_cols = n_rows, n_cols
        
        # Get figure dimensions in cm
        fig_width_cm = self.config.panel_dimensions.width_cm
        fig_height_cm = self.config.panel_dimensions.height_cm
        
        # Get margins from config and calculate the plot region in relative coordinates
        margins = self.config.panel_margins
        plot_left = margins.left_cm / fig_width_cm
        plot_bottom = margins.bottom_cm / fig_height_cm
        plot_width = (fig_width_cm - margins.left_cm - margins.right_cm) / fig_width_cm
        plot_height = (
            (fig_height_cm - margins.top_cm - margins.bottom_cm) / fig_height_cm
        )
        
        # Convert separation to relative coordinates
        sep_x_rel = self.config.axes_separation.x_cm / fig_width_cm
        sep_y_rel = self.config.axes_separation.y_cm / fig_height_cm

        # Calculate relative widths and heights
        rel_col_widths = (1.0 / num_cols,) * num_cols
        rel_row_heights = (1.0 / num_rows,) * num_rows

        # Calculate actual axes dimensions
        axes_widths_rel = [
            (plot_width - (num_cols - 1) * sep_x_rel) * w
            for w in rel_col_widths
        ]
        axes_heights_rel = [
            (plot_height - (num_rows - 1) * sep_y_rel) * h
            for h in rel_row_heights
        ]

        # Create the axes
        axs: list[list[MatplotlibAxes]] = []
        ax_x_left = plot_left  # left edge of plot region
        ax_y_top = plot_bottom + plot_height  # top edge of plot region

        for row in range(num_rows):
            row_axes = []

            # Calculate current row's vertical position
            ax_y = ax_y_top - sum(axes_heights_rel[:row]) - row * sep_y_rel

            for col in range(num_cols):
                # Calculate current column's horizontal position
                ax_x = ax_x_left + sum(axes_widths_rel[:col]) + col * sep_x_rel

                ax_pos = (
                    ax_x,
                    ax_y - axes_heights_rel[row],
                    axes_widths_rel[col],
                    axes_heights_rel[row],
                )

                ax = fig.add_axes(ax_pos, aspect="auto")
                row_axes.append(ax)

            axs.append(row_axes)

        return axs