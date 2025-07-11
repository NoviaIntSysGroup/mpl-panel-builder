""" This example depicts config keys with three custom panels.

The script defines the following subclasses of :class:`PanelBuilder`:
- DimPanelDemo: 1 by 1 panel showing panel dimensions
- MarginPanelDemo: 1 by 1 panel illustrating panel margins
- FontSizePanelDemo: 1 by 1 panel demonstrating configured font sizes
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import numpy as np
from matplotlib.axes import Axes

# Add the project root to sys.path to allow importing helpers module
sys.path.append(str(Path(__file__).parent.parent.parent.absolute()))
from examples.helpers import get_logger, get_project_root
from mpl_panel_builder.mpl_helpers import cm_to_fig_rel, create_full_figure_axes
from mpl_panel_builder.panel_builder import PanelBuilder

logger = get_logger(__name__)

# Define panel configuration
margin = 1
project_root = get_project_root()
current_dir = Path(__file__).parent
example_name = current_dir.name
config: dict[str, Any] = {
    # Required keys (no default values)
    "panel_dimensions": {"width_cm": 6.0, "height_cm": 5.0},
    "panel_margins": {
        "left_cm": margin,
        "right_cm": margin,
        "top_cm": margin,
        "bottom_cm": margin,
    },
    "font_sizes": {"axes_pt": 8, "text_pt": 6},
    # Optional keys (with default values)
    "panel_output": {
        "directory": project_root / "outputs" / example_name / "panels",
        "format": "pdf",
    },
    # Custom keys that are not part of the PanelBuilder class
    # but that we want to share across panels
    "plot_styles": {"config": "k:", "data": "b-"},
}

# Create output directory if it doesn't exist
config["panel_output"]["directory"].mkdir(parents=True, exist_ok=True)

# Example specific helper functions
def _plot_sinusoid(ax: Axes, style: str = "b-") -> None:
    """Plot a simple sinusoid.

    Args:
        ax: Axes to plot the sinusoid on.
    """

    x = np.linspace(0, 5 * np.pi, 100)
    y = np.sin(x)
    ax.plot(x, y, style, label="text")
    ax.set(xticks=[], yticks=[])
    for spine in ax.spines.values():
        spine.set_visible(True)


class DimPanelDemo(PanelBuilder):
    """1 by 1 panel showing panel dimensions."""

    _n_cols = 1
    _n_rows = 1
    _panel_name = "dim_panel"

    def build_panel(self) -> None:
        """Create custom content for the panel."""

        _plot_sinusoid(self.axs[0][0], self.config.plot_styles.data)

        delta = 0.005  # Small delta to avoid overlap with panel border
        ax_panel = create_full_figure_axes(self.fig)
        ax_panel.plot([0, 1], [delta, delta], self.config.plot_styles.config)
        ax_panel.plot([delta, delta], [0, 1], self.config.plot_styles.config)

        padding_rel_x = cm_to_fig_rel(self.fig, margin / 2, "width")
        padding_rel_y = cm_to_fig_rel(self.fig, margin / 2, "height")
        shared_text_args: dict[str, Any] = {
            "ha": "center",
            "va": "center",
            "fontsize": self.config.font_sizes.axes_pt,
        }
        self.fig.text(0.5, padding_rel_y, "width", **shared_text_args)
        self.fig.text(padding_rel_x, 0.5, "height", rotation=90, **shared_text_args)


class MarginPanelDemo(PanelBuilder):
    """1 by 1 panel illustrating panel margins."""

    _n_cols = 1
    _n_rows = 1
    _panel_name = "margin_panel"

    def build_panel(self) -> None:
        """Create custom content for the panel."""

        _plot_sinusoid(self.axs[0][0])

        margins_cm = self.config.panel_margins
        dims_cm = self.config.panel_dimensions
        left_margin = margins_cm.left_cm / dims_cm.width_cm
        right_margin = margins_cm.right_cm / dims_cm.width_cm
        top_margin = margins_cm.top_cm / dims_cm.height_cm
        bottom_margin = margins_cm.bottom_cm / dims_cm.height_cm

        ax_panel = create_full_figure_axes(self.fig)
        ax_panel.plot([0, 1], [bottom_margin, bottom_margin], "k:")
        ax_panel.plot([left_margin, left_margin], [0, 1], "k:")
        ax_panel.plot([1 - right_margin, 1 - right_margin], [0, 1], "k:")
        ax_panel.plot([0, 1], [1 - top_margin, 1 - top_margin], "k:")

        shared_text_args: dict[str, Any] = {
            "ha": "center",
            "va": "center",
            "fontsize": self.config.font_sizes.axes_pt,
        }
        self.fig.text(0.5, bottom_margin / 2, "bottom", **shared_text_args)
        self.fig.text(0.5, 1 - top_margin / 2, "top", **shared_text_args)
        self.fig.text(left_margin / 2, 0.5, "left", rotation=90, **shared_text_args)
        self.fig.text(
            1 - right_margin / 2,
            0.5,
            "right",
            rotation=90,
            **shared_text_args,
        )


class FontSizePanelDemo(PanelBuilder):
    """1 by 1 panel demonstrating configured font sizes."""

    _n_cols = 1
    _n_rows = 1
    _panel_name = "font_size_panel"

    def build_panel(self) -> None:
        """Create custom content for the panel."""

        _plot_sinusoid(self.axs[0][0])
        self.axs[0][0].set(
            xlabel="axes",
            ylabel="axes",
            title="axes",
        )
        self.axs[0][0].legend(loc="lower right")
        sample_text = "text\ntext\ntext\ntext"
        self.axs[0][0].text(0.1, -0.9, sample_text, va="bottom", ha="left")


if __name__ == "__main__":
    builders = [
        DimPanelDemo,
        MarginPanelDemo,
        FontSizePanelDemo,
    ]

    for builder_class in builders:
        logger.info("Creating panel with class: %s", builder_class.__name__)
        builder = builder_class(config)
        builder()
        logger.info(
            "Panel created and saved to %s", 
            config["panel_output"]["directory"]
        )
