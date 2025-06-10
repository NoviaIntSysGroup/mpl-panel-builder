# mpl-panel-builder

![Black](https://img.shields.io/badge/code%20style-black-000000.svg)
![Ruff](https://img.shields.io/badge/linter-ruff-0098db)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

## Project structure
```text
project-root/
├── src/
│   ├── mpl_panel_builder/  # Installable shared package
│   │   ├── __init__.py
│   │   ├── panel_builder.py
│   │   ├── panel_config.py
├── notebooks/              # Jupyter notebooks for usage & examples
│   ├── demo.ipynb          # Example usage
├── config.yaml             # Panel configuration file for example usage

├── environment.yml         # Conda environment file
├── poetry.lock             # Locked dependencies  
├── pyproject.toml          # Project definition

├── README.md               # README
└── LICENSE                 # License file
```

## Installation
The project uses Conda to create a Python 3.12 virtual environment, and Poetry to manage dependencies and packaging.

```bash
# Clone the repository (e.g using SSH or by downloading it as a zip file)
$ git clone ADD LINK
$ cd mpl-panel-builder
# Set up the Conda environment
$ conda env create -f environment.yml
$ conda activate mpl-panel-builder
# Tell Poetry to use the current Conda environment
$ poetry config virtualenvs.create false
# Install runtime dependencies
$ poetry install --with notebook
```

## Usage
See the example notebooks for how to create custom figure panels.

## Contribution
Install the development dependencies:
```bash
poetry install --with notebook --with dev
```
and follow the guidelines below to maintain code quality and consistency across the project.

### Code Style
Use [Google-style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) for all public modules, functions, classes, and methods.

### Linting & Type Checking
The project uses the following tools to enforce code quality:

- [`ruff`](https://docs.astral.sh/ruff/) – A fast Python linter to ensure consistent code style and catch common issues.
- [`mypy`](https://mypy-lang.org/) – A static type checker for Python.

To run these checks locally:

```bash
# Lint with ruff
poetry run ruff check .

# Type-check with mypy
poetry run mypy .
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
