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
        "panel_dimensions_cm": {"width": 10.0, "height": 8.0},
        "panel_margins_cm": {"top": 1.0, "bottom": 1.5, "left": 2.0, "right": 1.0},
        "font_sizes_pt": {"axes": 12.0, "text": 10.0},
        # Optional (has default values)
        "ax_separation_cm": {"x": 0.5, "y": 1.0},
        "debug_panel": {"show": True, "grid_res_cm": 0.5},
        "panel_output": {
            "directory": str(tmp_path),
            "format": "pdf",
            "dpi": 600,
        },
    }
