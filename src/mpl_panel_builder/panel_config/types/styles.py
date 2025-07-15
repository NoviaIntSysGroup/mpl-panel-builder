"""Styling configuration types."""

from dataclasses import dataclass, field

from ..base import FrozenConfigBase


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