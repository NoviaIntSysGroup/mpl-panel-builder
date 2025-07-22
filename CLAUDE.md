# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`mpl-panel-builder` is a Python library for creating publication-quality scientific figure panels with matplotlib. It provides a simple function-based API for building panels with precise dimensions (in centimeters), consistent styling, and repeatable layouts that can be assembled into complete figures.

## Development Commands

### Environment Setup
```bash
# Install from source (required for development and examples)
uv sync
```

### Testing
```bash
# Run all tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=mpl_panel_builder

# Run tests excluding examples (faster)
uv run pytest -m "not example"
```

### Code Quality
```bash
# Run linter
uv run ruff check .

# Run type checker
uv run pyright

# Run all quality checks before committing
uv run ruff check . && uv run pyright && uv run pytest
```

### Pre-commit Hooks
```bash
# Install hooks
uv run pre-commit install --hook-type pre-commit --hook-type pre-push
```

## Architecture

### Core Components

- **`configure()`** (`src/mpl_panel_builder/config.py`): Global configuration system using dictionaries. Supports deep merging and special override strings like "+=2", "*1.5".

- **`create_panel()`** (`src/mpl_panel_builder/panel.py`): Creates matplotlib figure and axes grid with precise dimensions from global config.

- **`save_panel()`** (`src/mpl_panel_builder/panel.py`): Saves panels using output configuration settings.

- **Features Module** (`src/mpl_panel_builder/features/`): Individual functions for scale bars, colorbars, annotations, and debug gridlines.

### Panel Creation Pattern

1. Configure the package with `configure(config_dict)`:
   - `panel`: Dimensions, margins, and axes separation
   - `style`: Theme and matplotlib rcParams
   - `features`: Settings for individual features
   - `output`: Directory, format, and DPI

2. Set rcParams with `set_rc_style()` and create panels with `create_panel(rows, cols)`

3. Add plotting code and features as needed

4. Save with `save_panel(fig, name)`

### Styling Architecture

The styling system uses global configuration:

- **Theme Support**: Built-in 'article' and 'none' themes
- **rcParams Override**: User rcParams merge with theme defaults
- **Global Style Setting**: Use `set_rc_style()` to apply rcParams globally

### Complete API Reference

**Configuration Functions:**
- **`configure(config_dict)`**: Apply configuration dictionary with deep merging and special operators
- **`get_config()`**: Retrieve current configuration dictionary
- **`reset_config()`**: Reset to default configuration
- **`print_template_config()`**: Print default config template to stdout (safer than file operations)

**Panel Functions:**
- **`create_panel(rows=1, cols=1)`**: Create figure and axes grid using global config
- **`save_panel(fig, filepath)`**: Save panel using output configuration
- **`set_rc_style()`**: Apply rcParams globally from style configuration

**Features Module:**
- Import individual functions as needed: `from mpl_panel_builder.features import draw_x_scale_bar, add_colorbar, add_annotation, draw_gridlines`

### Key Features

- **Precise Layout**: All dimensions specified in centimeters for exact sizing
- **Simple API**: No subclassing - just function calls
- **Modular Features**: Import only what you need from `features` module
- **Global Configuration**: Easy to configure once and reuse
- **Template Output**: View configuration options with `print_template_config()`
- **Flexible Output**: Configurable output directory, format, and DPI

## Testing

- Tests are in `tests/` directory using pytest
- Example scripts are tested with `@pytest.mark.example` marker
- Use `pytest -m "not example"` to skip slower example tests during development
- Coverage configuration includes source path mapping via `pythonpath = ["src"]`

## Example Structure

Examples in `examples/` directory demonstrate both panel creation and figure assembly:
- Each example has its own subdirectory with clear naming
- Examples include helper scripts for TikZ-based figure assembly
- Generated outputs are stored in `outputs/` directory
