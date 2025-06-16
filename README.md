# mpl-panel-builder

[![Pre-commit](https://github.com/NoviaIntSysGroup/mpl-panel-builder/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/NoviaIntSysGroup/mpl-panel-builder/actions/workflows/pre-commit.yml)
[![tests](https://github.com/NoviaIntSysGroup/mpl-panel-builder/actions/workflows/tests.yml/badge.svg)](https://github.com/NoviaIntSysGroup/mpl-panel-builder/actions/workflows/tests.yml)
![Black](https://img.shields.io/badge/code%20style-black-000000.svg)
![Ruff](https://img.shields.io/badge/linter-ruff-0098db)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

`mpl-panel-builder` helps you compose publication-quality figure panels with precise and repeatable layouts.  Panels are created by subclassing `PanelBuilder` and defining their size, margins and axes grid in centimeters.  A dataclass based configuration system keeps layout parameters and custom options in one place.  Example scripts show how panels can be combined via TikZ to produce complete figures.

## Installation

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

## Example

Run one of the demo scripts to generate panels and assemble them into a figure:

```bash
python examples/config_visualization/create_figure.py
```

Generated files are stored under `outputs/`.

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

## License

This project is released under the [MIT License](LICENSE).
