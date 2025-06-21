import copy
from dataclasses import dataclass, field, fields, is_dataclass
from typing import Any, TypeVar

T = TypeVar("T", bound="FrozenConfigBase")


class CustomConfigDotDict(dict[str, Any]):
    """A read-only dictionary that can be accessed as an object with dot notation.
    
    This class is used to provide dot access to non-mandatory custom 
    configuration values. This allows for more flexible configuration, while
    still providing a consistent interface for all configuration values.
    """
    def __init__(self, d: dict[str, Any]) -> None:
        """Initializes the dictionary with the given values.
        
        Args:
            d: The dictionary to initialize the CustomConfigDotDict with.
        """
        super().__init__()
        for key, value in d.items():
            self[key] = self._wrap(value)

    def __getattr__(self, key: str) -> Any:
        """Returns the value for the given key.
        
        Args:
            key: The key to get the value for.
        """
        try:
            return self[key]
        except KeyError as e:
            raise AttributeError(f"Object has no attribute '{key}'") from e

    def __setattr__(self, key: str, value: Any) -> None:
        """Raises an error if the attribute is set.
        
        Args:
            key: The key to set the value for.
            value: The value to set.
        """
        raise AttributeError(f"Cannot modify read-only config attribute '{key}'")

    def __delattr__(self, key: str) -> None:
        """Raises an error if the attribute is deleted.
        
        Args:
            key: The key to delete.
        """
        raise AttributeError(f"Cannot delete read-only config attribute '{key}'")

    def _wrap(self, value: Any) -> Any:
        """Wraps the value in a CustomConfigDotDict if it is a dictionary.
        
        Args:
            value: The value to wrap.
        """
        if isinstance(value, dict):
            return CustomConfigDotDict(value)
        return value


@dataclass(frozen=True)
class FrozenConfigBase:
    """Base class for immutable config objects with dot access to extra fields.
    
    This class is used to create immutable config objects with dot access to extra 
    fields. The extra fields are stored in the _extra attribute, which is a dictionary
    of key-value pairs.
    """
    _extra: dict[str, Any] = field(default_factory=dict, init=False, repr=False)

    def __getattr__(self, name: str) -> Any:
        """Returns the value for the given key.
        
        Args:
            name: The key to get the value for.
        """
        # Safely access _extra only if initialized
        extra = object.__getattribute__(self, "__dict__").get("_extra", {})
        if name in extra:
            return extra[name]
        raise AttributeError(f"Object has no attribute '{name}'")

    @classmethod
    def from_dict(cls: type[T], data: dict[str, Any]) -> T:
        """Creates a FrozenConfigBase instance from a dictionary.
        
        Args:
            data: The dictionary to create the instance from.

        Returns:
            The FrozenConfigBase instance.
        """
        field_names = {f.name for f in fields(cls)}
        declared = {}
        extra = {}

        for key, value in data.items():
            # If the key is a declared field, add it to the declared dictionary
            if key in field_names:
                field_type = next(f.type for f in fields(cls) if f.name == key)

                # If the field is a dataclass, convert the value to the dataclass type
                if is_dataclass(field_type) and isinstance(value, dict):
                    # The field_type has from_dict as it inherits from FrozenConfigBase
                    value = field_type.from_dict(value)  # type: ignore

                declared[key] = value

            # If the key is not a declared field, add it to the extra dictionary    
            else:
                extra[key] = CustomConfigDotDict(value)

        # Create the frozen dataclass instance
        instance = cls(**declared)  # This triggers __post_init__ if defined

        # Inject _extra manually, bypassing frozen restriction
        object.__setattr__(instance, "_extra", extra)
        return instance


@dataclass(frozen=True)
class FontSizes(FrozenConfigBase):
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


@dataclass(frozen=True)
class Dimensions(FrozenConfigBase):
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


@dataclass(frozen=True)
class Margins(FrozenConfigBase):
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


@dataclass(frozen=True)
class AxSeparation(FrozenConfigBase):
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
        

@dataclass(frozen=True)
class ScaleBar(FrozenConfigBase):
    """Stores scale bar configuration.
    
    Attributes:
        sep_cm: Separation between the scale bar and the axes in centimeters.
        offset_cm: Distance from the axes edge to the scale bar in centimeters.
        delta_text_cm: Distance from the scale bar to the label in centimeters.
    """
    sep_cm: float = 0.2
    offset_cm: float = 0.2
    delta_text_cm: float = 0.1


@dataclass(frozen=True)
class DebugPanel(FrozenConfigBase):
    """Stores debug panel configuration.
    
    Attributes:
        show: Whether to show the debug grid lines.
        grid_res_cm: Resolution of the debug grid in centimeters.
    """
    show: bool = False
    grid_res_cm: float = 0.5

    def __post_init__(self) -> None:
        """Post-initialization checks for debug panel.
        
        Raises:
            ValueError: If grid_res_cm is negative.
        """
        if self.grid_res_cm < 0:
            raise ValueError("Grid resolution must be non-negative.")

@dataclass(frozen=True)
class PanelOutput(FrozenConfigBase):
    """Stores output configuration for panels.
    
    Attributes:
        directory: Directory to save the panel.
        format: Format to save the panel.
        dpi: DPI of the panel (if valid).
    """
    directory: str | None = None
    format: str = "pdf"
    dpi: int = 600

    def __post_init__(self) -> None:
        """Post-initialization checks for panel output.
        
        Raises:
            ValueError: If dpi is negative.
        """
        if self.dpi < 0:
            raise ValueError("DPI must be positive.")


@dataclass(frozen=True)
class PanelBuilderConfig(FrozenConfigBase):
    """Read only configuration for PanelBuilder.
    
    This class is immutable and provides dot-access to all fields in a nested
    configuration dictionary. This includes both mandatory fields required by
    the PanelBuilder class and use-case specific optional fields.

    Attributes:
        panel_dimensions_cm: Overall panel dimensions in centimeters.
        panel_margins_cm: Panel margin sizes in centimeters.
        font_sizes_pt: Font sizes for different figure elements in points.
        ax_separation_cm: Separation between adjacent axes in centimeters.
        scale_bar_pos_cm: Position of the scale bar in centimeters.
        debug_panel: Debug panel configuration.
        panel_output: Output configuration for panels.
    """
    panel_dimensions_cm: Dimensions
    panel_margins_cm: Margins
    font_sizes_pt: FontSizes
    ax_separation_cm: AxSeparation = AxSeparation()
    scale_bar_pos_cm: ScaleBar = ScaleBar()
    debug_panel: DebugPanel = DebugPanel()
    panel_output: PanelOutput = PanelOutput()

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
