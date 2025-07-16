"""Style management for panels."""

from typing import Any, ClassVar, Protocol

from ..panel_config import PanelConfig


class StyleTheme(Protocol):
    """Protocol for style themes."""
    
    @property
    def name(self) -> str:
        """Theme name."""
        ...
    
    def get_rcparams(self) -> dict[str, Any]:
        """Get rcParams for this theme."""
        ...


class WhiteTheme:
    """Default theme."""
    
    name = "default"
    
    def get_rcparams(self) -> dict[str, Any]:
        """Get default theme rcParams."""
        return {
            # Figure appearance
            "figure.facecolor": "white",
            
            # Axes appearance
            "axes.facecolor": "white",
            "axes.spines.right": False,
            "axes.spines.top": False,
            "axes.titlepad": 4,
            
            # Font sizes
            "font.size": 6,
            "axes.titlesize": 8,
            "axes.labelsize": 8,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "figure.titlesize": 8,
            "legend.fontsize": 6,

            # Line styles
            "lines.linewidth": 1.0,
            "lines.markersize": 4.0,
            
            # Legend appearance
            "legend.frameon": True,
            "legend.framealpha": 0.6,
            "legend.edgecolor": "none",
            "legend.handlelength": 1.0,
            "legend.handletextpad": 0.7,
            "legend.labelspacing": 0.4,
            "legend.columnspacing": 1.0,
        }


class NoneTheme:
    """Empty theme - no default styling applied."""
    
    name = "none"
    
    def get_rcparams(self) -> dict[str, Any]:
        """Get empty rcParams - user must specify everything."""
        return {}


class StyleManager:
    """Enhanced style manager with theme support."""
    
    _themes: ClassVar[dict[str, StyleTheme]] = {
        "default": WhiteTheme(),
        "none": NoneTheme()
    }

    def __init__(self, config: PanelConfig):
        """Initialize style manager.
        
        Args:
            config: Panel configuration object.
        """
        self.config = config

    def get_style_rc(self) -> dict[str, Any]:
        """Returns a style dictionary (rcParams) for use in rc_context.

        This method constructs Matplotlib style settings by merging theme
        rcParams with user-provided rcParams (user takes precedence).

        Returns:
            Dict[str, Any]: A style dictionary for matplotlib.rc_context.
        """
        theme = self._themes[self.config.style.theme]
        base_params = theme.get_rcparams()
        user_params = self.config.style.rc_params
        return {**base_params, **user_params}  # User overrides theme
