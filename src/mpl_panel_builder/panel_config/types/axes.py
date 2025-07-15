"""Axes layout configuration types."""

from dataclasses import dataclass, field

from ..base import FrozenConfigBase


@dataclass(frozen=True)
class PanelMargins(FrozenConfigBase):
    """Panel margin specification in centimeters.
    
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
class AxesSpacing(FrozenConfigBase):
    """Spacing between subplot axes in centimeters.
    
    Attributes:
        x_cm: Horizontal spacing between adjacent axes in centimeters.
        y_cm: Vertical spacing between adjacent axes in centimeters.
    """
    
    x_cm: float = field(
        default=0.0,
        metadata={
            "description": "Horizontal spacing between adjacent axes in centimeters"
        }
    )
    y_cm: float = field(
        default=0.0,
        metadata={
            "description": "Vertical spacing between adjacent axes in centimeters"
        }
    )
    
    def __post_init__(self) -> None:
        """Post-initialization checks for axis spacing.

        Raises:
            ValueError: If x or y spacing is negative.
        """
        if self.x_cm < 0 or self.y_cm < 0:
            raise ValueError("Axis spacing must be non-negative.")