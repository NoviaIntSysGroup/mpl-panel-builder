"""Colorbar functionality."""

from typing import Literal

from matplotlib.axes import Axes
from matplotlib.cm import ScalarMappable
from matplotlib.colorbar import Colorbar

from ..config import get_config
from ..helpers.mpl import adjust_axes_size, cm_to_fig_rel


def calculate_colorbar_position(
    ax: Axes,
    position: Literal["left", "right", "bottom", "top"],
    width_cm: float,
    separation_cm: float
) -> tuple[float, float, float, float]:
    """Calculate colorbar position rectangle (x, y, width, height).
    
    Args:
        ax: The axes to place the colorbar next to.
        position: The position of the colorbar relative to the axes.
        width_cm: The width of the colorbar in centimeters.
        separation_cm: The separation between axes and colorbar in centimeters.
        
    Returns:
        Tuple of (x, y, width, height) in relative coordinates.
    
    Raises:
        ValueError: If position is not one of "left", "right", "bottom", "top".
    """
    valid_positions = ["left", "right", "bottom", "top"]
    if position not in valid_positions:
        raise ValueError(
            f"Invalid position: {position!r}. Must be one of: {valid_positions!r}."
        )
    
    fig = ax.get_figure()
    if fig is None:
        raise ValueError("Axes must be attached to a figure")
    
    ax_pos = ax.get_position()
    is_vertical = position in ["left", "right"]
    dimension_type: Literal["width", "height"] = "width" if is_vertical else "height"
    
    width_rel = cm_to_fig_rel(fig, width_cm, dimension_type)
    sep_rel = cm_to_fig_rel(fig, separation_cm, dimension_type)
    
    if position == "left":
        return (
            ax_pos.x0 - sep_rel - width_rel,
            ax_pos.y0,
            width_rel,
            ax_pos.height
        )
    elif position == "right":
        return (
            ax_pos.x0 + ax_pos.width + sep_rel,
            ax_pos.y0,
            width_rel,
            ax_pos.height
        )
    elif position == "bottom":
        return (
            ax_pos.x0,
            ax_pos.y0 - sep_rel - width_rel,
            ax_pos.width,
            width_rel
        )
    elif position == "top":
        return (
            ax_pos.x0,
            ax_pos.y0 + ax_pos.height + sep_rel,
            ax_pos.width,
            width_rel
        )

def add_colorbar(
    ax: Axes,
    mappable: ScalarMappable, 
    position: Literal["left", "right", "bottom", "top"],
    shrink_axes: bool = True
) -> Colorbar:
    """Add a colorbar adjacent to the given axes.

    This method optionally shrinks the provided axes to make room for a 
    colorbar and creates a properly configured colorbar in the specified position.

    Args:
        ax: The axes to add the colorbar to.
        mappable: The mappable object (e.g., result of imshow, contourf, etc.) 
            to create the colorbar for.
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
    
    fig = ax.get_figure()
    if fig is None:
        raise ValueError("Axes must be attached to a figure")
    
    config = get_config()
    colorbar_config = config['features']['colorbar']
    
    if shrink_axes:
        total_space_cm = colorbar_config['width_cm'] + colorbar_config['separation_cm']
        adjust_axes_size(ax, total_space_cm, position)
    
    position_rect = calculate_colorbar_position(
        ax, 
        position, 
        colorbar_config['width_cm'], 
        colorbar_config['separation_cm']
    )
    
    cbar_ax = fig.add_axes(position_rect)
    
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