"""Styling configuration types."""

from dataclasses import dataclass, field
from typing import Any

from ..base import FrozenConfigBase


@dataclass(frozen=True)
class StyleConfig(FrozenConfigBase):
    """Matplotlib styling configuration with theme support.

    Attributes:
        theme: Theme name for predefined style templates ('default' or 'none').
        rc_params: Custom rcParams that override theme defaults.
    """

    theme: str = field(
        default="default",
        metadata={"description": "Theme name: 'default' or 'none'"}
    )
    rc_params: dict[str, Any] = field(
        default_factory=dict,
        metadata={"description": "Custom rcParams that override theme defaults"}
    )

    def __post_init__(self) -> None:
        """Post-initialization checks for style configuration.

        Raises:
            ValueError: If theme is not 'default' or 'none'.
        """
        if self.theme not in ["default", "none"]:
            raise ValueError("Theme must be 'default' or 'none'")