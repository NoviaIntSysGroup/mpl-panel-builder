from typing import TypeAlias

import pytest

ConfigDict: TypeAlias = dict[str, dict[str, float]]


@pytest.fixture
def sample_config_dict() -> ConfigDict:
    """Sample configuration dictionary for testing.
    
    Returns:
        ConfigDict: A dictionary containing sample configuration values.
    """
    return {
        "panel_dimensions_cm": {"width": 10.0, "height": 8.0},
        "panel_margins_cm": {"top": 1.0, "bottom": 1.5, "left": 2.0, "right": 1.0},
        "font_sizes_pt": {"axes": 12.0, "text": 10.0},
        "ax_separation_cm": {"x": 0.5, "y": 1.0},
    }