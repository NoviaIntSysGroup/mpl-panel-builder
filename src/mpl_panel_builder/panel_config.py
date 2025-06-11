import copy
from dataclasses import dataclass, field
from typing import Any


@dataclass
class FontSizes:
    """Stores font sizes for different figure elements.
    
    Attributes:
        axes: Font size for axis labels and tick labels in points.
        text: Font size for general text elements in points.
    """
    axes: float
    text: float

    def __post_init__(self) -> None:
        """Post-initialization checks for font sizes.
        
        Raises:
            ValueError: If any font size is negative.
        """
        if self.axes < 0 or self.text < 0:
            raise ValueError("Font sizes must be positive.")

@dataclass
class Dimensions:
    """Stores width and height dimensions.
    
    Attributes:
        width: Width dimension in centimeters.
        height: Height dimension in centimeters.
    """
    width: float
    height: float

    def __post_init__(self) -> None:
        """Post-initialization checks for dimensions.
        
        Raises:
            ValueError: If width or height is negative.
        """
        if self.width < 0 or self.height < 0:
            raise ValueError("Dimensions must be positive.")

@dataclass
class Margins:
    """Stores margin sizes for all sides of a panel.
    
    Attributes:
        top: Top margin in centimeters.
        bottom: Bottom margin in centimeters.
        left: Left margin in centimeters.
        right: Right margin in centimeters.
    """
    top: float
    bottom: float
    left: float
    right: float

    def __post_init__(self) -> None:
        """Post-initialization checks for margins.
        
        Raises:
            ValueError: If any margin value is negative.
        """
        if self.top < 0 or self.bottom < 0 or self.left < 0 or self.right < 0:
            raise ValueError("Margins must be non-negative.")

@dataclass
class AxSeparation:
    """Stores separation distances between adjacent axes.
    
    Attributes:
        x: Horizontal separation between adjacent axes in centimeters.
        y: Vertical separation between adjacent axes in centimeters.
    """
    x: float = 0.0
    y: float = 0.0

    def __post_init__(self) -> None:
        """Post-initialization checks for axis separation.
        
        Raises:
            ValueError: If x or y separation is negative.
        """
        if self.x < 0 or self.y < 0:
            raise ValueError("Axis separation must be non-negative.")

@dataclass
class PanelConfig:
    """Configuration for a figure panel
    
    Attributes:
        panel_dimensions_cm: Overall panel dimensions in centimeters.
        panel_margins_cm: Panel margin sizes in centimeters.
        font_sizes_pt: Font sizes for different figure elements in points.
        ax_separation_cm: Separation between adjacent axes in centimeters.
    """
    panel_dimensions_cm: Dimensions
    panel_margins_cm: Margins
    font_sizes_pt: FontSizes
    ax_separation_cm: AxSeparation = field(default_factory=AxSeparation)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PanelConfig":
        """Creates a PanelConfig instance from a dictionary.
        
        Args:
            data: Dictionary containing panel configuration parameters.
                Must include 'panel_dimensions_cm' and 'panel_margins_cm', and
                'font_sizes_pt' keys. Optional keys are 'ax_separation_cm'.
        
        Returns:
            PanelConfig: A new PanelConfig instance with the specified configuration.
            
        Raises:
            KeyError: If any required configuration keys are missing.
        """
        return cls(
            panel_dimensions_cm=Dimensions(**data["panel_dimensions_cm"]),
            panel_margins_cm=Margins(**data["panel_margins_cm"]),
            font_sizes_pt=FontSizes(**data["font_sizes_pt"]),
            ax_separation_cm=AxSeparation(**data.get("ax_separation_cm", {})),
        )


def override_config(base: dict[str, Any], updates: dict[str, Any]) -> dict[str, Any]:
    """Overrides a base configuration with update values.
    
    Supports special string formats for relative updates:
    - "+=X": Add X to the current value
    - "-=X": Subtract X from the current value
    - "*X": Multiply current value by X
    - "=X": Set value to X (same as providing X directly)
    
    Args:
        base: Base configuration dictionary to be updated.
        updates: Dictionary with values to override in the base configuration.
    
    Returns:
        Updated configuration dictionary.
    
    Raises:
        ValueError: If an override string has invalid format.
    """
    def _interpret(value: Any, current: float) -> Any:
        """Interprets update values, handling special string formats.
        
        Args:
            value: The update value, possibly containing special format strings.
            current: The current value that might be modified.
            
        Returns:
            The interpreted value after applying any operations.
            
        Raises:
            ValueError: If the string format is invalid.
        """
        if isinstance(value, int | float):
            return value
        if isinstance(value, str):
            try:
                if value.startswith("+="):
                    return current + float(value[2:])
                elif value.startswith("-="):
                    return current - float(value[2:])
                elif value.startswith("*"):
                    return current * float(value[1:])
                elif value.startswith("="):
                    return float(value[1:])
                return float(value)
            except ValueError as e:
                raise ValueError(f"Invalid override format: {value}") from e
        return value

    def _recursive_merge(
        base_dict: dict[str, Any], 
        override_dict: dict[str, Any]
    ) -> dict[str, Any]:
        """Recursively merges two dictionaries, applying value interpretation.
        
        Args:
            base_dict: Base dictionary to merge into.
            override_dict: Dictionary with values to override in the base.
            
        Returns:
            Merged dictionary with interpreted values.
            
        Raises:
            KeyError: If trying to override a base key that doesn't exist.
        """
        result = copy.deepcopy(base_dict)
        for key, val in override_dict.items():
            if key not in result:
                raise KeyError(f"Cannot override non-existent key: {key}")
            
            if isinstance(val, dict) and isinstance(result[key], dict):
                result[key] = _recursive_merge(result[key], val)
            else:
                result[key] = _interpret(val, result[key])
        return result

    return _recursive_merge(base, updates)
