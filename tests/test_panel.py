"""Tests for panel module."""

import tempfile
from pathlib import Path

import matplotlib.pyplot as plt
import pytest

import mpl_panel_builder as mpb


def test_create_panel() -> None:
    """Test panel creation."""
    mpb.reset_config()
    
    mpb.set_rc_style()
    fig, axs = mpb.create_panel(rows=2, cols=2)
    
    assert fig is not None
    assert len(axs) == 2
    assert len(axs[0]) == 2
    assert len(axs[1]) == 2


def test_save_panel() -> None:
    """Test panel saving."""
    mpb.reset_config()
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        mpb.configure({
            "output": {"format": "png", "dpi": 100}
        })
        
        mpb.set_rc_style()
        fig, axs = mpb.create_panel(rows=1, cols=1)
        axs[0][0].plot([1, 2, 3], [1, 2, 3])
        
        # Use full path instead of just name
        filepath = str(Path(tmp_dir) / "test_panel")
        mpb.save_panel(fig, filepath)
        
        # Check that file was created
        saved_file = Path(tmp_dir) / "test_panel.png"
        assert saved_file.exists()


def test_set_rc_style() -> None:
    """Test style RC parameters setting."""
    mpb.reset_config()
    
    mpb.configure({
        "style": {"rc_params": {"font.size": 12, "axes.labelsize": 10}}
    })
    
    # Store original values
    original_font_size = plt.rcParams.get("font.size")
    original_labelsize = plt.rcParams.get("axes.labelsize")
    
    mpb.set_rc_style()
    
    assert plt.rcParams["font.size"] == 12
    assert plt.rcParams["axes.labelsize"] == 10
    
    # Reset to original values
    plt.rcParams["font.size"] = original_font_size
    plt.rcParams["axes.labelsize"] = original_labelsize


def test_set_rc_style_invalid_theme() -> None:
    """Test that invalid theme raises ValueError."""
    mpb.reset_config()
    
    mpb.configure({
        "style": {"theme": "invalid_theme"}
    })
    
    with pytest.raises(ValueError, match="Unknown theme 'invalid_theme'"):
        mpb.set_rc_style()


def test_create_stacked_panel() -> None:
    """Test stacked panel creation."""
    mpb.reset_config()
    
    mpb.set_rc_style()
    fig, axs = mpb.create_stacked_panel(rows=2, cols=2)
    
    assert fig is not None
    assert len(axs) == 2
    assert len(axs[0]) == 2
    assert len(axs[1]) == 2