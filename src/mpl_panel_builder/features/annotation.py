"""Annotation functionality."""

from matplotlib.axes import Axes

from ..config import get_config
from ..helpers.mpl import cm_to_axes_rel, pt_to_cm


def add_annotation(
    ax: Axes,
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
    config = get_config()
    annotation_config = config['features']['annotation']
    
    # Get font size from global config
    font_size_pt = config['style']['rc_params'].get('font.size', 8)
    
    # Calculate margins with ascender correction for south positions
    margin_cm = annotation_config['margin_cm']
    delta_x = cm_to_axes_rel(ax, margin_cm, "width")
    delta_y = cm_to_axes_rel(ax, margin_cm, "height")

    if "south" in loc:
        # The ascender length is roughly 0.25 of the font size for the default font
        # We therefore move the text this amount to make it appear to have the 
        # same distance to the scale bar as the text for the x-direction.
        font_offset_cm = pt_to_cm(font_size_pt) * 0.25
        delta_y -= cm_to_axes_rel(ax, font_offset_cm, "height")

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
    