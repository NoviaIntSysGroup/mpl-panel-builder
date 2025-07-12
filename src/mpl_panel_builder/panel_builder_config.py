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
                # Only wrap dictionaries with CustomConfigDotDict
                if isinstance(value, dict):
                    extra[key] = CustomConfigDotDict(value)
                else:
                    extra[key] = value

        # Create the frozen dataclass instance
        instance = cls(**declared)  # This triggers __post_init__ if defined

        # Inject _extra manually, bypassing frozen restriction
        object.__setattr__(instance, "_extra", extra)
        return instance


@dataclass(frozen=True)
class FontSizes(FrozenConfigBase):
    """Stores font sizes for different figure elements.

    Attributes:
        axes_pt: Font size for axis labels and tick labels in points.
        text_pt: Font size for general text elements in points.
    """

    axes_pt: float = field(
        metadata={"description": "Font size for axis labels and tick labels in points"}
    )
    text_pt: float = field(
        metadata={"description": "Font size for general text elements in points"}
    )

    def __post_init__(self) -> None:
        """Post-initialization checks for font sizes.

        Raises:
            ValueError: If any font size is negative.
        """
        if self.axes_pt < 0 or self.text_pt < 0:
            raise ValueError("Font sizes must be positive.")


@dataclass(frozen=True)
class Dimensions(FrozenConfigBase):
    """Stores width and height dimensions.

    Attributes:
        width_cm: Width dimension in centimeters.
        height_cm: Height dimension in centimeters.
    """

    width_cm: float = field(metadata={"description": "Width dimension in centimeters"})
    height_cm: float = field(
        metadata={"description": "Height dimension in centimeters"}
    )

    def __post_init__(self) -> None:
        """Post-initialization checks for dimensions.

        Raises:
            ValueError: If width or height is negative.
        """
        if self.width_cm < 0 or self.height_cm < 0:
            raise ValueError("Dimensions must be positive.")


@dataclass(frozen=True)
class Margins(FrozenConfigBase):
    """Stores margin sizes for all sides of a panel.

    Attributes:
        top_cm: Top margin in centimeters.
        bottom_cm: Bottom margin in centimeters.
        left_cm: Left margin in centimeters.
        right_cm: Right margin in centimeters.
    """

    top_cm: float = field(metadata={"description": "Top margin in centimeters"})
    bottom_cm: float = field(metadata={"description": "Bottom margin in centimeters"})
    left_cm: float = field(metadata={"description": "Left margin in centimeters"})
    right_cm: float = field(metadata={"description": "Right margin in centimeters"})

    def __post_init__(self) -> None:
        """Post-initialization checks for margins.

        Raises:
            ValueError: If any margin value is negative.
        """
        if (
            self.top_cm < 0
            or self.bottom_cm < 0
            or self.left_cm < 0
            or self.right_cm < 0
        ):
            raise ValueError("Margins must be non-negative.")


@dataclass(frozen=True)
class AxesSeparation(FrozenConfigBase):
    """Stores separation distances between adjacent axes.

    Attributes:
        x_cm: Horizontal separation between adjacent axes in centimeters.
        y_cm: Vertical separation between adjacent axes in centimeters.
    """

    x_cm: float = field(
        default=0.0,
        metadata={
            "description": "Horizontal separation between adjacent axes in centimeters"
        },
    )
    y_cm: float = field(
        default=0.0,
        metadata={
            "description": "Vertical separation between adjacent axes in centimeters"
        },
    )

    def __post_init__(self) -> None:
        """Post-initialization checks for axis separation.

        Raises:
            ValueError: If x or y separation is negative.
        """
        if self.x_cm < 0 or self.y_cm < 0:
            raise ValueError("Axis separation must be non-negative.")


@dataclass(frozen=True)
class LineStyle(FrozenConfigBase):
    """Stores line and marker styling configuration.

    Attributes:
        line_width_pt: Width of lines in points.
        marker_size_pt: Size of markers in points.
    """

    line_width_pt: float = field(
        default=1.0, metadata={"description": "Width of lines in points"}
    )
    marker_size_pt: float = field(
        default=4.0, metadata={"description": "Size of markers in points"}
    )

    def __post_init__(self) -> None:
        """Post-initialization checks for line style.

        Raises:
            ValueError: If line_width_pt or marker_size_pt is negative.
        """
        if self.line_width_pt <= 0 or self.marker_size_pt <= 0:
            raise ValueError("Line width and marker size must be positive.")


