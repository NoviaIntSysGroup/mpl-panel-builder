"""Main panel configuration class."""

from dataclasses import MISSING, dataclass, field, fields, is_dataclass
from pathlib import Path
from typing import Any

import yaml

from .base import FrozenConfigBase
from .types.axes import AxesSpacing, PanelMargins
from .types.features import ColorBar, ScaleBar, TextAnnotation
from .types.figure import DebugPanel, PanelDimensions
from .types.output import PanelOutput
from .types.styles import FontSizes, LineStyle


@dataclass(frozen=True)
class PanelConfig(FrozenConfigBase):
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

    panel_dimensions: PanelDimensions = field(
        metadata={"description": "Overall panel dimensions"}
    )
    panel_margins: PanelMargins = field(metadata={"description": "Panel margin sizes"})
    font_sizes: FontSizes = field(
        metadata={"description": "Font sizes for different figure elements"}
    )
    axes_separation: AxesSpacing = field(
        default_factory=AxesSpacing,
        metadata={"description": "Separation between adjacent axes"},
    )
    line_style: LineStyle = field(
        default_factory=LineStyle,
        metadata={"description": "Line and marker styling configuration"},
    )
    scalebar_config: ScaleBar = field(
        default_factory=ScaleBar,
        metadata={"description": "Scale bar configuration"},
    )
    colorbar_config: ColorBar = field(
        default_factory=ColorBar,
        metadata={"description": "Color bar configuration"},
    )
    description_config: TextAnnotation = field(
        default_factory=TextAnnotation,
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
    def _classify_fields(cls, cls_inner: Any = None) -> tuple[list[Any], list[Any]]:
        """Classify fields into required and optional categories.
        
        Args:
            cls_inner: The dataclass to analyze (defaults to cls if not provided).
            
        Returns:
            Tuple of (required_fields, optional_fields) lists.
        """
        if cls_inner is None:
            cls_inner = cls
            
        config_fields = fields(cls_inner)
        required_fields = [
            f for f in config_fields
            if f.default is MISSING and f.default_factory is MISSING
            and not f.name.startswith("_")
        ]
        optional_fields = [
            f for f in config_fields
            if f not in required_fields and not f.name.startswith("_")
        ]
        return required_fields, optional_fields

    @classmethod
    def _get_field_description(cls, field_obj: Any) -> str:
        """Get the description for a field from its metadata."""
        return field_obj.metadata.get("description", "No description available")

    @classmethod
    def _get_default_value(cls, field_obj: Any) -> Any:
        """Get the default value for a field, or None if no default."""
        if field_obj.default is not MISSING:
            return field_obj.default
        elif field_obj.default_factory is not MISSING:
            return field_obj.default_factory()
        return None

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
        def _format_field_info(f: Any, level: int = 0) -> str:
            """Format information about a dataclass field."""
            indent = "  " * level
            type_str = f.type.__name__ if hasattr(f.type, "__name__") else str(f.type)

            # Get description from metadata
            description = cls._get_field_description(f)

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

        header = "PanelConfig Configuration Reference\n" + "=" * 45 + "\n\n"

        # Separate required and optional fields
        required_fields, optional_fields = cls._classify_fields()

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

    @classmethod
    def save_template_config(
        cls,
        filepath: str | Path = "config_template.yaml",
        include_optional: bool = True,
        include_descriptions: bool = True,
        top_level_key: str = "panel_config",
    ) -> None:
        """Save a template YAML configuration file with defaults and placeholders.

        Args:
            filepath: Path to save the template file.
            include_optional: Whether to include optional fields with defaults.
            include_descriptions: Whether to include field descriptions as comments.
            top_level_key: Top-level key to wrap the configuration in.
        """

        def _build_template_dict(cls_inner: Any) -> dict[str, Any]:
            """Build a template dictionary for a dataclass."""
            template = {}
            
            for f in fields(cls_inner):
                if f.name.startswith("_"):  # Skip private fields
                    continue
                
                if is_dataclass(f.type):
                    # Recursively build nested template
                    template[f.name] = _build_template_dict(f.type)
                else:
                    # Get default value or use placeholder
                    default_value = cls._get_default_value(f)
                    if default_value is not None:
                        template[f.name] = default_value
                    else:
                        # Use placeholder comment for required fields
                        template[f.name] = f"# TODO: Set {f.name.replace('_', ' ')}"
            
            return template

        def _add_comments_to_yaml(template_dict: dict[str, Any], cls_inner: Any) -> str:
            """Convert template dict to YAML with comments."""
            # First, separate required and optional fields
            required_fields, optional_fields = cls._classify_fields(cls_inner)
            
            lines = []
            
            # Add header comments
            lines.append("# Generated template for mpl-panel-builder configuration")
            lines.append(
                f'# Load with: config_dict = yaml.safe_load(file)["{top_level_key}"]'
            )
            lines.append("# Then: panel_config = PanelConfig.from_dict(config_dict)")
            lines.append("")
            lines.append(f"{top_level_key}:")
            
            if required_fields:
                lines.append("  # === REQUIRED FIELDS ===")
                for f in required_fields:
                    if include_descriptions:
                        description = cls._get_field_description(f)
                        if description != "No description available":
                            lines.append(f"  # {description}")
                    lines.append(f"  {f.name}:")
                    
                    if is_dataclass(f.type):
                        # Add nested fields
                        nested_dict = template_dict[f.name]
                        nested_yaml = yaml.dump(
                            nested_dict, default_flow_style=False, sort_keys=False
                        )
                        for line in nested_yaml.strip().split('\n'):
                            lines.append(f"    {line}")
                    else:
                        lines.append(f"    {template_dict[f.name]}")
                    lines.append("")
            
            if optional_fields and include_optional:
                if required_fields:
                    lines.append("  # === OPTIONAL FIELDS ===")
                for f in optional_fields:
                    if include_descriptions:
                        description = cls._get_field_description(f)
                        if description != "No description available":
                            lines.append(f"  # {description}")
                    lines.append(f"  {f.name}:")
                    
                    if is_dataclass(f.type):
                        # Add nested fields
                        nested_dict = template_dict[f.name]
                        nested_yaml = yaml.dump(
                            nested_dict, default_flow_style=False, sort_keys=False
                        )
                        for line in nested_yaml.strip().split('\n'):
                            lines.append(f"    {line}")
                    else:
                        lines.append(f"    {template_dict[f.name]}")
                    lines.append("")
            
            # Add custom fields section
            lines.append("  # === CUSTOM FIELDS ===")
            lines.append("  # Add any custom configuration below")
            lines.append("  # colors:")
            lines.append("  #   primary: [0.2, 0.4, 0.8]")
            lines.append("  #   secondary: [0.8, 0.2, 0.4]")
            
            return "\n".join(lines)

        # Build the template dictionary
        template_dict = _build_template_dict(cls)
        
        # Generate YAML content with comments
        yaml_content = _add_comments_to_yaml(template_dict, cls)
        
        # Write to file
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w') as f:
            f.write(yaml_content)