"""Configuration type definitions."""

from .axes import AxesSpacing, PanelMargins
from .features import ColorBar, ScaleBar, TextAnnotation
from .figure import DebugPanel, PanelDimensions
from .output import PanelOutput
from .styles import FontSizes, LineStyle

__all__ = [
    "AxesSpacing",
    "ColorBar",
    "DebugPanel",
    # Styling types
    "FontSizes",
    "LineStyle",
    # Figure types
    "PanelDimensions",
    # Axes types
    "PanelMargins",
    # Output types
    "PanelOutput",
    # Feature types
    "ScaleBar",
    "TextAnnotation",
]