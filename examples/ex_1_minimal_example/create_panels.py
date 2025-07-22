"""This example shows a minimal example of how to create a panel using the new
function-based API.

The script demonstrates:
- Simple panel creation with mpb.create_panel()
- Configuration using mpb.configure()
- Saving panels with mpb.save_panel()
"""

from pathlib import Path

import matplotlib.pyplot as plt

import mpl_panel_builder as mpb
from mpl_panel_builder.helpers.examples import get_logger, get_repo_root

# Simple setup
example_name = Path(__file__).parent.name
output_dir = get_repo_root() / "outputs" / example_name
output_dir.mkdir(parents=True, exist_ok=True)
logger = get_logger(example_name)

# Panel configuration
mpb_config = {
    "panel": {
        "dimensions": {
            "width_cm": 6.0,
            "height_cm": 5.0,
        },
        "margins": {
            "top_cm": 0.5,
            "bottom_cm": 1.5,
            "left_cm": 1.5,
            "right_cm": 0.5,
        },
    },
    "style": {
        "rc_params": { 
            "font.size": 8,
        }
    },
}

# Create and populate the panel
if __name__ == "__main__":
    logger.info("Starting panel creation...")
    
    # Set matplotlib styling and create the panel
    mpb.configure(mpb_config)
    mpb.set_rc_style()
    fig, axs = mpb.create_panel(rows=1, cols=1)
    
    # Access the single axis
    ax = axs[0][0]

    # Add your plotting code here
    ax.plot([1, 2, 3], [1, 2, 3])
    ax.set_xlabel("X axis")
    ax.set_ylabel("Y axis")
    
    # Save the panel
    panel_path = output_dir / "panels" / "my_panel"
    mpb.save_panel(fig, str(panel_path))
    logger.info(f"Panel saved to: {panel_path.with_suffix('.pdf').resolve()}")
    
    plt.close(fig)
