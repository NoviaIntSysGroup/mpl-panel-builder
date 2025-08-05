"""Simple global configuration system."""

from typing import Any, TypedDict, cast


# Type definitions for configuration structure
class DimensionsConfig(TypedDict):
    width_cm: float
    height_cm: float

class MarginsConfig(TypedDict):
    top_cm: float
    bottom_cm: float
    left_cm: float
    right_cm: float

class AxesSeparationConfig(TypedDict):
    x_cm: float
    y_cm: float

class PanelConfig(TypedDict):
    dimensions: DimensionsConfig
    margins: MarginsConfig
    axes_separation: AxesSeparationConfig

class StyleConfig(TypedDict):
    theme: str
    rc_params: dict[str, Any]

class ScalebarConfig(TypedDict):
    separation_cm: float
    offset_cm: float
    text_offset_cm: float
    line_width_pt: float

class ColorbarConfig(TypedDict):
    width_cm: float
    separation_cm: float

class AnnotationConfig(TypedDict):
    margin_cm: float

class LabelConfig(TypedDict):
    x_cm: float
    y_cm: float
    bold: bool
    caps: bool
    prefix: str
    suffix: str
    fontsize_pt: float

class GridlinesConfig(TypedDict):
    resolution_cm: float

class FeaturesConfig(TypedDict):
    scalebar: ScalebarConfig
    colorbar: ColorbarConfig
    annotation: AnnotationConfig
    label: LabelConfig
    gridlines: GridlinesConfig

class OutputConfig(TypedDict):
    format: str
    dpi: int

class Config(TypedDict):
    panel: PanelConfig
    style: StyleConfig
    features: FeaturesConfig
    output: OutputConfig

# Default configuration
_default_config = {
    'panel': {
        'dimensions': {'width_cm': 8, 'height_cm': 6},
        'margins': {'top_cm': 0.5, 'bottom_cm': 1.0, 'left_cm': 1.5, 'right_cm': 0.5},
        'axes_separation': {'x_cm': 0.5, 'y_cm': 0.5}
    },
    'style': {
        'theme': 'none',
        'rc_params': {}
    },
    'features': {
        'scalebar': {
            'separation_cm': 0.2, 'offset_cm': 0.2, 'text_offset_cm': 0.1,
            'line_width_pt': 1.5
        },
        'colorbar': {'width_cm': 0.3, 'separation_cm': 0.2},
        'annotation': {'margin_cm': 0.2},
        'label': {
            'x_cm': 0.5, 'y_cm': 0.5, 'bold': True, 'caps': True,
            'prefix': '', 'suffix': '', 'fontsize_pt': 10
        },
        'gridlines': {'resolution_cm': 0.5}
    },
    'output': {
        'format': 'pdf',
        'dpi': 600
    },
}

_config = _default_config.copy()

def configure(config_dict: dict[str, Any]) -> None:
    """Configure the package with user settings.
    
    Supports special string formats for relative updates:
    - "+=X": Add X to the current value
    - "-=X": Subtract X from the current value
    - "*X": Multiply current value by X
    - "=X": Set value to X (same as providing X directly)
    
    Args:
        config_dict: Dictionary with configuration updates
    """
    global _config
    _config = _merge_config(_config, config_dict)

def get_config() -> Config:
    """Get current configuration."""
    return cast(Config, _config)

def reset_config() -> None:
    """Reset to default configuration."""
    global _config
    _config = _default_config.copy()

def print_template_config() -> None:
    """Print the default configuration as YAML to standard output."""
    import sys

    import yaml
    
    yaml.dump(_default_config, sys.stdout, default_flow_style=False, sort_keys=False)

def _merge_config(base: dict[str, Any], updates: dict[str, Any]) -> Config:
    """Merges configuration updates into a base configuration.

    Supports special string formats for relative updates:
    - "+=X": Add X to the current value
    - "-=X": Subtract X from the current value
    - "*X": Multiply current value by X
    - "=X": Set value to X (same as providing X directly)

    Args:
        base: Base configuration dictionary to be updated.
        updates: Dictionary with configuration updates to merge into the base.

    Returns:
        Updated configuration dictionary.

    Raises:
        ValueError: If an override string has invalid format.
    """
    import copy
    
    def _interpret(value: Any, current: Any) -> Any:
        """Interprets update values, handling special string formats."""
        if isinstance(value, int | float):
            return value
        if isinstance(value, str):
            # Check for special operators first
            if value.startswith("+="):
                try:
                    return current + float(value[2:])
                except ValueError as e:
                    raise ValueError(f"Invalid configuration format: {value}") from e
            elif value.startswith("-="):
                try:
                    return current - float(value[2:])
                except ValueError as e:
                    raise ValueError(f"Invalid configuration format: {value}") from e
            elif value.startswith("*"):
                try:
                    return current * float(value[1:])
                except ValueError as e:
                    raise ValueError(f"Invalid configuration format: {value}") from e
            elif value.startswith("="):
                try:
                    return float(value[1:])
                except ValueError as e:
                    raise ValueError(f"Invalid configuration format: {value}") from e
            else:
                # Try to convert to float, but if it fails, return as string
                try:
                    return float(value)
                except ValueError:
                    return value
        return value

    def _recursive_merge(
        base_dict: dict[str, Any], override_dict: dict[str, Any]
    ) -> dict[str, Any]:
        """Recursively merges two dictionaries, applying value interpretation."""
        result = copy.deepcopy(base_dict)
        for key, val in override_dict.items():
            if key not in result:
                raise KeyError(f"Configuration key '{key}' is not valid")

            if key in ["rc_params"]:
                # Special handling: merge rc_params without validation
                # as we don't want to specify every possible rc_param
                # and since rcParams validate keys at runtime.
                result[key].update(val)
            elif isinstance(val, dict) and isinstance(result[key], dict):
                result[key] = _recursive_merge(result[key], val)
            else:
                result[key] = _interpret(val, result[key])
        return result

    return cast(Config, _recursive_merge(base, updates))
