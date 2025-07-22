"""Test configuration fixtures."""

import matplotlib

matplotlib.use('Agg')  # Use non-interactive backend for testing

from pathlib import Path
from typing import Any, TypeAlias

import pytest

ConfigDict: TypeAlias = dict[str, Any]


@pytest.fixture
def sample_config_dict(tmp_path: Path) -> ConfigDict:
    """Sample configuration dictionary for testing with new structure.
    
    Args:
        tmp_path: Pytest fixture providing a temporary directory.
        
    Returns:
        ConfigDict: A dictionary containing sample configuration values.
    """
    return {
        "panel": {
            "dimensions": {"width_cm": 10.0, "height_cm": 8.0},
            "margins": {
                "top_cm": 1.0, 
                "bottom_cm": 1.5, 
                "left_cm": 2.0, 
                "right_cm": 1.0
            },
            "axes_separation": {"x_cm": 0.5, "y_cm": 1.0},
        },
        "style": {
            "theme": "white",
            "rc_params": {
                "axes.titlesize": 12.0,
                "axes.labelsize": 12.0,
                "xtick.labelsize": 12.0,
                "ytick.labelsize": 12.0,
                "figure.titlesize": 12.0,
                "font.size": 10.0,
                "legend.fontsize": 10.0,
            }
        },
        "features": {
            "scalebar": {"separation_cm": 0.2, "offset_cm": 0.2, "text_offset_cm": 0.1},
            "colorbar": {"width_cm": 0.3, "separation_cm": 0.2},
            "annotation": {"margin_cm": 0.2},
            "gridlines": {"resolution_cm": 0.5}
        },
        "output": {
            "format": "pdf",
            "dpi": 600,
        },
    }
