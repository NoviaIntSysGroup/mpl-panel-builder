import warnings
from pathlib import Path
from typing import Any, Literal

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes as MatplotlibAxes
from matplotlib.cm import ScalarMappable
from matplotlib.colorbar import Colorbar
from matplotlib.figure import Figure as MatplotlibFigure

from mpl_panel_builder import mpl_helpers
from mpl_panel_builder.panel_builder_config import PanelBuilderConfig


class PanelBuilder:
    """Base class for constructing matplotlib panels with consistent layout.

    This class provides a framework for creating publication-quality figure panels
    with precise sizing in centimeters, consistent margins, and customizable styling.
    Subclasses must define n_rows and n_cols class attributes.

    Attributes:
        config (PanelConfig): Configuration object containing panel dimensions,
            margins, font sizes, and axis separation settings.
        panel_name (str): Name of the panel to use for saving the figure.
        n_rows (int): Number of subplot rows defined by the user.
        n_cols (int): Number of subplot columns defined by the user.
        fig (Optional[MatplotlibFigure]): Created matplotlib figure object.
        axs (Optional[List[List[MatplotlibAxes]]]): Grid of axes objects.
    """

    # Private class attributes that must be defined by subclasses
    _panel_name: str
    _n_rows: int
    _n_cols: int

    def __init__(self, config: dict[str, Any]):
        """Initializes the PanelBuilder with config and grid layout.

        Args:
            config (Dict[str, Any]): Layout and styling configuration.
        """
        self.config = PanelBuilderConfig.from_dict(config)

        self._fig: MatplotlibFigure | None = None
        self._axs: list[list[MatplotlibAxes]] | None = None

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
        required_attrs = ["_panel_name", "_n_rows", "_n_cols"]
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
            self._axs = self.create_axes()
            filename_suffix = self.build_panel(*args, **kwargs)
            self.save_fig(filename_suffix)
        return self.fig

    def build_panel(self, *args: Any, **kwargs: Any) -> str | None:
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
        axes_font_size = self.config.font_sizes.axes_pt
        text_font_size = self.config.font_sizes.text_pt

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
            "lines.linewidth": self.config.line_style.line_width_pt,
            "lines.markersize": self.config.line_style.marker_size_pt,

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
        dims = self.config.panel_dimensions
        fig_width_in = dims.width_cm / 2.54
        fig_height_in = dims.height_cm / 2.54
        
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

                ax = self.fig.add_axes(ax_pos, aspect="auto")
                row_axes.append(ax)

            axs.append(row_axes)

        return axs
    
    def draw_scale_bar(
        self, 
        ax: MatplotlibAxes, 
        length: float, 
        label: str, 
        direction: Literal["x", "y"]
    ) -> None:
        """Draws a scale bar for the given axes.

        The scale bar is drawn on a new axes covering the entire figure. This 
        makes it possible to draw the scale bar on inside or outside of the axes.

        Args:
            ax: The axes to draw the scale bar for.
            length: The length of the scale bar in axes units.
            label: The label to display next to the scale bar.
            direction: The direction of the scale bar ("x" or "y").
        """

        sep_cm = self.config.scalebar_config.separation_cm
        offset_cm = self.config.scalebar_config.offset_cm
        delta_text_cm = self.config.scalebar_config.text_offset_cm
        font_size_pt = self.config.font_sizes.axes_pt

        ax_bbox = ax.get_position()
        overlay_ax = mpl_helpers.create_full_figure_axes(self.fig)

        if direction == "x":
            sep_rel = mpl_helpers.cm_to_fig_rel(self.fig, sep_cm, "height")
            offset_rel = mpl_helpers.cm_to_fig_rel(self.fig, offset_cm, "width")
            delta_text_rel = mpl_helpers.cm_to_fig_rel(
                self.fig, delta_text_cm, "height"
            )

            ax_lim = ax.get_xlim()
            length_rel = ax_bbox.width / (ax_lim[1] - ax_lim[0]) * length

            x_rel = ax_bbox.x0 + offset_rel
            y_rel = ax_bbox.y0 - sep_rel

            overlay_ax.plot([x_rel, x_rel + length_rel], [y_rel, y_rel], "k-")
            overlay_ax.text(
                x_rel + length_rel / 2, 
                y_rel - delta_text_rel, 
                label, 
                ha="center", 
                va="top", 
                fontsize=font_size_pt
            )
        
        elif direction == "y":
            sep_rel = mpl_helpers.cm_to_fig_rel(self.fig, sep_cm, "width")
            offset_rel = mpl_helpers.cm_to_fig_rel(self.fig, offset_cm, "height")
            delta_text_rel = mpl_helpers.cm_to_fig_rel(self.fig, delta_text_cm, "width")
            # The ascender length is roughly 0.25 of the font size for the default font
            # We therefore move the text this amount to make it appear to have the 
            # same distance to the scale bar as the text for the x-direction.
            font_offset_cm = mpl_helpers.pt_to_cm(font_size_pt) * 0.25
            delta_text_rel -= mpl_helpers.cm_to_fig_rel(
                self.fig, font_offset_cm, "width"
            )

            # Get the length of the scale bar in relative coordinates   
            ax_lim = ax.get_ylim()
            length_rel = ax_bbox.height / (ax_lim[1] - ax_lim[0]) * length

            x_rel = ax_bbox.x0 - sep_rel
            y_rel = ax_bbox.y0 + offset_rel

            overlay_ax.plot([x_rel, x_rel], [y_rel, y_rel + length_rel], "k-")
            overlay_ax.text(
                x_rel - delta_text_rel, 
                y_rel + length_rel / 2, 
                label, 
                ha="right", 
                va="center", 
                rotation=90, 
                fontsize=font_size_pt
            )
    
    def add_colorbar(
        self, 
        mappable: ScalarMappable,
        ax: MatplotlibAxes, 
        position: Literal["left", "right", "bottom", "top"],
        shrink_axes: bool = True
    ) -> Colorbar:
        """Add a colorbar adjacent to the given axes.

        This method optionally shrinks the provided axes to make room for a 
        colorbar and creates a properly configured colorbar in the specified position.

        Args:
            mappable: The mappable object (e.g., result of imshow, contourf, etc.) 
                to create the colorbar for.
            ax: The axes to add the colorbar to.
            position: The position of the colorbar relative to the axes.
            shrink_axes: Whether to shrink the original axes to make room for
                the colorbar. Defaults to True.

        Returns:
            The created colorbar object.
        """
        colorbar_config = self.config.colorbar_config
        
        if shrink_axes:
            total_space_cm = colorbar_config.width_cm + colorbar_config.separation_cm
            mpl_helpers.adjust_axes_size(ax, total_space_cm, position)
        
        position_rect = mpl_helpers.calculate_colorbar_position(
            ax, 
            position, 
            colorbar_config.width_cm, 
            colorbar_config.separation_cm
        )
        
        cbar_ax: MatplotlibAxes = self.fig.add_axes(position_rect)
        
        # Determine orientation based on position
        orientation = "vertical" if position in ["left", "right"] else "horizontal"
        
        # Create the colorbar
        cbar = self.fig.colorbar(mappable, cax=cbar_ax, orientation=orientation)
        
        # Configure colorbar based on position
        if position == "left":
            # Move ticks and labels to the left
            cbar.ax.yaxis.set_ticks_position('left')
            cbar.ax.yaxis.set_label_position('left')
        elif position == "right":
            # Ticks and labels are already on the right by default
            pass
        elif position == "bottom":
            # Ticks and labels are already on the bottom by default
            pass
        elif position == "top":
            # Move ticks and labels to the top
            cbar.ax.xaxis.set_ticks_position('top')
            cbar.ax.xaxis.set_label_position('top')
        
        return cbar
    
    def draw_description(
        self,
        ax: MatplotlibAxes,
        text: str,
        loc: str = "northwest",
        color: tuple[float, float, float] | str = (0, 0, 0),
        bg_color: tuple[float, float, float] | str = "none",
    ) -> None:
        """Add a description text inside the axes at a specified corner location.

        Args:
            ax: The matplotlib Axes object to annotate.
            text: The text to display as the description.
            loc: The corner location for the description. Must be one of
                'northwest', 'southwest', 'southeast', 'northeast'. Defaults to
                'northwest'.
            color: Text color. Defaults to black.
            bg_color: Background color behind the text. Defaults to "none".

        Returns:
            None

        Raises:
            ValueError: If `loc` is not one of the allowed position keywords.
        """
        font_size_pt = self.config.font_sizes.text_pt
        margin_cm = self.config.description_config.margin_cm
        delta_x = mpl_helpers.cm_to_axes_rel(ax, margin_cm, "width")
        delta_y = mpl_helpers.cm_to_axes_rel(ax, margin_cm, "height")

        if "south" in loc:
            # The ascender length is roughly 0.25 of the font size for the default font
            # We therefore move the text this amount to make it appear to have the 
            # same distance to the scale bar as the text for the x-direction.
            font_offset_cm = mpl_helpers.pt_to_cm(font_size_pt) * 0.25
            delta_y -= mpl_helpers.cm_to_axes_rel(
                ax, font_offset_cm, "height"
            )

        if loc == "northwest":
            x, y = delta_x, 1 - delta_y
            ha, va = "left", "top"
        elif loc == "southwest":
            x, y = delta_x, delta_y
            ha, va = "left", "bottom"
        elif loc == "southeast":
            x, y = 1 - delta_x, delta_y
            ha, va = "right", "bottom"
        elif loc == "northeast":
            x, y = 1 - delta_x, 1 - delta_y
            ha, va = "right", "top"
        else:
            raise ValueError(
                "Invalid 'loc' value. Must be one of: "
                "'northwest', 'southwest', 'southeast', 'northeast'."
            )

        ax.text(
            x,
            y,
            text,
            transform=ax.transAxes,
            color=color,
            fontsize=font_size_pt,
            ha=ha,
            va=va,
            bbox={
                "facecolor": bg_color,
                "edgecolor": "none",
                "boxstyle": "square,pad=0",
            },
        )
    
    def draw_debug_lines(self) -> None:
        """Draw debug grid lines if enabled in the configuration."""
        if not self.config.debug_panel.show:
            return
        
        # Create a transparent axes covering the entire figure
        fig = self.fig
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
        
    def save_fig(self, filename_suffix: str | None = None) -> None:
        """Saves the figure to the output directory.

        Args:
            filename_suffix: Optional string to append to
                :pyattr:`panel_name` when naming the saved file.
                
        Note:
            If no output directory is configured, a warning will be issued and
            the figure will not be saved.
        """
        try:
            if not self.config.panel_output.directory:
                warnings.warn(
                    "No output directory configured. Figure will not be saved.",
                    UserWarning,
                    stacklevel=2,
                )
                return

            directory = Path(self.config.panel_output.directory)
            if not directory.exists():
                warnings.warn(
                    f"Output directory does not exist: {directory}. "
                    "Figure will not be saved.",
                    UserWarning,
                    stacklevel=2,
                )
                return

            # Save the figure
            file_format = self.config.panel_output.format
            dpi = self.config.panel_output.dpi
            panel_name = self.panel_name
            if filename_suffix:
                panel_name = f"{panel_name}_{filename_suffix}"
            
            output_path = directory / f"{panel_name}.{file_format}"
            self.fig.savefig(output_path, dpi=dpi)

        except Exception as e:
            warnings.warn(
                f"Failed to save figure: {e!s}",
                UserWarning,
                stacklevel=2,
            )

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
    def axs(self) -> list[list[MatplotlibAxes]]:
        """List[List[matplotlib.axes.Axes]]: The grid of axes, guaranteed to exist.

        Raises:
            RuntimeError: If the axes grid has not been created yet.
        """
        if self._axs is None:
            raise RuntimeError("Axes grid has not been created yet.")
        return self._axs
    
    @property
    def panel_name(self) -> str:
        """str: The name of the panel, read-only."""
        return type(self)._panel_name

    @property
    def n_rows(self) -> int:
        """int: The number of rows in the panel grid, read-only."""
        return type(self)._n_rows

    @property
    def n_cols(self) -> int:
        """int: The number of columns in the panel grid, read-only."""
        return type(self)._n_cols
