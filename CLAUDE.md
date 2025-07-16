# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`mpl-panel-builder` is a Python library for creating publication-quality scientific figure panels with matplotlib. It provides a class-based architecture for building panels with precise dimensions (in centimeters), consistent styling, and repeatable layouts that can be assembled into complete figures.

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

- **`PanelBuilder`** (`src/mpl_panel_builder/panel_builder.py`): Abstract base class for creating panels. Subclasses must define `_panel_name`, `_n_rows`, `_n_cols` class attributes and implement `build_panel()` method.

- **`PanelConfig`** (`src/mpl_panel_builder/panel_config/config.py`): Immutable configuration system using frozen dataclasses with dot-access. Supports nested configurations and custom fields through `_extra` attribute.

- **Configuration System**: Uses frozen dataclasses for type-safe, immutable configuration with automatic validation. Supports relative updates (e.g., "+=0.5", "*1.2") via `override_config()` function.

### Panel Creation Pattern

1. Define configuration dictionary with required keys:
   - `panel_dimensions`: Panel size in centimeters
   - `panel_margins`: Margins around plot area  
   - `style`: Styling configuration with theme support and matplotlib rcParams

2. Subclass `PanelBuilder` with required class attributes:
   - `_panel_name`: Unique panel identifier
   - `_n_rows`, `_n_cols`: Grid dimensions

3. Implement `build_panel()` method with plotting logic

4. Instantiate and call panel class to generate figure

### Styling Architecture

The styling system is built around themes and rcParams:

- **`StyleConfig`** (`src/mpl_panel_builder/panel_config/types/styles.py`): Configuration dataclass containing `theme` (str) and `rc_params` (dict) fields.

- **`StyleManager`** (`src/mpl_panel_builder/panel_builder/styles.py`): Manages theme-based styling with:
  - Theme registry with `WhiteTheme` and `NoneTheme` 
  - Theme merging logic where user rcParams override theme defaults
  - `get_style_rc()` method returns final rcParams for matplotlib

- **Font Size Extraction**: Features module extracts font sizes dynamically from axes objects:
  - Scale bars use `ax.xaxis.label.get_fontsize()` / `ax.yaxis.label.get_fontsize()`
  - Text annotations use `plt.rcParams['font.size']`

### Key Features

- **Precise Layout**: All dimensions specified in centimeters for exact sizing
- **Theme-based Style Management**: Flexible styling system with predefined themes ('white', 'none') and full matplotlib rcParams support. User rcParams override theme defaults.
- **Scale Bars**: Built-in support for scale bars with `draw_scale_bar()` method
- **Debug Mode**: Grid overlay for layout debugging via `debug_panel.show` config
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
