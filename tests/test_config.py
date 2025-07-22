"""Tests for config module."""


import pytest

import mpl_panel_builder as mpb


def test_configure_and_get_config() -> None:
    """Test configuration system."""
    mpb.reset_config()
    
    mpb.configure({
        "panel": {"dimensions": {"width_cm": 10, "height_cm": 8}}
    })
    
    config = mpb.get_config()
    
    assert config["panel"]["dimensions"]["width_cm"] == 10
    assert config["panel"]["dimensions"]["height_cm"] == 8


def test_configure_merge_functionality() -> None:
    """Test configuration merging functionality."""
    mpb.reset_config()
    
    # Set initial config
    mpb.configure({
        "panel": {
            "dimensions": {"width_cm": 10, "height_cm": 8},
            "margins": {"left_cm": 1, "right_cm": 1}
        },
        "style": {
            "rc_params": {"font.size": 12}
        }
    })
    
    # Update only width
    mpb.configure({
        "panel": {
            "dimensions": {"width_cm": 15}
        }
    })
    
    config = mpb.get_config()
    
    assert config["panel"]["dimensions"]["width_cm"] == 15
    assert config["panel"]["dimensions"]["height_cm"] == 8  # unchanged
    assert config["panel"]["margins"]["left_cm"] == 1  # unchanged
    assert config["style"]["rc_params"]["font.size"] == 12  # unchanged


def test_configure_all_operators() -> None:
    """Test all operators (+=, -=, *, =) in configure."""
    mpb.reset_config()
    
    # Set initial config
    mpb.configure({
        "panel": {
            "dimensions": {"width_cm": 10, "height_cm": 8},
            "margins": {"left_cm": 2, "right_cm": 3}
        }
    })
    
    # Test += operator
    mpb.configure({
        "panel": {
            "dimensions": {"width_cm": "+=5"}
        }
    })
    
    config = mpb.get_config()
    assert config["panel"]["dimensions"]["width_cm"] == 15
    
    # Test -= operator
    mpb.configure({
        "panel": {
            "dimensions": {"height_cm": "-=3"}
        }
    })
    
    config = mpb.get_config()
    assert config["panel"]["dimensions"]["height_cm"] == 5
    
    # Test * operator
    mpb.configure({
        "panel": {
            "margins": {"left_cm": "*1.5"}
        }
    })
    
    config = mpb.get_config()
    assert config["panel"]["margins"]["left_cm"] == 3.0
    
    # Test = operator
    mpb.configure({
        "panel": {
            "margins": {"right_cm": "=7"}
        }
    })
    
    config = mpb.get_config()
    assert config["panel"]["margins"]["right_cm"] == 7.0


def test_configure_rc_params_merge() -> None:
    """Test that rc_params merges correctly."""
    mpb.reset_config()
    
    # Set initial rc_params
    mpb.configure({
        "style": {
            "rc_params": {"font.size": 12}
        }
    })
    
    # Add new rc_params without affecting existing ones
    mpb.configure({
        "style": {
            "rc_params": {"figure.figsize": [6, 4], "axes.labelsize": 10}
        }
    })
    
    config = mpb.get_config()
    
    assert config["style"]["rc_params"]["font.size"] == 12  # unchanged
    assert config["style"]["rc_params"]["figure.figsize"] == [6, 4]  # new
    assert config["style"]["rc_params"]["axes.labelsize"] == 10  # new


def test_configure_invalid_key_error() -> None:
    """Test error when trying to configure invalid key."""
    mpb.reset_config()
    
    with pytest.raises(KeyError, match="Configuration key .* is not valid"):
        mpb.configure({
            "invalid_section": {"some_key": "value"}
        })


def test_configure_invalid_format_error() -> None:
    """Test error with invalid format string."""
    mpb.reset_config()
    
    with pytest.raises(ValueError, match="Invalid configuration format"):
        mpb.configure({
            "panel": {
                "dimensions": {"width_cm": "+=invalid"}
            }
        })


def test_print_template_config() -> None:
    """Test printing template configuration to stdout."""
    import io
    import sys
    
    # Capture stdout
    captured_output = io.StringIO()
    sys.stdout = captured_output
    
    try:
        mpb.print_template_config()
        output = captured_output.getvalue()
        
        # Check that YAML output contains expected keys
        assert "panel:" in output
        assert "dimensions:" in output  
        assert "width_cm:" in output
        assert "style:" in output
        assert "rc_params:" in output
        assert "features:" in output
        assert "output:" in output
    finally:
        # Restore stdout
        sys.stdout = sys.__stdout__

