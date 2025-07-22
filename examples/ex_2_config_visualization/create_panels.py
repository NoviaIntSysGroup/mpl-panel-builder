""" This example depicts config keys with three custom panels using the new
function-based API.

The script demonstrates:
- DimPanelDemo: 1 by 1 panel showing panel dimensions
- MarginPanelDemo: 1 by 1 panel illustrating panel margins
- FontSizePanelDemo: 1 by 1 panel demonstrating configured font sizes
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes

import mpl_panel_builder as mpb
from mpl_panel_builder.helpers import (
    cm_to_fig_rel,
    create_full_figure_axes,
)
from mpl_panel_builder.helpers.examples import get_logger, get_repo_root

# Simple setup
example_name = Path(__file__).parent.name
output_dir = get_repo_root() / "outputs" / example_name
output_dir.mkdir(parents=True, exist_ok=True)
(output_dir / "panels").mkdir(parents=True, exist_ok=True)
logger = get_logger(example_name)
plot_styles = {"config": "k:", "data": "b-"}

# Define panel configuration
margin = 1
config_color = (0.000, 0.000, 0.000)
data_color = (0.118, 0.565, 1.000)
mpb_config = {
    "panel": {
        "dimensions": {"width_cm": 6.0, "height_cm": 5.0},
        "margins": {
            "left_cm": margin,
            "right_cm": margin,
            "top_cm": margin,
            "bottom_cm": margin,
        },
        "axes_separation": {
            "x_cm": 0.5,
            "y_cm": 0.5,
        },
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
    "output": {
        "format": "pdf",
    },
}

# Example specific helper functions
def _plot_sinusoid(ax: Axes) -> None:
    """Plot a simple sinusoid.

    Args:
        ax: Axes to plot the sinusoid on.
    """
    x = np.linspace(0, 5 * np.pi, 100)
    y = np.sin(x)
    ax.plot(x, y, label="text", color=data_color)
    ax.set(xticks=[], yticks=[])
    for spine in ax.spines.values():
        spine.set_visible(True)


def create_dim_panel() -> None:
    """Create panel showing panel dimensions."""
    mpb.configure(mpb_config)
    mpb.set_rc_style()
    fig, axs = mpb.create_panel(rows=1, cols=1)
    ax = axs[0][0]

    _plot_sinusoid(ax)

    delta = 0.005  # Small delta to avoid overlap with panel border
    ax_panel = create_full_figure_axes(fig)
    ax_panel.plot([0, 1], [delta, delta], ":", color=config_color)
    ax_panel.plot([delta, delta], [0, 1], ":", color=config_color)

    padding_rel_x = cm_to_fig_rel(fig, margin / 2, "width")
    padding_rel_y = cm_to_fig_rel(fig, margin / 2, "height")

    fig.text(0.5, padding_rel_y, "width_cm", ha="center", va="center")
    fig.text(padding_rel_x, 0.5, "height_cm", rotation=90, ha="center", va="center")

    panel_path = output_dir / "panels" / "dim_panel"
    mpb.save_panel(fig, str(panel_path))
    logger.info(
        f"Dimension panel saved to: {panel_path.with_suffix('.pdf').resolve()}"
    )
    
    plt.close(fig)


def create_margin_panel() -> None:
    """Create panel illustrating panel margins."""

    mpb.configure(mpb_config)
    mpb.set_rc_style()
    fig, axs = mpb.create_panel(rows=1, cols=1)
    ax = axs[0][0]
    
    _plot_sinusoid(ax)

    margins_cm = mpb_config["panel"]["margins"]
    dims_cm = mpb_config["panel"]["dimensions"]
    left_margin_rel = margins_cm["left_cm"] / dims_cm["width_cm"]
    right_margin_rel = margins_cm["right_cm"] / dims_cm["width_cm"]
    top_margin_rel = margins_cm["top_cm"] / dims_cm["height_cm"]
    bottom_margin_rel = margins_cm["bottom_cm"] / dims_cm["height_cm"]

    ax_panel = create_full_figure_axes(fig)
    ax_panel.plot(
        [0, 1], [bottom_margin_rel, bottom_margin_rel], ":", color=config_color
    )
    ax_panel.plot(
        [left_margin_rel, left_margin_rel], [0, 1], ":", color=config_color
    )
    ax_panel.plot(
        [1 - right_margin_rel, 1 - right_margin_rel], [0, 1], ":", color=config_color
    )
    ax_panel.plot(
        [0, 1], [1 - top_margin_rel, 1 - top_margin_rel], ":", color=config_color
    )

    fig.text(0.5, bottom_margin_rel / 2, "bottom_cm", ha="center", va="center")
    fig.text(0.5, 1 - top_margin_rel / 2, "top_cm", ha="center", va="center")
    fig.text(left_margin_rel / 2, 0.5, "left_cm", rotation=90, ha="center", va="center")
    fig.text(
        1 - right_margin_rel / 2,
        0.5,
        "right_cm",
        rotation=90,
        ha="center",
        va="center",
    )
    
    panel_path = output_dir / "panels" / "margin_panel"
    mpb.save_panel(fig, str(panel_path))
    logger.info(
        f"Margin panel saved to: {panel_path.with_suffix('.pdf').resolve()}"
    )

def create_ax_separation_panel() -> None:
    """Create panel illustrating axes separation."""

    mpb.configure(mpb_config)
    mpb.set_rc_style()
    fig, axs = mpb.create_panel(rows=2, cols=2)
    ax = axs[0][0]
    
    for i in range(2):
        for j in range(2):
            ax = axs[i][j]
            _plot_sinusoid(ax)

    left_x = axs[0][0].get_position().x1
    right_x = axs[0][1].get_position().x0
    top_y = axs[0][0].get_position().y0
    bottom_y = axs[1][0].get_position().y1

    ax_panel = create_full_figure_axes(fig)
    ax_panel.plot([left_x, left_x], [0, 1], ":", color=config_color)
    ax_panel.plot([right_x, right_x], [0, 1], ":", color=config_color)
    ax_panel.plot([0, 1], [bottom_y, bottom_y], ":", color=config_color)
    ax_panel.plot([0, 1], [top_y, top_y], ":", color=config_color)

    mid_x = (left_x + right_x) / 2
    mid_y = (top_y + bottom_y) / 2
    padding_rel_x = cm_to_fig_rel(fig, margin / 2, "width")
    padding_rel_y = cm_to_fig_rel(fig, margin / 2, "height")

    fig.text(mid_x, padding_rel_y, "x_cm", rotation=90, ha="center", va="center")
    fig.text(1-padding_rel_x, mid_y, "y_cm", rotation=0, ha="center", va="center")

    panel_path = output_dir / "panels" / "axes_separation_panel"
    mpb.save_panel(fig, str(panel_path))
    logger.info(
        f"Axes separation panel saved to: {panel_path.with_suffix('.pdf').resolve()}"
    )


def create_font_size_panel() -> None:
    """Create panel demonstrating configured font sizes."""

    mpb.configure(mpb_config)
    mpb.set_rc_style()
    fig, axs = mpb.create_panel(rows=1, cols=1)
    ax = axs[0][0]
    
    _plot_sinusoid(ax)
    ax.set(
        xlabel="axes",
        ylabel="axes",
        title="axes",
    )
    ax.legend(loc="lower right")
    sample_text = "text\ntext\ntext\ntext"
    ax.text(0.1, -0.9, sample_text, va="bottom", ha="left")
    
    panel_path = output_dir / "panels" / "font_size_panel"
    mpb.save_panel(fig, str(panel_path))
    logger.info(
        f"Font size panel saved to: {panel_path.with_suffix('.pdf').resolve()}"
    )


if __name__ == "__main__":
    logger.info("Starting panel creation...")
    
    panels = [
        ("DimPanelDemo", create_dim_panel),
        ("MarginPanelDemo", create_margin_panel),
        ("AxesSeparationPanelDemo", create_ax_separation_panel),
        ("FontSizePanelDemo", create_font_size_panel),
    ]

    for panel_name, panel_func in panels:
        logger.info(f"Creating {panel_name}...")
        panel_func()
