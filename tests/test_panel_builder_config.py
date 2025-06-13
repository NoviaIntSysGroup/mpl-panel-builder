from __future__ import annotations

import copy
from typing import TypeAlias

import pytest

from mpl_panel_builder.panel_builder_config import (
    CustomConfigDotDict,
    PanelBuilderConfig,
    override_config,
)

ConfigDict: TypeAlias = dict[str, dict[str, float]]

# Tests for CustomConfigDotDict
def test_custom_config_dot_dict() -> None:
    """Test the core functionality of CustomConfigDotDict."""
    
    # Test data with nested structure
    config_data = {
        'key1': {
            'subkey1': 'value1',
            'subkey2': 42
        },
        'key2': 'value2',
        'key3': True
    }
    
    config = CustomConfigDotDict(config_data)
    
    # Test dot notation access works
    assert config.key2 == 'value2'
    assert config.key3 is True
    
    # Test nested dot notation access works
    assert config.key1.subkey1 == 'value1'
    assert config.key1.subkey2 == 42
    
    # Test dictionary access still works
    assert config['key2'] == 'value2'
    assert config['key1']['subkey1'] == 'value1'
    
    # Test read-only behavior - cannot modify attributes
    with pytest.raises(AttributeError, match="Cannot modify read-only config"):
        config.key2 = 'new_value'
    
    # Test read-only behavior - cannot delete attributes
    with pytest.raises(AttributeError, match="Cannot delete read-only config"):
        del config.key2
    
    # Test accessing non-existent attribute raises AttributeError
    with pytest.raises(AttributeError, match="Object has no attribute 'nonexistent'"):
        _ = config.nonexistent


# Tests for PanelBuilderConfig
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
    del missing_ax_separation_dict["ax_separation_cm"]
    
    config = PanelBuilderConfig.from_dict(missing_ax_separation_dict)
    
    # Should use defaults for ax_separation_cm
    assert config.ax_separation_cm.x == pytest.approx(0.0)
    assert config.ax_separation_cm.y == pytest.approx(0.0)


def test_from_dict_missing_required_keys(
    sample_config_dict: ConfigDict
) -> None:
    """Test from_dict fails appropriately with missing required keys.
    
    Args:
        sample_config_dict: Fixture providing sample configuration dictionary.
        
    Returns:
        None
        
    Raises:
        KeyError: Expected when required keys are missing.
    """
    # Keep only panel_dimensions_cm
    incomplete_dict = {
        "panel_dimensions_cm": copy.deepcopy(
            sample_config_dict["panel_dimensions_cm"]
            )
    }
    
    with pytest.raises(TypeError):
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
    del invalid_dict["panel_dimensions_cm"]["height"]
    
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
    invalid_dict["panel_dimensions_cm"]["width"] = -10.0
    
    with pytest.raises(ValueError):
        PanelBuilderConfig.from_dict(invalid_dict)


def test_arithmetic_operations(sample_config_dict: ConfigDict) -> None:
    """Test all arithmetic override operations work correctly.
    
    Args:
        sample_config_dict: Fixture providing sample configuration dictionary.
        
    Returns:
        None
    """
    updates = {
        "panel_dimensions_cm": {"width": "+=5.0", "height": "*0.5"},
        "panel_margins_cm": {"top": "=2.0", "left": "-=0.5"},
        "font_sizes_pt": {"axes": 16, "text": "+=2"},
    }
    
    result = override_config(sample_config_dict, updates)
    
    # Get base values from sample_config_dict
    base_width = sample_config_dict["panel_dimensions_cm"]["width"]
    base_height = sample_config_dict["panel_dimensions_cm"]["height"]
    base_margin_left = sample_config_dict["panel_margins_cm"]["left"]
    base_text_size = sample_config_dict["font_sizes_pt"]["text"]
    
    assert (
        result["panel_dimensions_cm"]["width"] 
        == pytest.approx(base_width + 5.0)
    )
    assert (
        result["panel_dimensions_cm"]["height"] 
        == pytest.approx(base_height * 0.5)
    )
    # Directly set value
    assert (
        result["panel_margins_cm"]["top"] 
        == pytest.approx(2.0)
    )
    assert (
        result["panel_margins_cm"]["left"] 
        == pytest.approx(base_margin_left - 0.5)
    )
    assert (
        result["font_sizes_pt"]["axes"] 
        == pytest.approx(16)  # Direct assignment
    )
    assert (
        result["font_sizes_pt"]["text"] 
        == pytest.approx(base_text_size + 2)
    )


def test_string_number_conversion(sample_config_dict: ConfigDict) -> None:
    """Test that string numbers are properly converted.
    
    Args:
        sample_config_dict: Fixture providing sample configuration dictionary.
        
    Returns:
        None
    """
    updates = {
        "panel_dimensions_cm": {"width": "15.5"},
        "font_sizes_pt": {"axes": "14"},
    }
    
    result = override_config(sample_config_dict, updates)
    
    assert result["panel_dimensions_cm"]["width"] == pytest.approx(15.5)
    assert result["font_sizes_pt"]["axes"] == pytest.approx(14.0)


