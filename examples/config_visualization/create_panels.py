"""Demo script illustrating usage of :class:`PanelBuilder` subclasses."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import numpy as np

# Add the examples directory to sys.path to allow importing helpers module
sys.path.append(str(Path(__file__).parent.parent.absolute()))
from helpers import get_project_root
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from mpl_panel_builder.panel_builder import PanelBuilder

# Define panel configuration
margin = 1
project_root = get_project_root()
current_dir = Path(__file__).parent
example_name = current_dir.name
config = {
    "panel_dimensions_cm": {"width": 6.0, "height": 5.0},
    "panel_margins_cm": {
        "left": margin,
        "right": margin,
        "top": margin,
        "bottom": margin,
    },
    "font_sizes_pt": {"axes": 8, "text": 6},
    "ax_separation_cm": {"x": 0.5, "y": 0.5},
    "panel_output": {
        "directory": project_root / "outputs" / example_name / "panels",
        "format": "pdf",
        "dpi": 600,
    },
}

# Create output directory if it doesn't exist
config["panel_output"]["directory"].mkdir(parents=True, exist_ok=True)  # type: ignore

# Example specific helper functions

def add_full_panel_axes(fig: Figure) -> Axes:
    """Add an invisible axes covering the entire figure.

    Args:
        fig: Figure to add the axes to.

    Returns:
        The created axes.
    """

    ax = fig.add_axes((0.0, 0.0, 1.0, 1.0), facecolor="none", zorder=-1)
    ax.axis("off")
    ax.set(xlim=[0, 1], ylim=[0, 1])
    return ax


def plot_sinusoid(ax: Axes) -> None:
    """Plot a simple sinusoid.

    Args:
        ax: Axes to plot the sinusoid on.
    """

    x = np.linspace(0, 5 * np.pi, 100)
    y = np.sin(x)
    ax.plot(x, y, label="text")
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

        plot_sinusoid(self.axs[0][0])

        ax_panel = add_full_panel_axes(self.fig)
        ax_panel.plot([0, 1], [0.001, 0.001], "k:")
        ax_panel.plot([0.001, 0.001], [0, 1], "k:")

        padding_rel_x = self.cm_to_rel(margin / 2, "width")
        padding_rel_y = self.cm_to_rel(margin / 2, "height")
        shared_text_args: dict[str, Any] = {
            "ha": "center",
            "va": "center",
            "fontsize": self.config.font_sizes_pt.axes,
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

        plot_sinusoid(self.axs[0][0])

        margins_cm = self.config.panel_margins_cm
        dims_cm = self.config.panel_dimensions_cm
        left_margin = margins_cm.left / dims_cm.width
        right_margin = margins_cm.right / dims_cm.width
        top_margin = margins_cm.top / dims_cm.height
        bottom_margin = margins_cm.bottom / dims_cm.height

        ax_panel = add_full_panel_axes(self.fig)
        ax_panel.plot([0, 1], [bottom_margin, bottom_margin], "k:")
        ax_panel.plot([left_margin, left_margin], [0, 1], "k:")
        ax_panel.plot([1 - right_margin, 1 - right_margin], [0, 1], "k:")
        ax_panel.plot([0, 1], [1 - top_margin, 1 - top_margin], "k:")

        shared_text_args: dict[str, Any] = {
            "ha": "center",
            "va": "center",
            "fontsize": self.config.font_sizes_pt.axes,
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


class AxesSeparationPanelDemo(PanelBuilder):
    """2 by 2 panel showing axes separation."""

    _n_cols = 2
    _n_rows = 2
    _panel_name = "axes_separation_panel"

    def build_panel(self) -> None:
        """Create custom content for the panel."""

        for i in range(self.n_cols):
            for j in range(self.n_rows):
                plot_sinusoid(self.axs[i][j])

        ax_panel = add_full_panel_axes(self.fig)

        ax_00_x1 = self.axs[0][0].get_position().x1
        ax_01_x0 = self.axs[0][1].get_position().x0
        ax_panel.plot([ax_00_x1, ax_00_x1], [0, 1], "k:")
        ax_panel.plot([ax_01_x0, ax_01_x0], [0, 1], "k:")

        ax_00_y1 = self.axs[0][0].get_position().y0
        ax_10_y0 = self.axs[1][0].get_position().y1
        ax_panel.plot([0, 1], [ax_00_y1, ax_00_y1], "k:")
        ax_panel.plot([0, 1], [ax_10_y0, ax_10_y0], "k:")

        mid_x = 0.5 * (ax_01_x0 + ax_00_x1)
        mid_y = 0.5 * (ax_10_y0 + ax_00_y1)
        padding_rel_x = self.cm_to_rel(margin / 2, "width")
        padding_rel_y = self.cm_to_rel(margin / 2, "height")
        shared_text_args: dict[str, Any] = {
            "ha": "center",
            "va": "center",
            "fontsize": self.config.font_sizes_pt.axes,
        }
        self.fig.text(mid_x, padding_rel_y, "x", **shared_text_args)
        self.fig.text(padding_rel_x, mid_y, "y", **shared_text_args)


class FontSizePanelDemo(PanelBuilder):
    """1 by 1 panel demonstrating configured font sizes."""

    _n_cols = 1
    _n_rows = 1
    _panel_name = "font_size_panel"

    def build_panel(self) -> None:
        """Create custom content for the panel."""

        plot_sinusoid(self.axs[0][0])
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
        AxesSeparationPanelDemo,
        FontSizePanelDemo,
    ]

    for builder_class in builders:
        builder = builder_class(config)
        builder()
