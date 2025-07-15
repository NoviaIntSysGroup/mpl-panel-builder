"""Style management for panels."""

from typing import Any

from ..panel_config import PanelConfig


class StyleManager:
    """Manages styling for panels."""

    def __init__(self, config: PanelConfig):
        """Initialize style manager.
        
        Args:
            config: Panel configuration object.
        """
        self.config = config

    def get_default_style_rc(self) -> dict[str, Any]:
        """Returns a style dictionary (rcParams) for use in rc_context.

        This method constructs Matplotlib style settings based on the config
        for font sizes and visual aesthetics for article-style figures.

        Returns:
            Dict[str, Any]: A style dictionary for matplotlib.rc_context, or empty 
                dict if font sizes are not defined in config.
        """
        axes_font_size = self.config.font_sizes.axes_pt
        text_font_size = self.config.font_sizes.text_pt

        return {

            # Figure appearance
            "figure.facecolor": "white",

            # Axes appearance
            "axes.facecolor": "none",
            "axes.spines.right": False,
            "axes.spines.top": False,
            "axes.titlepad": 4,

            # Font sizes
            "font.size": text_font_size,
            "axes.titlesize": axes_font_size,
            "axes.labelsize": axes_font_size,
            "xtick.labelsize": axes_font_size,
            "ytick.labelsize": axes_font_size,
            "figure.titlesize": axes_font_size,
            "legend.fontsize": text_font_size,

            # Line styles
            "lines.linewidth": self.config.line_style.line_width_pt,
            "lines.markersize": self.config.line_style.marker_size_pt,

            # Legend appearance
            "legend.frameon": True,
            "legend.framealpha": 0.6,
            "legend.edgecolor": (1, 1, 1, 0.5),
            "legend.handlelength": 1.0,
            "legend.handletextpad": 0.7,
            "legend.labelspacing": 0.4,
            "legend.columnspacing": 1.0,
        }
    
