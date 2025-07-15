"""Tests for panel_config utils module (override_config)."""

from typing import Any, TypeAlias

import pytest

from mpl_panel_builder import override_config

ConfigDict: TypeAlias = dict[str, dict[str, Any]]


def test_arithmetic_operations(sample_config_dict: ConfigDict) -> None:
    """Test all arithmetic override operations work correctly.
    
    Args:
        sample_config_dict: Fixture providing sample configuration dictionary.
        
    Returns:
        None
    """
    # Get first three different sections for testing
    sections = list(sample_config_dict.keys())[:3]
    first_section = sections[0]
    second_section = sections[1]
    third_section = sections[2]
    
    # Get first two keys from each section
    first_section_keys = list(sample_config_dict[first_section].keys())[:2]
    second_section_keys = list(sample_config_dict[second_section].keys())[:2]
    third_section_keys = list(sample_config_dict[third_section].keys())[:2]
    
    first_key, second_key = first_section_keys
    third_key, fourth_key = second_section_keys
    fifth_key, sixth_key = third_section_keys
    
    updates = {
        first_section: {first_key: "+=5.0", second_key: "*0.5"},
        second_section: {third_key: "=2.0", fourth_key: "-=0.5"},
        third_section: {fifth_key: 16, sixth_key: "+=2"},
    }
    
    result = override_config(sample_config_dict, updates)
    
    # Get base values from sample_config_dict
    base_first = sample_config_dict[first_section][first_key]
    base_second = sample_config_dict[first_section][second_key]
    base_fourth = sample_config_dict[second_section][fourth_key]
    base_sixth = sample_config_dict[third_section][sixth_key]
    
    assert (
        result[first_section][first_key] 
        == pytest.approx(base_first + 5.0)
    )
    assert (
        result[first_section][second_key] 
        == pytest.approx(base_second * 0.5)
    )
    assert (
        result[second_section][third_key] 
        == pytest.approx(2.0)  # Direct assignment
    )
    assert (
        result[second_section][fourth_key] 
        == pytest.approx(base_fourth - 0.5)
    )
    assert (
        result[third_section][fifth_key] 
        == pytest.approx(16)  # Direct assignment
    )
    assert (
        result[third_section][sixth_key] 
        == pytest.approx(base_sixth + 2)
    )


def test_string_number_conversion(sample_config_dict: ConfigDict) -> None:
    """Test that string numbers are properly converted.
    
    Args:
        sample_config_dict: Fixture providing sample configuration dictionary.
        
    Returns:
        None
    """
    # Get first two different sections for testing
    sections = list(sample_config_dict.keys())[:2]
    first_section = sections[0]
    second_section = sections[1]
    
    # Get first key from each section
    first_key = next(iter(sample_config_dict[first_section].keys()))
    second_key = next(iter(sample_config_dict[second_section].keys()))
    
    updates = {
        first_section: {first_key: "15.5"},
        second_section: {second_key: "14"},
    }
    
    result = override_config(sample_config_dict, updates)
    
    assert result[first_section][first_key] == pytest.approx(15.5)
    assert result[second_section][second_key] == pytest.approx(14.0)


def test_nonexistent_key_error(sample_config_dict: ConfigDict) -> None:
    """Test that overriding non-existent keys raises appropriate error.
    
    Args:
        sample_config_dict: Fixture providing sample configuration dictionary.
        
    Returns:
        None
        
    Raises:
        KeyError: Expected when trying to override a non-existent key.
    """
    # Get first section for testing
    first_section = next(iter(sample_config_dict.keys()))
    
    # Test non-existent section
    updates = {
        "nonexistent_section": {"value": 10.0}
    }
    
    error_msg = "Cannot override non-existent key: nonexistent_section"
    with pytest.raises(KeyError, match=error_msg):
        override_config(sample_config_dict, updates)
    
    # Test nested non-existent key
    updates = {
        first_section: {"nonexistent_field": 10.0}
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
    # Get first section and its first key for testing
    first_section = next(iter(sample_config_dict.keys()))
    first_key = next(iter(sample_config_dict[first_section].keys()))
    
    updates = {
        first_section: {first_key: invalid_format}
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
    # Get first section and its first key for testing
    first_section = next(iter(sample_config_dict.keys()))
    first_key = next(iter(sample_config_dict[first_section].keys()))
    
    original_value = sample_config_dict[first_section][first_key]
    
    updates = {
        first_section: {first_key: "+=5.0"}
    }
    
    _ = override_config(sample_config_dict, updates)
    
    # Original should be unchanged
    assert (
        sample_config_dict[first_section][first_key] 
        == pytest.approx(original_value)
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