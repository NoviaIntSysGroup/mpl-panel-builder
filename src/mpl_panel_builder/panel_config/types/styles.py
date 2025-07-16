"""Styling configuration types."""

from dataclasses import dataclass, field
from typing import Any

from ..base import FrozenConfigBase


@dataclass(frozen=True)
class StyleConfig(FrozenConfigBase):
    """Matplotlib styling configuration with theme support.

    Attributes:
        theme: Theme name for predefined style templates ('white' or 'none').
        rc_params: Custom rcParams that override theme defaults.
    """

    theme: str = field(
        default="none",
        metadata={"description": "Theme name: 'white' or 'none'"}
    )
    rc_params: dict[str, Any] = field(
        default_factory=dict,
        metadata={"description": "Custom rcParams that override theme defaults"}
    )

    def __post_init__(self) -> None:
        """Post-initialization checks for style configuration.

        Raises:
            ValueError: If theme is not 'white' or 'none'.
        """
        if self.theme not in ["white", "none"]:
            raise ValueError("Theme must be 'white' or 'none'")