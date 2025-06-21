# mpl-panel-builder

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
[![Pre-commit](https://github.com/NoviaIntSysGroup/mpl-panel-builder/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/NoviaIntSysGroup/mpl-panel-builder/actions/workflows/pre-commit.yml)
[![tests](https://github.com/NoviaIntSysGroup/mpl-panel-builder/actions/workflows/tests.yml/badge.svg)](https://github.com/NoviaIntSysGroup/mpl-panel-builder/actions/workflows/tests.yml)
![Black](https://img.shields.io/badge/code%20style-black-000000.svg)
![Ruff](https://img.shields.io/badge/linter-ruff-0098db)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

`mpl-panel-builder` helps you compose matplotlib-based publication-quality scientific figure panels with precise and repeatable layouts. The shared precise layout lets you align panels perfectly into complete figures by simply stacking them vertically or horizontally. Included example scripts emphasize both how to create panels and how these can be combined with TikZ to obtain a complete figure creation pipeline that is fully reproducible and under version control in Git. 

## Features

- 📏 **Precise Layout Control**: Define panel dimensions in centimeters for exact sizing
- 🎨 **Consistent Styling**: Maintain uniform fonts, margins, and aesthetics across panels
- 🔄 **Reproducible Workflow**: Version-controlled figure creation pipeline
- 📊 **Flexible Panel Composition**: Easy vertical and horizontal stacking of panels
- 🎯 **Publication-Ready**: Optimized for scientific publication requirements
- 🔧 **Extensible**: Simple class-based architecture for custom panel types

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

# create the conda environment and use it with Poetry
$ conda env create -f environment.yml
$ conda activate mpl-panel-builder
$ poetry config virtualenvs.create false

# install package and notebook extras
$ poetry install --with notebook
```

## Usage

Panels are created by subclassing `PanelBuilder`, and by defining their size, margins and font sizes. A minimal example is given below:

```python
from mpl_panel_builder.panel_builder import PanelBuilder

# 1. Define the configuration
config = {
    # Panel dimensions in centimeters
    "panel_dimensions_cm": {
        "width": 6.0,   # 8 cm wide
        "height": 5.0,  # 6 cm tall
    },
    # Margins around the panel content (axes)
    "panel_margins_cm": {
        "top": 0.5,
        "bottom": 1.5,
        "left": 1.5,
        "right": 0.5,
    },
    # Font sizes in points
    "font_sizes_pt": {
        "axes": 8,      # font size for axis labels and ticks
        "text": 6,      # font size for other text elements
    }
}

# 2. Subclass PanelBuilder
class MyPanel(PanelBuilder):
    # Required class attributes
    _panel_name = "my_panel"  # Unique identifier for the panel
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

# 3. Create and build the panel
panel = MyPanel(config)
fig = panel()  # This creates and returns the figure panel
```

## Examples

The repository includes example scripts that demonstrate both panel creation and how to programmatically assemble panels into complete figures using additional tools (TikZ and Poppler). All generated files are stored under `outputs/`.

### Example 1: Config key visualization

```bash
# Create panels only
python examples/config_visualization/create_panels.py
# Create complete figure, requires TikZ and Poppler
python examples/config_visualization/create_figure.py
```

<img src="outputs/ex_2_config_visualization/figure.png" style="max-width: 500px; width: 100%; height: auto;" />  

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
poetry install --with dev,notebook
poetry run pre-commit install --hook-type pre-commit --hook-type pre-push
```

Before committing or pushing run:

```bash
poetry run ruff check .
poetry run mypy .
poetry run pytest
```

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run the test suite (`poetry run pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

Please ensure your code follows our style guidelines:
- Use Black for code formatting
- Follow Google's Python style guide for docstrings
- Include type annotations for all functions
- Add tests for new functionality

## License

This project is released under the [MIT License](LICENSE).
