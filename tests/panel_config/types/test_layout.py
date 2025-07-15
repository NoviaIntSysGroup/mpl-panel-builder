"""Tests for layout configuration types."""

import pytest

from mpl_panel_builder.panel_config.types.figure import PanelDimensions


def test_panel_dimensions_valid() -> None:
    """Test PanelDimensions with valid values."""
    dims = PanelDimensions(width_cm=10.0, height_cm=8.0)
    assert dims.width_cm == 10.0
    assert dims.height_cm == 8.0


def test_panel_dimensions_negative_width() -> None:
    """Test PanelDimensions raises with negative width."""
    with pytest.raises(ValueError, match="Dimensions must be positive"):
        PanelDimensions(width_cm=-5.0, height_cm=8.0)


def test_panel_dimensions_negative_height() -> None:
    """Test PanelDimensions raises with negative height."""
    with pytest.raises(ValueError, match="Dimensions must be positive"):
        PanelDimensions(width_cm=10.0, height_cm=-3.0)


def test_panel_dimensions_immutable() -> None:
    """Test that PanelDimensions is immutable."""
    dims = PanelDimensions(width_cm=10.0, height_cm=8.0)
    
    with pytest.raises(AttributeError):
        dims.width_cm = 15.0
    
    with pytest.raises(AttributeError):
        dims.height_cm = 12.0