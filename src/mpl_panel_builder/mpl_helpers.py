"""Helper functions for matplotlib."""

from typing import Literal, cast

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure, SubFigure
from numpy.typing import NDArray


def cm_to_inches(cm: float) -> float:
    """Convert centimeters to inches.
    
    Args:
        cm: The value in centimeters.
        
    Returns:
        The value in inches.
    """
    return cm / 2.54

def inches_to_cm(inch: float) -> float:
    """Convert inches to centimeters.
    
    Args:
        inch: The value in inches.
        
    Returns:
        The value in centimeters.
    """
    return inch * 2.54

def cm_to_pt(cm: float) -> float:
    """Convert centimeters to points.
    
    Args:
        cm: The value in centimeters.
        
    Returns:
        The value in points.
    """
    return cm_to_inches(cm) * 72

def pt_to_cm(pt: float) -> float:
    """Convert points to centimeters.

    A point is 1/72 of an inch.

    Args:
        pt: The value in points.

    Returns:
        The value in centimeters.
    """
    return inches_to_cm(pt / 72)

def cm_to_fig_rel(
    fig: Figure | SubFigure, cm: float, dim: Literal["width", "height"]
) -> float:
    """Convert centimeters to relative figure coordinates.
    
    This is a simple conversion factor.

    Args:
        fig: The figure to convert the coordinates for.
        cm: The value in centimeters.
        dim: The dimension to convert to relative coordinates.

    Returns:
        The value in relative coordinates.
    
    Raises:
        ValueError: If dim is not "width" or "height".
    """
    valid_dims = ["width", "height"]
    if dim not in valid_dims:
        raise ValueError(
            f"Invalid dimension: {dim!r}. Must be one of: {valid_dims!r}."
        )
    
    if hasattr(fig, 'get_size_inches'):
        size_inches = fig.get_size_inches()
    else:
        # SubFigure case - get size from parent figure
        size_inches = fig.figure.get_size_inches()
    
    if dim == "width":
        return cm_to_inches(cm) / float(size_inches[0])
    elif dim == "height":
        return cm_to_inches(cm) / float(size_inches[1])
    else:
        # This should never be reached due to validation above
        raise ValueError(f"Invalid dimension: {dim!r}")

def fig_rel_to_cm(
    fig: Figure | SubFigure, rel: float, dim: Literal["width", "height"]
) -> float:
    """Convert relative coordinates to centimeters.
    
    Args:
        fig: The figure to convert the coordinates for.
        rel: The value in relative coordinates.
        dim: The dimension to convert to centimeters.   

    Returns:
        The value in centimeters.
    
    Raises:
        ValueError: If dim is not "width" or "height".
    """
    valid_dims = ["width", "height"]
    if dim not in valid_dims:
        raise ValueError(
            f"Invalid dimension: {dim!r}. Must be one of: {valid_dims!r}."
        )
    
    if hasattr(fig, 'get_size_inches'):
        size_inches = fig.get_size_inches()
    else:
        # SubFigure case - get size from parent figure
        size_inches = fig.figure.get_size_inches()
    
    if dim == "width":
        return inches_to_cm(rel * float(size_inches[0]))
    elif dim == "height":
        return inches_to_cm(rel * float(size_inches[1]))
    else:
        # This should never be reached due to validation above
        raise ValueError(f"Invalid dimension: {dim!r}")

def cm_to_axes_rel(
    ax: Axes, cm: float, dim: Literal["width", "height"]
) -> float:
    """Convert centimeters to relative axes coordinates.
    
    Converts a distance in centimeters to relative coordinates for use with 
    ax.transAxes transform.
    
    Args:
        ax: The matplotlib Axes object to convert coordinates for.
        cm: The distance in centimeters.
        dim: The dimension to convert to relative coordinates.
        
    Returns:
        The value in relative axes coordinates.
    
    Raises:
        ValueError: If dim is not "width" or "height".
    """
    valid_dims = ["width", "height"]
    if dim not in valid_dims:
        raise ValueError(
            f"Invalid dimension: {dim!r}. Must be one of: {valid_dims!r}."
        )
    
    fig = ax.get_figure()
    if fig is None:
        raise ValueError("Axes must be attached to a figure")
    
    # Convert to figure relative coordinates first
    fig_rel = cm_to_fig_rel(fig, cm, dim)
    
    # Convert from figure coordinates to axes coordinates
    ax_pos = ax.get_position()
    if dim == "width":
        return float(fig_rel / ax_pos.width)
    elif dim == "height":
        return float(fig_rel / ax_pos.height)
    else:
        # This should never be reached due to validation above
        raise ValueError(f"Invalid dimension: {dim!r}")

