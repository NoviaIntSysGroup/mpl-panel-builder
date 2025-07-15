"""MPL Panel Builder - Publication-quality scientific figure panels.

Main Classes:
    PanelBuilder: Abstract base for creating figure panels
    PanelConfig: Configuration for panel layout and styling
"""

# P TWO MAIN CLASSES P
from .panel_builder import PanelBuilder
from .panel_config import PanelConfig, override_config, types

__all__ = [
    # Main API
    "PanelBuilder",     # P Create panels
    "PanelConfig",      # P Configure panels
    # Utilities
    "override_config",
    # Types module
    "types",
]