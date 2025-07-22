"""MPL Panel Builder - Simplified function-based API."""

from . import features
from .config import (
    configure,
    get_config,
    print_template_config,
    reset_config,
)
from .panel import create_panel, save_panel, set_rc_style

__version__ = "2.0.0"

__all__ = [
    'configure',
    'create_panel',
    'features',
    'get_config',
    'print_template_config',
    'reset_config',
    'save_panel',
    'set_rc_style'
]