def get_default_colors() -> list[str]:
    """Return the default Matplotlib colors in hex or named format.

    Retrieves the list of default colors used in Matplotlib's property cycle.

    Returns:
        list[str]: A list of color hex codes or named color strings.
    """
    prop_cycle = plt.rcParams["axes.prop_cycle"]
    colors = cast(list[str], prop_cycle.by_key().get("color", []))
    return colors

def get_pastel_colors() -> NDArray[np.float64]:
    """Return a list of 8 pastel colors from the 'Pastel2' colormap.

    Uses Matplotlib's 'Pastel2' colormap to generate 8 RGBA color values.

    Returns:
        NDArray[np.float64]: An array of shape (8, 4), where each row is an
        RGBA color with float64 components.
    """
    cmap = plt.get_cmap("Pastel2")
    colors: NDArray[np.float64] = cmap(np.arange(8))
    return colors

def create_full_figure_axes(fig: Figure) -> Axes:
    """Create an invisible axes covering the entire figure.

    This axes is used to draw or annotate anywhere in the figure using relative
    coordinates.

    Args:
        fig: Figure to add the axes to.

    Returns:
        The created axes.
    """

    ax = fig.add_axes((0.0, 0.0, 1.0, 1.0), facecolor="none", zorder=-1)
    ax.axis("off")
    ax.set(xlim=[0, 1], ylim=[0, 1])
    return ax

def move_yaxis_right(ax: Axes) -> None:
    """Move the y-axis of the given Axes object to the right side.

    This function updates tick marks, label position, and spine visibility to move
    the y-axis from the left to the right of the plot.

    Args:
        ax (Axes): The matplotlib Axes object to modify.

    Returns:
        None
    """
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position("right")
    ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(True)

def move_xaxis_top(ax: Axes) -> None:
    """Move the x-axis of the given Axes object to the top side.

    This function updates tick marks, label position, and spine visibility to move
    the x-axis from the bottom to the top of the plot.

    Args:
        ax (Axes): The matplotlib Axes object to modify.

    Returns:
        None
    """
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position("top")
    ax.spines["bottom"].set_visible(False)
    ax.spines["top"].set_visible(True)

def adjust_axes_size(
    ax: Axes, 
    length_cm: float, 
    direction: Literal["left", "right", "bottom", "top"]
) -> None:
    """Adjust the size of an axes by shrinking it in the specified direction.

    This function modifies the axes position to make room for additional 
    elements like colorbars by reducing its size in the specified direction.

    Args:
        ax (Axes): The matplotlib Axes object to modify.
        length_cm (float): The amount to shrink the axes by in centimeters.
        direction (Literal["left", "right", "bottom", "top"]): The direction
            to shrink the axes towards.

    Returns:
        None
    
    Raises:
        ValueError: If direction is not one of "left", "right", "bottom", "top".
    """
    valid_directions = ["left", "right", "bottom", "top"]
    if direction not in valid_directions:
        raise ValueError(
            f"Invalid direction: {direction!r}. Must be one of: {valid_directions!r}."
        )
    
    fig = ax.get_figure()
    if fig is None:
        raise ValueError("Axes must be attached to a figure")
    
    # Get current position
    pos = ax.get_position()
    x0, y0, width, height = pos.x0, pos.y0, pos.width, pos.height
    
    # Convert length to relative coordinates
    if direction in ["left", "right"]:
        length_rel = cm_to_fig_rel(fig, length_cm, "width")
    else:  # "bottom", "top"
        length_rel = cm_to_fig_rel(fig, length_cm, "height")
    
    # Adjust position based on direction
    if direction == "left":
        new_x0 = x0 + length_rel
        new_width = width - length_rel
        ax.set_position((new_x0, y0, new_width, height))
    elif direction == "right":
        new_width = width - length_rel
        ax.set_position((x0, y0, new_width, height))
    elif direction == "bottom":
        new_y0 = y0 + length_rel
        new_height = height - length_rel
        ax.set_position((x0, new_y0, width, new_height))
    elif direction == "top":
        new_height = height - length_rel
        ax.set_position((x0, y0, width, new_height))

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
    else:
        # This should never be reached due to validation above
        raise ValueError(f"Invalid position: {position!r}")
