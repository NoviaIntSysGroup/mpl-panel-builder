"""Tests for mpl_helpers module."""

import numpy as np
import pytest

from mpl_panel_builder.helpers.mpl import (
    cm_to_inches,
    cm_to_pt,
    get_default_colors,
    get_pastel_colors,
    inches_to_cm,
    pt_to_cm,
)


def test_cm_to_inches() -> None:
    """Test centimeter to inch conversion."""
    # Test known conversions
    assert cm_to_inches(2.54) == pytest.approx(1.0)
    assert cm_to_inches(0.0) == 0.0


def test_inches_to_cm() -> None:
    """Test inch to centimeter conversion."""
    # Test known conversions
    assert inches_to_cm(1.0) == pytest.approx(2.54)
    assert inches_to_cm(0.0) == 0.0


def test_cm_to_pt() -> None:
    """Test centimeter to point conversion."""
    # Test known conversions (1 inch = 72 points)
    assert cm_to_pt(2.54) == pytest.approx(72.0)
    assert cm_to_pt(0.0) == 0.0


def test_pt_to_cm() -> None:
    """Test point to centimeter conversion."""
    # Test known conversions
    assert pt_to_cm(72.0) == pytest.approx(2.54)
    assert pt_to_cm(0.0) == 0.0


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
