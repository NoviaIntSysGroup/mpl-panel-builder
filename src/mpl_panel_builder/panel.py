"""Core panel creation and management functions."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from .config import get_config
from .helpers.mpl import cm_to_inches


def create_panel(rows: int = 1, cols: int = 1) -> tuple[Figure, list[list[Axes]]]:
    """Creates figure and axes grid using global config.
    
    Args:
        rows: Number of rows in axes grid
        cols: Number of columns in axes grid
        
    Returns:
        Tuple of (figure, axes_grid)
    """
    config = get_config()
    
    # Get dimensions from config
    panel_dims = config['panel']['dimensions']
    margins = config['panel']['margins']
    axes_sep = config['panel']['axes_separation']
    
    # Convert cm to inches
    fig_width_in = cm_to_inches(panel_dims['width_cm'])
    fig_height_in = cm_to_inches(panel_dims['height_cm'])
    
    # Create figure
    fig = plt.figure(figsize=(fig_width_in, fig_height_in))
    
    # Calculate plot region in relative coordinates
    plot_left_rel = margins['left_cm'] / panel_dims['width_cm']
    plot_bottom_rel = margins['bottom_cm'] / panel_dims['height_cm']
    plot_width_rel = (
        panel_dims['width_cm'] - margins['left_cm'] - margins['right_cm']
    ) / panel_dims['width_cm']
    plot_height_rel = (
        panel_dims['height_cm'] - margins['top_cm'] - margins['bottom_cm']
    ) / panel_dims['height_cm']
    
    # Convert separation to relative coordinates
    sep_x_rel = axes_sep['x_cm'] / panel_dims['width_cm']
    sep_y_rel = axes_sep['y_cm'] / panel_dims['height_cm']
    
    # Calculate axes dimensions
    axes_width_rel = (plot_width_rel - (cols - 1) * sep_x_rel) / cols
    axes_height_rel = (plot_height_rel - (rows - 1) * sep_y_rel) / rows
    
    # Create axes grid using manual positioning
    axs = []
    for i in range(rows):
        row = []
        for j in range(cols):
            # Calculate position for this axes
            ax_x = plot_left_rel + j * (axes_width_rel + sep_x_rel)
            ax_y = (plot_bottom_rel + plot_height_rel 
                    - (i + 1) * axes_height_rel - i * sep_y_rel)
            
            ax = fig.add_axes((ax_x, ax_y, axes_width_rel, axes_height_rel))
            row.append(ax)
        axs.append(row)
    
    return fig, axs

def save_panel(fig: Figure, filepath: str) -> None:
    """Saves panel using global config.
    
    Args:
        fig: Matplotlib figure to save
        filepath: Full path including filename and extension
        
    Raises:
        ValueError: If filepath contains parent directory references (..)
        OSError: If file or directory operations fail
    """
    config = get_config()
    output_config = config['output']
    
    # Check for parent directory references for security
    if '..' in filepath:
        raise ValueError(
            f"Path contains parent directory references ('..'): {filepath}. "
            "This could be unsafe."
        )
    
    try:
        path = Path(filepath)
    except (ValueError, OSError) as e:
        raise ValueError(f"Invalid file path: {filepath}") from e
    
    # Create output directory if it doesn't exist
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except (OSError, PermissionError) as e:
        raise OSError(f"Could not create directory {path.parent}: {e}") from e
    
    # Add extension if not provided
    final_path = path
    if path.suffix == '':
        final_path = path.with_suffix(f'.{output_config["format"]}')
    
    # Save the figure
    try:
        fig.savefig(
            str(final_path), 
            dpi=output_config['dpi'], 
            format=output_config['format']
        )
    except Exception as e:
        raise OSError(f"Could not save figure to {final_path}: {e}") from e

def set_rc_style() -> None:
    """Sets matplotlib rcParams globally from configuration.
    
    Raises:
        ValueError: If theme is not 'article' or 'none'
    """
    config = get_config()
    style_config = config['style']
    
    # Validate theme
    valid_themes = {'article', 'none'}
    theme = style_config['theme']
    if theme not in valid_themes:
        valid_themes_str = ', '.join(sorted(valid_themes))
        raise ValueError(
            f"Unknown theme '{theme}'. Valid themes are: {valid_themes_str}"
        )
    
    # Start with theme-based defaults
    if theme == 'article':
        rc_params = {
            # Font settings
            "font.size": 6,
            "axes.titlesize": 8,
            "axes.labelsize": 8,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "figure.titlesize": 8,
            "legend.fontsize": 6,
            # Line and marker styles
            "lines.linewidth": 1,
            "lines.markersize": 4,
            # Axes appearance
            'axes.facecolor': 'white',
            "axes.spines.right": False,
            "axes.spines.top": False,
            # Legend appearance
            "legend.frameon": True,
            "legend.framealpha": 0.6,
            "legend.edgecolor": 'none',
            "legend.handlelength": 1.0,
            "legend.handletextpad": 0.7,
            "legend.labelspacing": 0.4,
            "legend.columnspacing": 1.0,
        }
    else:  # 'none' theme
        rc_params = {}
    
    # Update with user-specified rcParams
    rc_params.update(style_config['rc_params'])
    
    # Set rcParams globally
    plt.rcParams.update(rc_params)