from pathlib import Path
from typing import TypeAlias

import pytest

ConfigDict: TypeAlias = dict[str, dict[str, float | str | None]]


@pytest.fixture
def sample_config_dict(tmp_path: Path) -> ConfigDict:
    """Sample configuration dictionary for testing.
    
    Args:
        tmp_path: Pytest fixture providing a temporary directory.
        
    Returns:
        ConfigDict: A dictionary containing sample configuration values.
    """
    return {
        # Required (no default values)
        "panel_dimensions": {"width_cm": 10.0, "height_cm": 8.0},
        "panel_margins": {
            "top_cm": 1.0, 
            "bottom_cm": 1.5, 
            "left_cm": 2.0, 
            "right_cm": 1.0
        },
        "font_sizes": {"axes_pt": 12.0, "text_pt": 10.0},
        # Optional (has default values)
        "axes_separation": {"x_cm": 0.5, "y_cm": 1.0},
        "debug_panel": {"show": True, "grid_resolution_cm": 0.5},
        "panel_output": {
            "directory": str(tmp_path),
            "format": "pdf",
            "dpi": 600,
        },
    }
