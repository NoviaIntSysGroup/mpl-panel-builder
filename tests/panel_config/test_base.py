"""Tests for panel_config base module (DotDict)."""

import pytest

from mpl_panel_builder.panel_config import DotDict
from mpl_panel_builder.panel_config.base import FrozenConfigBase


def test_dot_dict_core_functionality() -> None:
    """Test the core functionality of DotDict."""
    
    # Test data with nested structure
    config_data = {
        'key1': {
            'subkey1': 'value1',
            'subkey2': 42
        },
        'key2': 'value2',
        'key3': True
    }
    
    config = DotDict(config_data)
    
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


def test_frozen_config_base_extra_attributes() -> None:
    """Test FrozenConfigBase with extra attributes."""
    from dataclasses import dataclass
    
    @dataclass(frozen=True)
    class TestConfig(FrozenConfigBase):
        required_field: str
    
    # Test creation with extra attributes (dict and non-dict values)
    data = {
        'required_field': 'test_value',
        'extra_dict': {'nested': 'value'},
        'extra_string': 'simple_value',
        'extra_number': 42,
        'extra_bool': True
    }
    
    config = TestConfig.from_dict(data)
    
    # Test required field access
    assert config.required_field == 'test_value'
    
    # Test extra dict attribute access (should be wrapped in DotDict)
    assert config.extra_dict.nested == 'value'
    assert isinstance(config.extra_dict, DotDict)
    
    # Test extra non-dict attribute access
    assert config.extra_string == 'simple_value'
    assert config.extra_number == 42
    assert config.extra_bool is True
    
    # Test accessing non-existent extra attribute
    with pytest.raises(AttributeError, match="Object has no attribute 'nonexistent'"):
        _ = config.nonexistent


def test_frozen_config_base_nested_dataclass() -> None:
    """Test FrozenConfigBase with nested dataclass fields."""
    from dataclasses import dataclass
    
    @dataclass(frozen=True)
    class NestedConfig(FrozenConfigBase):
        nested_value: str
    
    @dataclass(frozen=True)
    class ParentConfig(FrozenConfigBase):
        required_field: str
        nested: NestedConfig
    
    # Test creation with nested dataclass
    data = {
        'required_field': 'parent_value',
        'nested': {
            'nested_value': 'child_value',
            'extra_nested': 'extra_value'
        }
    }
    
    config = ParentConfig.from_dict(data)
    
    # Test nested dataclass access
    assert config.nested.nested_value == 'child_value'
    assert config.nested.extra_nested == 'extra_value'
    assert isinstance(config.nested, NestedConfig)