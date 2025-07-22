"""Scale bar functionality."""

from matplotlib.axes import Axes

from ..config import get_config
from ..helpers.mpl import cm_to_fig_rel, create_full_figure_axes, pt_to_cm


def draw_x_scale_bar(ax: Axes, length: float, label: str) -> None:
    """Draws a horizontal scale bar for the given axes.

    The scale bar is drawn on a new axes covering the entire figure. This 
    makes it possible to draw the scale bar on inside or outside of the axes.

    Args:
        ax: The axes to draw the scale bar for.
        length: The length of the scale bar in axes units.
        label: The label to display next to the scale bar.
    """
    fig = ax.get_figure()
    if fig is None:
        raise ValueError("Axes must be attached to a figure")
    config = get_config()
    scalebar_config = config['features']['scalebar']
    
    # Get font size from axes and line width from axis spines
    font_size_pt = float(ax.xaxis.label.get_fontsize())
    linewidth = ax.spines['bottom'].get_linewidth()
    
    # Get axes position in figure coordinates
    ax_bbox = ax.get_position()
    
    # Convert measurements to figure-relative coordinates
    sep_rel = cm_to_fig_rel(fig, scalebar_config['separation_cm'], "height")
    offset_rel = cm_to_fig_rel(fig, scalebar_config['offset_cm'], "width")
    delta_text_rel = cm_to_fig_rel(fig, scalebar_config['text_offset_cm'], "height")
    
    # Calculate scale bar length in figure-relative coordinates
    ax_lim = ax.get_xlim()
    length_rel = ax_bbox.width / (ax_lim[1] - ax_lim[0]) * length
    
    # Position scale bar (bottom-left of axes with offset)
    x_rel = ax_bbox.x0 + offset_rel
    y_rel = ax_bbox.y0 - sep_rel
    
    # Create overlay axes covering the entire figure
    overlay_ax = create_full_figure_axes(fig)

    # Draw scale bar
    overlay_ax.plot(
        [x_rel, x_rel + length_rel], [y_rel, y_rel], "k-", linewidth=linewidth
    )
    
    # Add label
    overlay_ax.text(
        x_rel + length_rel / 2, 
        y_rel - delta_text_rel, 
        label, 
        ha="center", 
        va="top",
        fontsize=font_size_pt
    )

def draw_y_scale_bar(ax: Axes, length: float, label: str) -> None:
    """Draws a vertical scale bar for the given axes.

    The scale bar is drawn on a new axes covering the entire figure. This 
    makes it possible to draw the scale bar on inside or outside of the axes.

    Args:
        ax: The axes to draw the scale bar for.
        length: The length of the scale bar in axes units.
        label: The label to display next to the scale bar.
    """
    fig = ax.get_figure()
    if fig is None:
        raise ValueError("Axes must be attached to a figure")
    config = get_config()
    scalebar_config = config['features']['scalebar']
    
    # Get font size from axes and line width from axis spines
    font_size_pt = float(ax.yaxis.label.get_fontsize())
    linewidth = ax.spines['left'].get_linewidth()
    
    # Get axes position in figure coordinates
    ax_bbox = ax.get_position()
    
    # Convert measurements to figure-relative coordinates
    sep_rel = cm_to_fig_rel(fig, scalebar_config['separation_cm'], "width")
    offset_rel = cm_to_fig_rel(fig, scalebar_config['offset_cm'], "height")
    delta_text_rel = cm_to_fig_rel(fig, scalebar_config['text_offset_cm'], "width")
    # The ascender length is roughly 0.25 of the font size for the default font
    # We therefore move the text this amount to make it appear to have the 
    # same distance to the scale bar as the text for the x-direction.
    font_offset_cm = pt_to_cm(font_size_pt) * 0.25
    delta_text_rel -= cm_to_fig_rel(fig, font_offset_cm, "width")
    
    # Get the length of the scale bar in relative coordinates   
    ax_lim = ax.get_ylim()
    length_rel = ax_bbox.height / (ax_lim[1] - ax_lim[0]) * length
    
    # Position scale bar (left side of axes with offset)
    x_rel = ax_bbox.x0 - sep_rel
    y_rel = ax_bbox.y0 + offset_rel
    
    # Create overlay axes covering the entire figure
    overlay_ax = create_full_figure_axes(fig)

    # Draw scale bar
    overlay_ax.plot(
        [x_rel, x_rel], [y_rel, y_rel + length_rel], "k-", linewidth=linewidth
    )
    
    # Add label
    overlay_ax.text(
        x_rel - delta_text_rel, 
        y_rel + length_rel / 2, 
        label, 
        ha="right", 
        va="center", 
        rotation=90,
        fontsize=font_size_pt
    )