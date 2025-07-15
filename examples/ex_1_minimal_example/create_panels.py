"""This example shows a minimal example of how to create a custom panel.

The script defines the following subclass of :class:`PanelBuilder`:
- MyPanel: 1 by 1 panel with a simple plot
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from mpl_panel_builder import PanelBuilder
from mpl_panel_builder.helpers import get_logger, setup_output_dir

# Simple setup
example_name = Path(__file__).parent.name
output_dir = setup_output_dir(example_name)
logger = get_logger(example_name)

# 1. Define the configuration
config: dict[str, Any] = {
    # Panel dimensions in centimeters
    "panel_dimensions": {
        "width_cm": 6.0,
        "height_cm": 5.0,
    },
    # Margins around the panel content (axes)
    "panel_margins": {
        "top_cm": 0.5,
        "bottom_cm": 1.5,
        "left_cm": 1.5,
        "right_cm": 0.5,
    },
    # Font sizes in points
    "font_sizes": {
        "axes_pt": 8,      # font size for axis labels and ticks
        "text_pt": 6,      # font size for other text elements
    },
    # Optional keys (with default values)
    "panel_output": {
        "directory": str(output_dir / "panels"),
        "format": "pdf",
    },
}

# Create output directory if it doesn't exist
(output_dir / "panels").mkdir(parents=True, exist_ok=True)

# 2. Create a panel subclass
class MyPanel(PanelBuilder):
    # Required class attributes
    _panel_name = "my_panel"  # Name of the panel
    _n_rows = 1               # Number of rows in the panel grid
    _n_cols = 1               # Number of columns in the panel grid

    def build_panel(self) -> None:
        """Populate the panel with your content.
        
        This method is called automatically when calling the panel class instance.
        Override this method to define your custom plotting logic.
        """
        # Access the single axis
        ax = self.axs[0][0]

        # Add your plotting code here
        ax.plot([1, 2, 3], [1, 2, 3])
        ax.set_xlabel("X axis")
        ax.set_ylabel("Y axis")


if __name__ == "__main__":
    logger.info("Creating panel with class: %s", MyPanel.__name__)
    builder = MyPanel(config)
    fig = builder()
    logger.info("Panel created and saved to %s", config["panel_output"]["directory"])
    
