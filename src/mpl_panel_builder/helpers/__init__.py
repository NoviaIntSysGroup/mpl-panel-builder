"""Helper utilities for mpl-panel-builder.

This module contains matplotlib-specific utilities used by the core library.
Example utilities are available in the .examples submodule but not exposed here.
"""

# Core matplotlib helpers (used internally by the library)
from .mpl import (
    adjust_axes_size,
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
    "cm_to_axes_rel",
    "cm_to_fig_rel",
    "cm_to_inches",
    "cm_to_pt",
    "create_full_figure_axes",
    "get_default_colors",
    "get_pastel_colors",
    "inches_to_cm",
    "pt_to_cm",
]