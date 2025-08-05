"""Label functionality."""

from matplotlib.axes import Axes

from ..config import get_config
from ..helpers.mpl import cm_to_fig_rel


def add_label(ax: Axes, label: str) -> None:
    """Add a label at specified position from top-left corner of axes.
    
    Uses global configuration for positioning and formatting. Position is measured
    from top-left corner of axes, with positive values moving away from the axes.
    Uses figure-relative coordinates for consistent positioning.
    
    Args:
        ax: The matplotlib Axes object to label.
        label: The text to display as the label.
        
    Returns:
        None
    """
    config = get_config()
    label_config = config['features']['label']
    
    # Get font size from label config
    font_size_pt = label_config['fontsize_pt']
    
    # Apply text transformations
    text = label
    if label_config['caps']:
        text = text.upper()
    else:
        text = text.lower()
    
    # Add prefix and suffix
    text = f"{label_config['prefix']}{text}{label_config['suffix']}"
    
    # Get figure for coordinate conversion
    fig = ax.get_figure()
    if fig is None:
        raise ValueError("Axes must be attached to a figure")
    
    # Get axes position in figure coordinates
    ax_pos = ax.get_position()
    
    # Convert offset distances to figure relative coordinates
    x_offset_rel = cm_to_fig_rel(fig, label_config['x_cm'], "width")
    y_offset_rel = cm_to_fig_rel(fig, label_config['y_cm'], "height")
    
    # Position at top-left corner of axes, offset by specified distances
    x_fig = ax_pos.x0 - x_offset_rel
    y_fig = ax_pos.y1 + y_offset_rel
    
    # Determine font weight
    font_weight = 'bold' if label_config['bold'] else 'normal'
    
    ax.text(
        x_fig,
        y_fig,
        text,
        transform=fig.transFigure,
        fontsize=font_size_pt,
        fontweight=font_weight,
        ha='left',
        va='top'
    )