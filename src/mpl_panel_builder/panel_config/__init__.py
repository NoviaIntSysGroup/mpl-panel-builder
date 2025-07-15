"""Panel configuration system."""

# For advanced users who need access to type definitions
from . import types
from .base import DotDict
from .config import PanelConfig
from .utils import override_config

__all__ = [
    # For testing and advanced usage
    "DotDict",
    # Main API
    "PanelConfig",
    "override_config",
    "types",
]