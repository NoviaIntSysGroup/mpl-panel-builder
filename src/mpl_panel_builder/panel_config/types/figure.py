"""Figure configuration types."""

from dataclasses import dataclass, field

from ..base import FrozenConfigBase


@dataclass(frozen=True)
class PanelDimensions(FrozenConfigBase):
    """Panel size specification in centimeters.
    
    Attributes:
        width_cm: Width dimension in centimeters.
        height_cm: Height dimension in centimeters.
    """
    
    width_cm: float = field(
        metadata={"description": "Width dimension in centimeters"}
    )
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