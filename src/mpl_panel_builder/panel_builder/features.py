"""Feature rendering (scale bars, colorbars, descriptions)."""

from typing import Literal

from matplotlib.axes import Axes as MatplotlibAxes
from matplotlib.cm import ScalarMappable
from matplotlib.colorbar import Colorbar
from matplotlib.figure import Figure as MatplotlibFigure

from ..helpers import mpl as mpl_helpers
from ..panel_config import PanelConfig


class FeatureManager:
    """Manages rendering of panel features like scale bars and colorbars."""

    def __init__(self, config: PanelConfig):
        """Initialize feature manager.
        
        Args:
            config: Panel configuration object.
        """
        self.config = config

    def draw_x_scale_bar(
        self, 
        fig: MatplotlibFigure,
        ax: MatplotlibAxes, 
        length: float, 
        label: str
    ) -> None:
        """Draws a horizontal scale bar for the given axes.

        The scale bar is drawn on a new axes covering the entire figure. This 
        makes it possible to draw the scale bar on inside or outside of the axes.

        Args:
            fig: The matplotlib figure to draw on.
            ax: The axes to draw the scale bar for.
            length: The length of the scale bar in axes units.
            label: The label to display next to the scale bar.
        """
        sep_cm = self.config.scalebar_config.separation_cm
        offset_cm = self.config.scalebar_config.offset_cm
        delta_text_cm = self.config.scalebar_config.text_offset_cm
        font_size_pt = self.config.font_sizes.axes_pt

        ax_bbox = ax.get_position()
        overlay_ax = mpl_helpers.create_full_figure_axes(fig)

        sep_rel = mpl_helpers.cm_to_fig_rel(fig, sep_cm, "height")
        offset_rel = mpl_helpers.cm_to_fig_rel(fig, offset_cm, "width")
        delta_text_rel = mpl_helpers.cm_to_fig_rel(
            fig, delta_text_cm, "height"
        )

        ax_lim = ax.get_xlim()
        length_rel = ax_bbox.width / (ax_lim[1] - ax_lim[0]) * length

        x_rel = ax_bbox.x0 + offset_rel
        y_rel = ax_bbox.y0 - sep_rel

        overlay_ax.plot(
            [x_rel, x_rel + length_rel], [y_rel, y_rel], "k-", linewidth=1.0
        )
        overlay_ax.text(
            x_rel + length_rel / 2, 
            y_rel - delta_text_rel, 
            label, 
            ha="center", 
            va="top", 
            fontsize=font_size_pt
        )
    
    def draw_y_scale_bar(
        self, 
        fig: MatplotlibFigure,
        ax: MatplotlibAxes, 
        length: float, 
        label: str
    ) -> None:
        """Draws a vertical scale bar for the given axes.

        The scale bar is drawn on a new axes covering the entire figure. This 
        makes it possible to draw the scale bar on inside or outside of the axes.

        Args:
            fig: The matplotlib figure to draw on.
            ax: The axes to draw the scale bar for.
            length: The length of the scale bar in axes units.
            label: The label to display next to the scale bar.
        """
        sep_cm = self.config.scalebar_config.separation_cm
        offset_cm = self.config.scalebar_config.offset_cm
        delta_text_cm = self.config.scalebar_config.text_offset_cm
        font_size_pt = self.config.font_sizes.axes_pt

        ax_bbox = ax.get_position()
        overlay_ax = mpl_helpers.create_full_figure_axes(fig)

        sep_rel = mpl_helpers.cm_to_fig_rel(fig, sep_cm, "width")
        offset_rel = mpl_helpers.cm_to_fig_rel(fig, offset_cm, "height")
        delta_text_rel = mpl_helpers.cm_to_fig_rel(fig, delta_text_cm, "width")
        # The ascender length is roughly 0.25 of the font size for the default font
        # We therefore move the text this amount to make it appear to have the 
        # same distance to the scale bar as the text for the x-direction.
        font_offset_cm = mpl_helpers.pt_to_cm(font_size_pt) * 0.25
        delta_text_rel -= mpl_helpers.cm_to_fig_rel(
            fig, font_offset_cm, "width"
        )

        # Get the length of the scale bar in relative coordinates   
        ax_lim = ax.get_ylim()
        length_rel = ax_bbox.height / (ax_lim[1] - ax_lim[0]) * length

        x_rel = ax_bbox.x0 - sep_rel
        y_rel = ax_bbox.y0 + offset_rel

        overlay_ax.plot(
            [x_rel, x_rel], [y_rel, y_rel + length_rel], "k-", linewidth=1.0
        )
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
        fig: MatplotlibFigure,
        mappable: ScalarMappable,
        ax: MatplotlibAxes, 
        position: Literal["left", "right", "bottom", "top"],
        shrink_axes: bool = True
    ) -> Colorbar:
        """Add a colorbar adjacent to the given axes.

        This method optionally shrinks the provided axes to make room for a 
        colorbar and creates a properly configured colorbar in the specified position.

        Args:
            fig: The matplotlib figure to draw on.
            mappable: The mappable object (e.g., result of imshow, contourf, etc.) 
                to create the colorbar for.
            ax: The axes to add the colorbar to.
            position: The position of the colorbar relative to the axes.
            shrink_axes: Whether to shrink the original axes to make room for
                the colorbar. Defaults to True.

        Returns:
            The created colorbar object.

        Raises:
            ValueError: If position is not one of "left", "right", "bottom", "top".
        """
        valid_positions = ["left", "right", "bottom", "top"]
        if position not in valid_positions:
            raise ValueError(
                f"Invalid position: {position!r}. Must be one of: {valid_positions!r}."
            )
        
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
        
        cbar_ax: MatplotlibAxes = fig.add_axes(position_rect)
        
        # Determine orientation based on position
        orientation = "vertical" if position in ["left", "right"] else "horizontal"
        
        # Create the colorbar
        cbar = fig.colorbar(mappable, cax=cbar_ax, orientation=orientation)
        
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
    
    def add_annotation(
        self,
        ax: MatplotlibAxes,
        text: str,
        loc: str = "northwest",
        color: tuple[float, float, float] | str = (0, 0, 0),
        bg_color: tuple[float, float, float] | str = "none",
    ) -> None:
        """Add a annotation text inside the axes at a specified corner location.

        Args:
            ax: The matplotlib Axes object to annotate.
            text: The text to display as the annotation.
            loc: The corner location for the annotation. Must be one of
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
    