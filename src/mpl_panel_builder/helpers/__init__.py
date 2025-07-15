"""Helper utilities for mpl-panel-builder.

This module contains utility functions organized by purpose:
- mpl: Matplotlib-specific utilities used by the core library
- examples: Utilities for simplifying example scripts
"""

# Core matplotlib helpers (used internally by the library)
# Example utilities (for users writing examples/tutorials)
from .examples import get_logger, get_repo_root, setup_output_dir
from .mpl import (
    adjust_axes_size,
    calculate_colorbar_position,
    cm_to_axes_rel,
    cm_to_fig_rel,
    cm_to_inches,
    cm_to_pt,
    create_full_figure_axes,
    get_default_colors,
    get_pastel_colors,
    inches_to_cm,
    pt_to_cm,
)

__all__ = [
    # MPL utilities (primarily for internal use)
    "adjust_axes_size",
    "calculate_colorbar_position",
    "cm_to_axes_rel",
    "cm_to_fig_rel",
    "cm_to_inches",
    "cm_to_pt",
    "create_full_figure_axes",
    "get_default_colors",
    # Example utilities (for users)
    "get_logger",
    "get_pastel_colors",
    "get_repo_root",
    "inches_to_cm",
    "pt_to_cm",
    "setup_output_dir",
]