def test_nonexistent_key_error(sample_config_dict: ConfigDict) -> None:
    """Test that overriding non-existent keys raises appropriate error.
    
    Args:
        sample_config_dict: Fixture providing sample configuration dictionary.
        
    Returns:
        None
        
    Raises:
        KeyError: Expected when trying to override a non-existent key.
    """
    updates = {
        "nonexistent_section": {"value": 10.0}
    }
    
    error_msg = "Cannot override non-existent key: nonexistent_section"
    with pytest.raises(KeyError, match=error_msg):
        override_config(sample_config_dict, updates)
    
    # Test nested non-existent key
    updates = {
        "panel_dimensions_cm": {"nonexistent_field": 10.0}
    }
    
    error_msg = "Cannot override non-existent key: nonexistent_field"
    with pytest.raises(KeyError, match=error_msg):
        override_config(sample_config_dict, updates)


@pytest.mark.parametrize(
    "invalid_format",
    [
        "invalid_format",
        "-=not_a_number",
        "+=invalid_number",
        "*bad_value",
        "=non_numeric",
    ]
)
def test_invalid_override_formats(
    sample_config_dict: ConfigDict, 
    invalid_format: str
) -> None:
    """Test error handling for invalid override string formats.
    
    Args:
        sample_config_dict: Fixture providing sample configuration dictionary.
        invalid_format: String containing an invalid override format to test.
        
    Returns:
        None
        
    Raises:
        ValueError: Expected when an invalid override format is provided.
    """
    updates = {
        "panel_dimensions_cm": {"width": invalid_format}
    }
    
    error_msg = f"Invalid override format: {invalid_format}"
    with pytest.raises(ValueError) as e:
        override_config(sample_config_dict, updates)
    assert error_msg in str(e.value)


def test_original_config_preserved(sample_config_dict: ConfigDict) -> None:
    """Test that original configuration is not mutated.
    
    Args:
        sample_config_dict: Fixture providing sample configuration dictionary.
        
    Returns:
        None
    """
    original_width = sample_config_dict["panel_dimensions_cm"]["width"]
    
    updates = {
        "panel_dimensions_cm": {"width": "+=5.0"}
    }
    
    result = override_config(sample_config_dict, updates)
    
    # Original should be unchanged
    assert (
        sample_config_dict["panel_dimensions_cm"]["width"] 
        == pytest.approx(original_width)
    )
    # Result should be updated
    assert (
        result["panel_dimensions_cm"]["width"] 
        == pytest.approx(original_width + 5.0)
    )


def test_deep_nested_overrides() -> None:
    """Test override works with arbitrary nesting depth.
    
    Returns:
        None
    """
    base = {
        "level1": {
            "level2": {
                "level3": {"value": 10.0, "other": 5.0}
            },
            "other_level2": {"value": 20.0}
        }
    }
    
    updates = {
        "level1": {
            "level2": {
                "level3": {"value": "+=5.0"}
            },
            "other_level2": {"value": "*2"}
        }
    }
    
    result = override_config(base, updates)
    
    assert result["level1"]["level2"]["level3"]["value"] == pytest.approx(15.0)
    assert result["level1"]["level2"]["level3"]["other"] == pytest.approx(5.0)
    assert result["level1"]["other_level2"]["value"] == pytest.approx(40.0)


def test_config_creation_with_overrides(
    sample_config_dict: ConfigDict
) -> None:
    """Test typical workflow: base config + overrides → PanelConfig object.
    
    Args:
        sample_config_dict: Fixture providing sample configuration dictionary.
        
    Returns:
        None
    """
    # Simulate user wanting larger figure with bigger fonts
    user_overrides = {
        "panel_dimensions_cm": {"width": "+=5.0", "height": "+=2.0"},
        "font_sizes_pt": {"axes": "*1.2", "text": "*1.2"},
    }
    
    updated_dict = override_config(sample_config_dict, user_overrides)
    config = PanelBuilderConfig.from_dict(updated_dict)
    
    # Verify the pipeline worked end-to-end
    assert config.panel_dimensions_cm.width == pytest.approx(15.0)
    assert config.panel_dimensions_cm.height == pytest.approx(10.0)
    assert config.font_sizes_pt.axes == pytest.approx(14.4)  # 12.0 * 1.2
    assert config.font_sizes_pt.text == pytest.approx(12.0)  # 10.0 * 1.2
    assert config.ax_separation_cm.x == pytest.approx(0.5)  # Unchanged


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
    # Remove ax_separation_cm to match the original test
    if "ax_separation_cm" in sample_config_dict:
        del sample_config_dict["ax_separation_cm"]
    
    # Invalid override should fail before PanelConfig creation
    invalid_overrides = {
        "panel_dimensions_cm": {"width": "invalid_operation"}
    }
    
    error_msg = "Invalid override format: invalid_operation"
    with pytest.raises(ValueError, match=error_msg):
        updated_dict = override_config(sample_config_dict, invalid_overrides)
        PanelBuilderConfig.from_dict(updated_dict)  # This line shouldn't be reached