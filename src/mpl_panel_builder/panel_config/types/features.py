"""Feature configuration types."""

from dataclasses import dataclass, field

from ..base import FrozenConfigBase


@dataclass(frozen=True)
class ScaleBar(FrozenConfigBase):
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
class ColorBar(FrozenConfigBase):
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
class TextAnnotation(FrozenConfigBase):
    """Stores text annotation configuration.

    Attributes:
        margin_cm: Margin from axes edge to text annotation in centimeters.
    """

    margin_cm: float = field(
        default=0.2,
        metadata={
            "description": "Margin from axes edge to text annotation in centimeters"
        },
    )

    def __post_init__(self) -> None:
        """Post-initialization checks for text annotation config.

        Raises:
            ValueError: If margin_cm is negative.
        """
        if self.margin_cm < 0:
            raise ValueError("Text annotation margin must be non-negative.")


