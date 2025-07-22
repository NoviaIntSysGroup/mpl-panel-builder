<p align="center">
    <img src="images/mpl-panel-builder-logo.png" alt="mpl-panel-builder logo" width="256px" >   
</p>

<h2 align="center"> Create publication-quality scientific figure panels with a consistent layout</h2>

<div align="center">

[![Ruff Lint](https://github.com/NoviaIntSysGroup/mpl-panel-builder/actions/workflows/lint.yml/badge.svg)](https://github.com/NoviaIntSysGroup/mpl-panel-builder/actions/workflows/lint.yml)
[![Pyright Type Check](https://github.com/NoviaIntSysGroup/mpl-panel-builder/actions/workflows/typecheck.yml/badge.svg)](https://github.com/NoviaIntSysGroup/mpl-panel-builder/actions/workflows/typecheck.yml)
[![Unit Tests](https://github.com/NoviaIntSysGroup/mpl-panel-builder/actions/workflows/tests.yml/badge.svg)](https://github.com/NoviaIntSysGroup/mpl-panel-builder/actions/workflows/tests.yml)

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
[![PyPI version](https://badge.fury.io/py/mpl-panel-builder.svg)](https://badge.fury.io/py/mpl-panel-builder)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

</div>

<div align="center">

`mpl-panel-builder` helps you compose matplotlib-based publication-quality scientific figure panels with precise and repeatable layouts. The shared precise layout lets you align panels perfectly into complete figures by simply stacking them vertically or horizontally. Included example scripts illustrate how to create panels and how these can be combined with TikZ to obtain a complete figure creation pipeline that is fully reproducible and under version control in Git. 

</div>

## Features

- 📏 **Precise Layout Control**: Define panel dimensions in centimeters for exact sizing
- 🎨 **Consistent Styling**: Maintain uniform fonts, margins, and aesthetics across panels
- 🔄 **Reproducible Workflow**: Version-controlled figure creation pipeline
- 📊 **Flexible Panel Composition**: Easy vertical and horizontal stacking of panels
- 🎯 **Publication-Ready**: Optimized for scientific publication requirements

## Requirements

- Python 3.11 or higher
- Matplotlib
- TikZ (optional, for complete figure assembly)
- Poppler (optional, for converting PDFs to png)

## Installation

### From PyPI (recommended)

To use `mpl-panel-builder` in your project, install it from PyPI:

```bash
pip install mpl-panel-builder
```

### From source (for examples and development)

If you want to explore the examples or contribute to the project, follow these steps to install from source:

```bash
# clone repository
$ git clone https://github.com/NoviaIntSysGroup/mpl-panel-builder.git
$ cd mpl-panel-builder

# install package and development dependencies
$ uv sync
```

## Basic usage

Panels are created using simple function calls. You first configure your panel with `mpb.configure(config_dict)` using a config dict specifying the panel's dimensions, margins, and styling (Matplotlib rcParams). Next, the styling is set via `mpb.set_style_rc()`, and the figure and axes are created via `mpb.create_panel()`. A minimal example is given below:

```python
import matplotlib.pyplot as plt
import mpl_panel_builder as mpb

# mpl_panel_builder configuration
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
    # Styling via rcParams
    "style": {
        "rc_params": {
            "font.size": 8,
        }
    }
}

# Apply the config and style, and create your figure and axes
mpb.configure(mpb_config)
mpb.set_rc_style()
fig, axs = mpb.create_panel(rows=1, cols=1)
ax = axs[0][0]

# Add your plotting code here
ax.plot([1, 2, 3], [1, 2, 3])
ax.set_xlabel("X axis")
ax.set_ylabel("Y axis")

# Save the panel
mpb.save_panel(fig, "my_panel")
```

### Configuration Options

The configuration dict supports four main sections:

- **`panel`**: Core settings for dimensions, margins, and axes separation.
- **`style`**: Styling via rcParams.
- **`features`**: Settings for additional features (e.g., scale bars and color bars).
- **`output`**: Settings for saving panels (format and DPI).

You can view all available configuration options by running:

```python
import mpl_panel_builder as mpb

# Print template configuration to see all available options
mpb.print_template_config()
```

### Configuration Override

For advanced configuration scenarios, the `configure()` function also supports special operators to modify the existing configuration:

```python
import mpl_panel_builder as mpb

base_config = {
    'panel': {
        'dimensions': {'width_cm': 10, 'height_cm': 8},
        'margins': {'left_cm': 1, 'right_cm': 1}
    }
}

# Use special operators for relative updates
updates = {
    'panel': {
        'dimensions': {'width_cm': '+=5'},     # Add 5 to current value
        'margins': {'left_cm': '*1.5'}        # Multiply by 1.5
    }
}

# First configure with base config
mpb.configure(base_config)

# Then apply updates using special operators
mpb.configure(updates)
# Result: width_cm becomes 15, left_cm becomes 1.5
```

Supported operators:
- `"+=X"`: Add X to current value
- `"-=X"`: Subtract X from current value  
- `"*X"`: Multiply current value by X
- `"=X"`: Set value to X

### Extra Features

Extra features include wrappers for systematically aligning scale bars, colorbars, and annotations. In addition, the package includes a feature for placing a grid over the whole panel to verify that all elements have their intended position.

```python
from mpl_panel_builder.features import (
    draw_x_scale_bar, draw_y_scale_bar, 
    add_colorbar, add_annotation, draw_gridlines
)

# Add scale bars
draw_x_scale_bar(ax, length=1.0, label="1 cm")
draw_y_scale_bar(ax, length=0.5, label="0.5 cm")

# Add colorbar, mappable could e.g. be
# mappable = ax.scatter()
# mappable = ax.imshow()
add_colorbar(ax, mappable, position="right")

# Add annotations
add_annotation(ax, "Text", loc="northwest")

# Add debug gridlines
draw_gridlines(fig)
```

## Examples

The repository includes example scripts that demonstrate both panel creation and how to programmatically assemble panels into complete figures using additional tools (TikZ and Poppler). All generated files are stored under `outputs/`.

### Example 1: Minimal example

```bash
# Create panels only
uv run python examples/ex_1_minimal_example/create_panels.py
```

### Example 2: Config key visualization

```bash
# Create panels only
uv run python examples/ex_2_config_visualization/create_panels.py
# Create complete figure, requires TikZ and Poppler
uv run python examples/ex_2_config_visualization/create_figure.py
```

<img src="outputs/ex_2_config_visualization/figure.png" style="max-width: 500px; width: 100%; height: auto;" />  

### Example 3: All features demonstration

```bash
# Create panels demonstrating all available features
uv run python examples/ex_3_debug_all_features/create_panels.py
```

## Repository layout

```
├── src/mpl_panel_builder/    # Library code
├── examples/                 # Demo scripts and LaTeX templates
├── outputs/                  # Generated content
├── tests/                    # Test suite
```

## Development

Install development requirements and set up the hooks:

```bash
uv sync
uv run pre-commit install --hook-type pre-commit --hook-type pre-push
```

Before committing or pushing run:

```bash
uv run ruff check .
uv run pyright
uv run pytest
```

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run the test suite (`uv run pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

Please ensure your code follows our style guidelines:
- Use Ruff for code formatting and linting
- Use Pyright for type checking
- Follow Google's Python style guide for docstrings
- Include type annotations for all functions
- Add tests for new functionality

## License

This project is released under the [MIT License](LICENSE).
