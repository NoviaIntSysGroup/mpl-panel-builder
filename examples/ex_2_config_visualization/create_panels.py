""" This example depicts config keys with three custom panels.

The script defines the following subclasses of :class:`PanelBuilder`:
- DimPanelDemo: 1 by 1 panel showing panel dimensions
- MarginPanelDemo: 1 by 1 panel illustrating panel margins
- FontSizePanelDemo: 1 by 1 panel demonstrating configured font sizes
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
from matplotlib.axes import Axes

from mpl_panel_builder import PanelBuilder
from mpl_panel_builder.helpers import (
    cm_to_fig_rel,
    create_full_figure_axes,
    get_logger,
    setup_output_dir,
)

# Simple setup
example_name = Path(__file__).parent.name
output_dir = setup_output_dir(example_name)
logger = get_logger(example_name)

# Define panel configuration
margin = 1
config: dict[str, Any] = {
    # Required keys (no default values)
    "panel_dimensions": {"width_cm": 6.0, "height_cm": 5.0},
    "panel_margins": {
        "left_cm": margin,
        "right_cm": margin,
        "top_cm": margin,
        "bottom_cm": margin,
    },
    "style": {
        "rc_params": {
            "font.size": 8,
            "axes.titlesize": 8,
            "axes.labelsize": 8,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "legend.fontsize": 8,
        }
    },
    # Optional keys (with default values)
    "panel_output": {
        "directory": str(output_dir / "panels"),
        "format": "pdf",
    },
    # Custom keys that are not part of the PanelBuilder class
    # but that we want to share across panels
    "plot_styles": {"config": "k:", "data": "b-"},
}

# Create output directory if it doesn't exist
(output_dir / "panels").mkdir(parents=True, exist_ok=True)

# Example specific helper functions
def _plot_sinusoid(ax: Axes, style: str = "b-") -> None:
    """Plot a simple sinusoid.

    Args:
        ax: Axes to plot the sinusoid on.
    """

    x = np.linspace(0, 5 * np.pi, 100)
    y = np.sin(x)
    ax.plot(x, y, style, label="legend.fontsize")
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

        ax = self.axs[0][0]
        _plot_sinusoid(ax, self.config.plot_styles.data)

        delta = 0.005  # Small delta to avoid overlap with panel border
        ax_panel = create_full_figure_axes(self.fig)
        ax_panel.plot([0, 1], [delta, delta], self.config.plot_styles.config)
        ax_panel.plot([delta, delta], [0, 1], self.config.plot_styles.config)

        padding_rel_x = cm_to_fig_rel(self.fig, margin / 2, "width")
        padding_rel_y = cm_to_fig_rel(self.fig, margin / 2, "height")
        shared_text_args: dict[str, Any] = {
            "ha": "center",
            "va": "center",
            "fontsize": ax.xaxis.label.get_fontsize(),
        }
        self.fig.text(0.5, padding_rel_y, "width_cm", **shared_text_args)
        self.fig.text(padding_rel_x, 0.5, "height_cm", rotation=90, **shared_text_args)


class MarginPanelDemo(PanelBuilder):
    """1 by 1 panel illustrating panel margins."""

    _n_cols = 1
    _n_rows = 1
    _panel_name = "margin_panel"

    def build_panel(self) -> None:
        """Create custom content for the panel."""

        ax = self.axs[0][0]
        _plot_sinusoid(ax)

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
            "fontsize": ax.xaxis.label.get_fontsize(),
        }
        self.fig.text(0.5, bottom_margin / 2, "bottom_cm", **shared_text_args)
        self.fig.text(0.5, 1 - top_margin / 2, "top_cm", **shared_text_args)
        self.fig.text(left_margin / 2, 0.5, "left_cm", rotation=90, **shared_text_args)
        self.fig.text(
            1 - right_margin / 2,
            0.5,
            "right_cm",
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

        ax = self.axs[0][0]
        _plot_sinusoid(ax)
        ax.set(
            xlabel="axes.labelsize",
            ylabel="axes.labelsize",
            title="figure.titlesize",
        )
        ax.legend(loc="lower right")


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
