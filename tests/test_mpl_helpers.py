"""Tests for mpl_helpers module."""

import numpy as np

from mpl_panel_builder.mpl_helpers import get_default_colors, get_pastel_colors


def test_get_default_colors() -> None:
    """Test that get_default_colors returns a list of valid color strings."""
    colors = get_default_colors()
    
    # Check return type
    assert isinstance(colors, list)
    assert all(isinstance(color, str) for color in colors)


def test_get_pastel_colors() -> None:
    """Test that get_pastel_colors returns an array of 8 RGBA colors."""
    colors = get_pastel_colors()
    
    # Check return type and shape
    assert isinstance(colors, np.ndarray)
    assert colors.dtype == np.float64
    assert colors.shape == (8, 4)
    
    # Check that all values are between 0 and 1 (valid RGBA range)
    assert np.all((colors >= 0) & (colors <= 1))
