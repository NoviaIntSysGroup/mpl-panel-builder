"""Tests for main PanelConfig functionality."""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any, TypeAlias

import pytest
import yaml

from mpl_panel_builder import PanelConfig, override_config

# For backward compatibility testing
PanelBuilderConfig = PanelConfig

ConfigDict: TypeAlias = dict[str, dict[str, Any]]

# Tests for PanelConfig
def test_from_dict_with_optional_ax_separation(
    sample_config_dict: ConfigDict
) -> None:
    """Test from_dict handles optional ax_separation_cm correctly.
    
    Args:
        sample_config_dict: Fixture providing sample configuration dictionary.
        
    Returns:
        None
    """
    missing_ax_separation_dict = copy.deepcopy(sample_config_dict)
    # Remove the optional key to test default behavior
    del missing_ax_separation_dict["axes_separation"]
    
    config = PanelBuilderConfig.from_dict(missing_ax_separation_dict)
    
    # Should use defaults for axes_separation
    assert config.axes_separation.x_cm == pytest.approx(0.0)
    assert config.axes_separation.y_cm == pytest.approx(0.0)


def test_from_dict_missing_required_keys(
    sample_config_dict: ConfigDict
) -> None:
    """Test from_dict fails appropriately with missing required keys.
    
    Args:
        sample_config_dict: Fixture providing sample configuration dictionary.
        
    Returns:
        None
        
    Raises:
        TypeError: Expected when required keys are missing.
    """
    required_keys = [
        "panel_dimensions",
        "panel_margins",
        "font_sizes"
    ]
    
    for key in required_keys:
        # Create a copy of the sample config with one required key removed
        incomplete_dict = copy.deepcopy(sample_config_dict)
        del incomplete_dict[key]
        
        with pytest.raises(TypeError, match=f"missing.*required.*argument.*{key}"):
            PanelBuilderConfig.from_dict(incomplete_dict)


def test_from_dict_invalid_nested_structure(
    sample_config_dict: ConfigDict
) -> None:
    """Test from_dict fails with malformed nested data.
    
    Args:
        sample_config_dict: Fixture providing sample configuration dictionary.
        
    Returns:
        None
        
    Raises:
        TypeError: Expected when nested data structure is invalid.
    """
    invalid_dict = copy.deepcopy(sample_config_dict)
    del invalid_dict["panel_dimensions"]["height_cm"]
    
    with pytest.raises(TypeError):
        PanelBuilderConfig.from_dict(invalid_dict)


def test_from_dict_invalid_dimensions(
    sample_config_dict: ConfigDict
) -> None:
    """Test from_dict fails with invalid dimensions.
    
    Args:
        sample_config_dict: Fixture providing sample configuration dictionary.
        
    Returns:
        None
        
    Raises:
        ValueError: Expected when dimensions have invalid values.
    """
    invalid_dict = copy.deepcopy(sample_config_dict)
    invalid_dict["panel_dimensions"]["width_cm"] = -10.0
    
    with pytest.raises(ValueError):
        PanelBuilderConfig.from_dict(invalid_dict)

# Tests for end to end config usage
def test_config_creation_with_overrides(
    sample_config_dict: ConfigDict
) -> None:
    """Test typical workflow: base config + overrides → PanelConfig object.
    
    Args:
        sample_config_dict: Fixture providing sample configuration dictionary.
        
    Returns:
        None
    """
    # Get first section and its first key for testing
    first_section = next(iter(sample_config_dict.keys()))
    first_key = next(iter(sample_config_dict[first_section].keys()))
    
    # Get original value for verification
    original_value = sample_config_dict[first_section][first_key]
    
    # Simulate user wanting larger figure
    user_overrides = {
        first_section: {first_key: "+=5.0"},
    }
    
    updated_dict = override_config(sample_config_dict, user_overrides)
    config = PanelBuilderConfig.from_dict(updated_dict)
    
    # Verify the pipeline worked end-to-end using dot notation
    section = getattr(config, first_section)
    assert getattr(section, first_key) == pytest.approx(original_value + 5.0)


