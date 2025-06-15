from pathlib import Path
from typing import Any, Literal

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes as MatplotlibAxes
from matplotlib.figure import Figure as MatplotlibFigure

from mpl_panel_builder.panel_builder_config import PanelBuilderConfig


class PanelBuilder:
    """Base class for constructing matplotlib panels with consistent layout.

    This class provides a framework for creating publication-quality figure panels
    with precise sizing in centimeters, consistent margins, and customizable styling.
    Subclasses must define n_rows and n_cols class attributes.

    Attributes:
        config (PanelConfig): Configuration object containing panel dimensions,
            margins, font sizes, and axis separation settings.
        debug (bool): Whether to draw debug grid lines for layout assistance.
        panel_name (str): Name of the panel to use for saving the figure.
        n_rows (int): Number of subplot rows defined by the user.
        n_cols (int): Number of subplot columns defined by the user.
        fig (Optional[MatplotlibFigure]): Created matplotlib figure object.
        axs_grid (Optional[List[List[MatplotlibAxes]]]): Grid of axes objects.
    """

    def __init__(self, config: dict[str, Any], debug: bool = False):
        """Initializes the PanelBuilder with config and grid layout.

        Args:
            config (Dict[str, Any]): Layout and styling configuration.
            debug (bool, optional): Whether to draw debug grid lines. 
                Defaults to False.
        """
        self.config = PanelBuilderConfig.from_dict(config)
        self.debug = debug
        self.panel_name: str = type(self).panel_name
        self.n_rows: int = type(self).n_rows
        self.n_cols: int = type(self).n_cols

        self._fig: MatplotlibFigure | None = None
        self._axs_grid: list[list[MatplotlibAxes]] | None = None

    def __init_subclass__(cls) -> None:
        """Validates that subclasses define required class attributes.
        
        This method ensures that any class inheriting from PanelBuilder properly
        defines the required panel_name, n_rows and n_cols class attributes that
        specify the panel grid dimensions.
        
        Args:
            cls: The class being defined that inherits from PanelBuilder.
            
        Raises:
            TypeError: If the subclass does not define panel_name, n_rows or
                n_cols.
        """
        super().__init_subclass__()
        required_attrs = ["panel_name", "n_rows", "n_cols"]
        missing = [attr for attr in required_attrs if not hasattr(cls, attr)]
        if missing:
            raise TypeError(
                "Subclasses of PanelBuilder must define class attributes: "
                + ", ".join(missing)
            )

    def __call__(self, *args: Any, **kwargs: Any) -> MatplotlibFigure:
        """Initializes and builds the panel, returning the resulting figure.

        Any positional and keyword arguments are forwarded to
        :meth:`build_panel`. If :meth:`build_panel` returns a string, it is
        treated as a filename *suffix* appended to :pyattr:`panel_name` when the
        panel is saved. Returning ``None`` keeps the default filename.

        Returns:
            MatplotlibFigure: The constructed matplotlib figure.
        """
        style_context = self.get_default_style_rc()
        with plt.rc_context(rc=style_context):
            self._fig = self.create_fig()
            self.draw_debug_lines()
            self._axs_grid = self.create_axes()
            filename_suffix = self.build_panel(*args, **kwargs)
            self.save_fig(filename_suffix if isinstance(filename_suffix, str) else None)
        return self.fig

    def build_panel(self, *args: Any, **kwargs: Any) -> Any:
        """Populates the panel with plot content.

        Subclasses should implement their plotting logic here.  The return value
        may optionally be a string which will be appended to
        :pyattr:`panel_name` when the panel is saved.  Any positional and
        keyword arguments passed to :py:meth:`__call__` are forwarded to this
        method.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement build_panel() method")

    def get_default_style_rc(self) -> dict[str, Any]:
        """Returns a style dictionary (rcParams) for use in rc_context.

        This method constructs Matplotlib style settings based on the config
        for font sizes and visual aesthetics for article-style figures.

        Returns:
            Dict[str, Any]: A style dictionary for matplotlib.rc_context, or empty 
                dict if font sizes are not defined in config.
        """
        axes_font_size = self.config.font_sizes_pt.axes
        text_font_size = self.config.font_sizes_pt.text

        return {

            # Figure appearance
            "figure.facecolor": "white",

            # Axes appearance
            "axes.facecolor": "none",
            "axes.spines.right": False,
            "axes.spines.top": False,
            "axes.titlepad": 4,

            # Font sizes
            "font.size": text_font_size,
            "axes.titlesize": axes_font_size,
            "axes.labelsize": axes_font_size,
            "xtick.labelsize": axes_font_size,
            "ytick.labelsize": axes_font_size,
            "figure.titlesize": axes_font_size,
            "legend.fontsize": text_font_size,

            # Line styles
            "lines.linewidth": 1,
            "lines.markersize": 4,

            # Legend appearance
            "legend.frameon": True,
            "legend.framealpha": 0.6,
            "legend.edgecolor": (1, 1, 1, 0.5),
            "legend.handlelength": 1.0,
            "legend.handletextpad": 0.7,
            "legend.labelspacing": 0.4,
            "legend.columnspacing": 1.0,
        }

    def create_fig(self) -> MatplotlibFigure:
        """Creates a matplotlib figure with the specified size.

        Returns:
            MatplotlibFigure: The created figure object.
        """
        # Get dimensions from config and convert to inches
        dims = self.config.panel_dimensions_cm
        fig_width_in = dims.width / 2.54
        fig_height_in = dims.height / 2.54
        
        # Create the figure
        fig = plt.figure(figsize=(fig_width_in, fig_height_in))
        return fig

    def create_axes(self) -> list[list[MatplotlibAxes]]:
        """Creates the grid of axes based on layout configuration.

        Returns:
            List[List[MatplotlibAxes]]: Grid of axes.
        """
        num_rows, num_cols = self.n_rows, self.n_cols
        
        # Get figure dimensions in cm
        fig_width_cm = self.config.panel_dimensions_cm.width
        fig_height_cm = self.config.panel_dimensions_cm.height
        
        # Get margins from config and calculate the plot region in relative coordinates
        margins = self.config.panel_margins_cm
        plot_left = margins.left / fig_width_cm
        plot_bottom = margins.bottom / fig_height_cm
        plot_width = (fig_width_cm - margins.left - margins.right) / fig_width_cm
        plot_height = (fig_height_cm - margins.top - margins.bottom) / fig_height_cm
        
        # Convert separation to relative coordinates
        sep_x_rel = self.config.ax_separation_cm.x / fig_width_cm
        sep_y_rel = self.config.ax_separation_cm.y / fig_height_cm

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
        axs_grid: list[list[MatplotlibAxes]] = []
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

                ax = self.fig.add_axes(ax_pos, aspect="auto")
                row_axes.append(ax)

            axs_grid.append(row_axes)

        return axs_grid
    
    def draw_debug_lines(self) -> None:
        """Draws debug lines on the axes to help with layout debugging.
        
        If debug is False, this method does nothing.
        """
        if not self.debug:
            return
        
        # Create a transparent axes covering the entire figure
        fig = self.fig
        ax = fig.add_axes(
            (0.0, 0.0, 1.0, 1.0), 
            frameon=False, 
            aspect="auto", 
            facecolor="none"
        )
        
        # Set the axes limits to the figure dimensions from the config
        fig_width_cm = self.config.panel_dimensions_cm.width
        fig_height_cm = self.config.panel_dimensions_cm.height
        ax.set_xlim(0, fig_width_cm)
        ax.set_ylim(0, fig_height_cm)
        
        # Draw gridlines at every 0.5 cm
        delta = 0.5
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

    def cm_to_rel(self, cm: float, dim: Literal["width", "height"]) -> float:
        """Converts a length in cm to a relative coordinate.
        
        Args:
            cm (float): The length in cm.
            dim (Literal["width", "height"]): The dimension to 
                convert to relative coordinates.

        Returns:
            float: The relative coordinate.
        """
        if dim == "width":
            return cm / self.config.panel_dimensions_cm.width
        elif dim == "height":
            return cm / self.config.panel_dimensions_cm.height
        else:
            raise ValueError(f"Invalid dimension: {dim}")
        
    def save_fig(self, filename_suffix: str | None = None) -> None:
        """Saves the figure to the output directory.

        Args:
            filename_suffix: Optional string to append to
                :pyattr:`panel_name` when naming the saved file.
        """
        # Check if output directory is set
        # TODO: Add logging to inform the user that the figure has been saved
        if self.config.panel_output.directory:

            # Check if the directory exists
            directory = Path(self.config.panel_output.directory)
            if not directory.exists():
                raise ValueError(f"Output directory does not exist: {directory}")

            # Save the figure
            file_format = self.config.panel_output.format
            dpi = self.config.panel_output.dpi
            panel_name = self.panel_name
            if filename_suffix:
                panel_name = f"{panel_name}_{filename_suffix}"
            self.fig.savefig(directory / f"{panel_name}.{file_format}", dpi=dpi)
        

    @property
    def fig(self) -> MatplotlibFigure:
        """matplotlib.figure.Figure: The figure object, guaranteed to be initialized.

        Raises:
            RuntimeError: If the figure has not been created yet.
        """
        if self._fig is None:
            raise RuntimeError("Figure has not been created yet.")
        return self._fig

    @property
    def axs_grid(self) -> list[list[MatplotlibAxes]]:
        """List[List[matplotlib.axes.Axes]]: The grid of axes, guaranteed to exist.

        Raises:
            RuntimeError: If the axes grid has not been created yet.
        """
        if self._axs_grid is None:
            raise RuntimeError("Axes grid has not been created yet.")
        return self._axs_grid