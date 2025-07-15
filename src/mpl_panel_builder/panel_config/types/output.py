"""Output configuration types."""

from dataclasses import dataclass, field

from ..base import FrozenConfigBase


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