def test_config_override_error_propagation(
    sample_config_dict: ConfigDict
) -> None:
    """Test that override errors propagate through the full pipeline.
    
    Args:
        sample_config_dict: Fixture providing sample configuration dictionary.
        
    Returns:
        None
        
    Raises:
        ValueError: Expected when an invalid override format is provided.
    """
    # Get first section and its first key for testing
    first_section = next(iter(sample_config_dict.keys()))
    first_key = next(iter(sample_config_dict[first_section].keys()))
    
    # Invalid override should fail before PanelConfig creation
    invalid_overrides = {
        first_section: {first_key: "invalid_operation"}
    }
    
    error_msg = "Invalid override format: invalid_operation"
    with pytest.raises(ValueError, match=error_msg):
        updated_dict = override_config(sample_config_dict, invalid_overrides)
        PanelBuilderConfig.from_dict(updated_dict)  # This line shouldn't be reached


def test_describe_config_returns_string() -> None:
    """Test that describe_config runs without errors and returns a string.
    
    Returns:
        None
    """
    # Test with default parameters
    result = PanelBuilderConfig.describe_config()
    assert isinstance(result, str)
    assert len(result) > 0
    assert "PanelConfig Configuration Reference" in result
    
    # Test with show_types=False
    result_no_types = PanelBuilderConfig.describe_config(show_types=False)
    assert isinstance(result_no_types, str)
    assert len(result_no_types) > 0
    
    # Test with show_defaults=False
    result_no_defaults = PanelBuilderConfig.describe_config(show_defaults=False)
    assert isinstance(result_no_defaults, str)
    assert len(result_no_defaults) > 0
    
    # Test with both disabled
    result_minimal = PanelBuilderConfig.describe_config(
        show_types=False, show_defaults=False
    )
    assert isinstance(result_minimal, str)
    assert len(result_minimal) > 0


def test_save_template_config_default_behavior(tmp_path: Path) -> None:
    """Test save_template_config with default parameters.
    
    Args:
        tmp_path: Pytest fixture providing temporary directory.
        
    Returns:
        None
    """
    # Save template to temporary path
    template_path = tmp_path / "test_template.yaml"
    PanelBuilderConfig.save_template_config(template_path)
    
    # Verify file was created
    assert template_path.exists()
    
    # Verify content is valid YAML
    with open(template_path) as f:
        content = yaml.safe_load(f)
    
    assert "panel_config" in content
    config_content = content["panel_config"]
    
    # Verify required fields are present with TODO placeholders
    assert "panel_dimensions" in config_content
    assert "panel_margins" in config_content
    assert "font_sizes" in config_content
    
    # Verify optional fields are present with default values
    assert "axes_separation" in config_content
    assert config_content["axes_separation"]["x_cm"] == 0.0
    assert config_content["axes_separation"]["y_cm"] == 0.0


def test_save_template_config_minimal_template(tmp_path: Path) -> None:
    """Test save_template_config with minimal options.
    
    Args:
        tmp_path: Pytest fixture providing temporary directory.
        
    Returns:
        None
    """
    # Save minimal template
    template_path = tmp_path / "minimal_template.yaml"
    PanelBuilderConfig.save_template_config(
        template_path,
        include_optional=False,
        include_descriptions=False
    )
    
    # Verify file was created
    assert template_path.exists()
    
    # Verify content is valid YAML
    with open(template_path) as f:
        content = yaml.safe_load(f)
    
    config_content = content["panel_config"]
    
    # Verify required fields are present
    assert "panel_dimensions" in config_content
    assert "panel_margins" in config_content
    assert "font_sizes" in config_content
    
    # Verify optional fields are not present (due to include_optional=False)
    assert "axes_separation" not in config_content


def test_save_template_config_custom_top_level_key(tmp_path: Path) -> None:
    """Test save_template_config with custom top-level key.
    
    Args:
        tmp_path: Pytest fixture providing temporary directory.
        
    Returns:
        None
    """
    # Save template with custom key
    template_path = tmp_path / "custom_key_template.yaml"
    custom_key = "my_custom_config"
    PanelBuilderConfig.save_template_config(
        template_path,
        top_level_key=custom_key
    )
    
    # Verify file was created
    assert template_path.exists()
    
    # Verify content uses custom key
    with open(template_path) as f:
        content = yaml.safe_load(f)
    
    assert custom_key in content
    assert "panel_config" not in content
