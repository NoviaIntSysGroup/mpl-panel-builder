"""Tests for mpl_helpers module."""

import matplotlib.pyplot as plt
import numpy as np
import pytest
from matplotlib.axes import Axes

from mpl_panel_builder.helpers.mpl import (
    adjust_axes_size,
    cm_to_axes_rel,
    cm_to_fig_rel,
    cm_to_inches,
    cm_to_pt,
    create_full_figure_axes,
    fig_rel_to_cm,
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


def test_cm_to_fig_rel() -> None:
    """Test centimeter to figure relative coordinate conversion."""
    # Create figure with known size
    fig = plt.figure(figsize=(10, 8))  # 10 inches wide, 8 inches tall
    
    # Test width conversion: 1 inch = 0.1 of 10 inch width
    one_inch_cm = inches_to_cm(1.0)
    width_rel = cm_to_fig_rel(fig, one_inch_cm, "width")
    assert width_rel == pytest.approx(0.1, abs=0.01)
    
    # Test height conversion: 1 inch = 0.125 of 8 inch height  
    height_rel = cm_to_fig_rel(fig, one_inch_cm, "height")
    assert height_rel == pytest.approx(0.125, abs=0.01)
    
    # Test invalid dimension
    with pytest.raises(ValueError, match="Invalid dimension"):
        cm_to_fig_rel(fig, 1.0, "depth") # type: ignore[call-arg]
    
    plt.close(fig)


def test_fig_rel_to_cm() -> None:
    """Test figure relative to centimeter conversion."""
    # Create figure with known size
    fig = plt.figure(figsize=(10, 8))  # 10 inches wide, 8 inches tall
    
    # Test width conversion: 0.1 of 10 inch width = 1 inch
    expected_cm = inches_to_cm(1.0)
    width_cm = fig_rel_to_cm(fig, 0.1, "width")
    assert width_cm == pytest.approx(expected_cm, abs=0.01)
    
    # Test height conversion: 0.125 of 8 inch height = 1 inch
    height_cm = fig_rel_to_cm(fig, 0.125, "height")
    assert height_cm == pytest.approx(expected_cm, abs=0.01)
    
    # Test roundtrip conversion
    original_cm = 5.0
    fig_rel = cm_to_fig_rel(fig, original_cm, "width")
    roundtrip_cm = fig_rel_to_cm(fig, fig_rel, "width")
    assert roundtrip_cm == pytest.approx(original_cm, abs=0.01)
    
    # Test invalid dimension
    with pytest.raises(ValueError, match="Invalid dimension"):
        fig_rel_to_cm(fig, 0.1, "depth") # type: ignore[call-arg]
    
    plt.close(fig)


def test_cm_to_axes_rel() -> None:
    """Test centimeter to axes relative coordinate conversion."""
    # Create figure and axes with known dimensions
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_axes((0.2, 0.2, 0.6, 0.5))  # 60% width, 50% height
    
    # Test conversion - axes is 60% of figure width (6 inches)
    # 1 inch = 1/6 of axes width = ~0.167
    one_inch_cm = inches_to_cm(1.0)
    width_rel = cm_to_axes_rel(ax, one_inch_cm, "width")
    assert width_rel == pytest.approx(0.167, abs=0.01)
    
    # Test conversion - axes is 50% of figure height (4 inches)  
    # 1 inch = 1/4 of axes height = 0.25
    height_rel = cm_to_axes_rel(ax, one_inch_cm, "height")
    assert height_rel == pytest.approx(0.25, abs=0.01)
    
    # Test invalid dimension
    with pytest.raises(ValueError, match="Invalid dimension"):
        cm_to_axes_rel(ax, 1.0, "depth") # type: ignore[call-arg]
    
    plt.close(fig)


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


def test_create_full_figure_axes() -> None:
    """Test creation of full-figure spanning axes."""
    fig = plt.figure(figsize=(6, 4))
    
    # Create full figure axes
    full_ax = create_full_figure_axes(fig)
    
    # Verify it's an Axes object
    assert isinstance(full_ax, Axes)
    
    # Check position covers entire figure
    pos = full_ax.get_position()
    assert pos.x0 == pytest.approx(0.0)
    assert pos.y0 == pytest.approx(0.0)
    assert pos.width == pytest.approx(1.0)
    assert pos.height == pytest.approx(1.0)
    
    # Check limits are normalized
    assert full_ax.get_xlim() == (0, 1)
    assert full_ax.get_ylim() == (0, 1)
    
    # Check it was added to the figure
    assert full_ax in fig.axes
    
    plt.close(fig)


def test_adjust_axes_size() -> None:
    """Test axes size adjustment in all directions."""
    # Create figure with known size (10x8 inches)
    fig = plt.figure(figsize=(10, 8))
    
    # Test each direction: make axes 1 cm smaller
    shrink_amount_cm = 1.0
    # Convert to relative coordinates using helper functions
    shrink_amount_rel_width = cm_to_inches(shrink_amount_cm) / 10  # 1 cm / 10 inch
    shrink_amount_rel_height = cm_to_inches(shrink_amount_cm) / 8  # 1 cm / 8 inch
    
    # Test "left" direction
    ax = fig.add_axes((0.2, 0.2, 0.6, 0.5))  # Start with known position
    original_pos = ax.get_position()
    adjust_axes_size(ax, shrink_amount_cm, "left")
    new_pos = ax.get_position()
    
    # Check: x0 should move right, width should decrease
    expected_x0 = original_pos.x0 + shrink_amount_rel_width
    assert new_pos.x0 == pytest.approx(expected_x0, abs=0.001)
    expected_width = original_pos.width - shrink_amount_rel_width
    assert new_pos.width == pytest.approx(expected_width, abs=0.001)
    assert new_pos.y0 == pytest.approx(original_pos.y0)  # y unchanged
    assert new_pos.height == pytest.approx(original_pos.height)  # height unchanged
    
    # Test "right" direction
    ax = fig.add_axes((0.2, 0.2, 0.6, 0.5))
    original_pos = ax.get_position()
    adjust_axes_size(ax, shrink_amount_cm, "right")
    new_pos = ax.get_position()
    
    # Check: x0 unchanged, width should decrease
    assert new_pos.x0 == pytest.approx(original_pos.x0)  # x0 unchanged
    expected_width = original_pos.width - shrink_amount_rel_width
    assert new_pos.width == pytest.approx(expected_width, abs=0.001)
    assert new_pos.y0 == pytest.approx(original_pos.y0)  # y unchanged
    assert new_pos.height == pytest.approx(original_pos.height)  # height unchanged
    
    # Test "bottom" direction
    ax = fig.add_axes((0.2, 0.2, 0.6, 0.5))
    original_pos = ax.get_position()
    adjust_axes_size(ax, shrink_amount_cm, "bottom")
    new_pos = ax.get_position()
    
    # Check: y0 should move up, height should decrease
    assert new_pos.x0 == pytest.approx(original_pos.x0)  # x unchanged
    assert new_pos.width == pytest.approx(original_pos.width)  # width unchanged
    expected_y0 = original_pos.y0 + shrink_amount_rel_height
    assert new_pos.y0 == pytest.approx(expected_y0, abs=0.001)
    expected_height = original_pos.height - shrink_amount_rel_height
    assert new_pos.height == pytest.approx(expected_height, abs=0.001)

    # Test "top" direction
    ax = fig.add_axes((0.2, 0.2, 0.6, 0.5))
    original_pos = ax.get_position()
    adjust_axes_size(ax, shrink_amount_cm, "top")
    new_pos = ax.get_position()
    
    # Check: y0 unchanged, height should decrease
    assert new_pos.x0 == pytest.approx(original_pos.x0)  # x unchanged
    assert new_pos.width == pytest.approx(original_pos.width)  # width unchanged
    assert new_pos.y0 == pytest.approx(original_pos.y0)  # y0 unchanged
    expected_height = original_pos.height - shrink_amount_rel_height
    assert new_pos.height == pytest.approx(expected_height, abs=0.001)
    
    # Test invalid direction
    ax = fig.add_axes((0.2, 0.2, 0.6, 0.5))
    with pytest.raises(ValueError, match="Invalid direction"):
        adjust_axes_size(ax, 1.0, "diagonal") # type: ignore[call-arg]
    
    plt.close(fig)