@dataclass(frozen=True)
class ScaleBarConfig(FrozenConfigBase):
    """Stores scale bar configuration.

    Attributes:
        separation_cm: Separation between the scale bar and the axes in centimeters.
        offset_cm: Distance from the axes edge to the scale bar in centimeters.
        text_offset_cm: Distance from the scale bar to the label in centimeters.
    """

    separation_cm: float = field(
        default=0.2,
        metadata={
            "description": (
                "Separation between the scale bar and the axes in centimeters"
            )
        },
    )
    offset_cm: float = field(
        default=0.2,
        metadata={
            "description": "Distance from the axes edge to the scale bar in centimeters"
        },
    )
    text_offset_cm: float = field(
        default=0.1,
        metadata={
            "description": "Distance from the scale bar to the label in centimeters"
        },
    )


@dataclass(frozen=True)
class ColorBarConfig(FrozenConfigBase):
    """Stores color bar configuration.

    Attributes:
        width_cm: Width of the color bar in centimeters.
        separation_cm: Separation between the color bar and the axes in centimeters.
    """

    width_cm: float = field(
        default=0.3, metadata={"description": "Width of the color bar in centimeters"}
    )
    separation_cm: float = field(
        default=0.2,
        metadata={
            "description": (
                "Separation between the color bar and the axes in centimeters"
            )
        },
    )

    def __post_init__(self) -> None:
        """Post-initialization checks for color bar.

        Raises:
            ValueError: If width_cm or separation_cm is negative.
        """
        if self.width_cm <= 0 or self.separation_cm < 0:
            raise ValueError(
                "Color bar width must be positive and separation must be non-negative."
            )


@dataclass(frozen=True)
class DebugPanel(FrozenConfigBase):
    """Stores debug panel configuration.

    Attributes:
        show: Whether to show the debug grid lines.
        grid_resolution_cm: Resolution of the debug grid in centimeters.
    """

    show: bool = field(
        default=False, metadata={"description": "Whether to show the debug grid lines"}
    )
    grid_resolution_cm: float = field(
        default=0.5,
        metadata={"description": "Resolution of the debug grid in centimeters"},
    )

    def __post_init__(self) -> None:
        """Post-initialization checks for debug panel.

        Raises:
            ValueError: If grid_resolution_cm is negative.
        """
        if self.grid_resolution_cm <= 0:
            raise ValueError("Grid resolution must be positive.")


@dataclass(frozen=True)
class DescriptionConfig(FrozenConfigBase):
    """Stores description text configuration.

    Attributes:
        margin_cm: Margin from axes edge to description text in centimeters.
    """

    margin_cm: float = field(
        default=0.2,
        metadata={
            "description": "Margin from axes edge to description text in centimeters"
        },
    )

    def __post_init__(self) -> None:
        """Post-initialization checks for description config.

        Raises:
            ValueError: If margin_cm is negative.
        """
        if self.margin_cm < 0:
            raise ValueError("Description margin must be non-negative.")


@dataclass(frozen=True)
class PanelOutput(FrozenConfigBase):
    """Stores output configuration for panels.

    Attributes:
        directory: Directory to save the panel.
        format: Format to save the panel.
        dpi: DPI of the panel (if valid).
    """

    directory: str | None = field(
        default=None,
        metadata={
            "description": "Directory to save the panel (None for current directory)"
        },
    )
    format: str = field(
        default="pdf",
        metadata={"description": "Format to save the panel (pdf, png, etc.)"},
    )
    dpi: int = field(
        default=600, metadata={"description": "DPI for raster formats (dots per inch)"}
    )

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
        panel_dimensions: Overall panel dimensions in centimeters.
        panel_margins: Panel margin sizes in centimeters.
        font_sizes: Font sizes for different figure elements in points.
        axes_separation: Separation between adjacent axes in centimeters.
        line_style: Line and marker styling configuration.
        scalebar_config: Scale bar configuration.
        colorbar_config: Color bar configuration.
        description_config: Description text configuration.
        debug_panel: Debug panel configuration.
        panel_output: Output configuration for panels.
    """

    panel_dimensions: Dimensions = field(
        metadata={"description": "Overall panel dimensions"}
    )
    panel_margins: Margins = field(metadata={"description": "Panel margin sizes"})
    font_sizes: FontSizes = field(
        metadata={"description": "Font sizes for different figure elements"}
    )
    axes_separation: AxesSeparation = field(
        default_factory=AxesSeparation,
        metadata={"description": "Separation between adjacent axes"},
    )
    line_style: LineStyle = field(
        default_factory=LineStyle,
        metadata={"description": "Line and marker styling configuration"},
    )
    scalebar_config: ScaleBarConfig = field(
        default_factory=ScaleBarConfig,
        metadata={"description": "Scale bar configuration"},
    )
    colorbar_config: ColorBarConfig = field(
        default_factory=ColorBarConfig,
        metadata={"description": "Color bar configuration"},
    )
    description_config: DescriptionConfig = field(
        default_factory=DescriptionConfig,
        metadata={"description": "Description text configuration"},
    )
    debug_panel: DebugPanel = field(
        default_factory=DebugPanel,
        metadata={"description": "Debug panel configuration"},
    )
    panel_output: PanelOutput = field(
        default_factory=PanelOutput,
        metadata={"description": "Output configuration for panels"},
    )

    @classmethod
    def describe_config(
        cls, show_types: bool = True, show_defaults: bool = True
    ) -> str:
        """Generate hierarchical documentation of all configuration keys.

        Args:
            show_types: Whether to include type information in the output.
            show_defaults: Whether to include default values in the output.

        Returns:
            A formatted string describing all configuration options.
        """
        from dataclasses import MISSING

        def _format_field_info(f: Any, level: int = 0) -> str:
            """Format information about a dataclass field."""
            indent = "  " * level
            type_str = f.type.__name__ if hasattr(f.type, "__name__") else str(f.type)

            # Get description from metadata
            description = f.metadata.get("description", "No description available")

            # Format type info
            type_info = f" ({type_str})" if show_types else ""

            # Format default info
            default_info = ""
            if show_defaults and f.default is not MISSING:
                default_info = f" [default: {f.default}]"

            return f"{indent}{f.name}{type_info}: {description}{default_info}"

        def _describe_dataclass(cls_inner: Any, level: int = 0) -> str:
            """Recursively describe a dataclass and its nested fields."""
            result = []

            for f in fields(cls_inner):
                if f.name.startswith("_"):  # Skip private fields
                    continue

                result.append(_format_field_info(f, level))

                # If the field type is a dataclass, recursively describe it
                if is_dataclass(f.type):
                    result.append(_describe_dataclass(f.type, level + 1))

            return "\n".join(result)

        header = "PanelBuilderConfig Configuration Reference\n" + "=" * 45 + "\n\n"

        # Separate required and optional fields
        config_fields = fields(cls)
        required_fields = [
            f
            for f in config_fields
            if f.default is MISSING
            and f.default_factory is MISSING
            and not f.name.startswith("_")
        ]
        optional_fields = [
            f
            for f in config_fields
            if f not in required_fields and not f.name.startswith("_")
        ]

        sections = []

        if required_fields:
            sections.append("Required Fields:")
            for f in required_fields:
                sections.append(_format_field_info(f))
                if is_dataclass(f.type):
                    sections.append(_describe_dataclass(f.type, 1))
            sections.append("")

        if optional_fields:
            sections.append("Optional Fields (with defaults):")
            for f in optional_fields:
                sections.append(_format_field_info(f))
                if is_dataclass(f.type):
                    sections.append(_describe_dataclass(f.type, 1))
            sections.append("")

        return header + "\n".join(sections)


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
        base_dict: dict[str, Any], override_dict: dict[str, Any]
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
