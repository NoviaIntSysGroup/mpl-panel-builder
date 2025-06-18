# Guidelines for AI contributions

This repository uses a `src` layout with the installable package located in
`src/mpl_panel_builder` and tests in `tests/`. Development dependencies and
pre-commit hooks are managed with Poetry. The version is derived from git tags
via `poetry-dynamic-versioning` and should not be edited manually.

## Development workflow

1. Install dependencies:
   ```bash
   poetry install --with dev,notebook
   poetry run pre-commit install --hook-type pre-commit --hook-type pre-push
   ```
2. Run linters and type checkers before committing:
   ```bash
   poetry run ruff check .
   poetry run mypy .
   ```
   Alternatively run `poetry run pre-commit run --files <changed files>`.
   Ruff is configured to automatically apply fixes.
3. Execute the test suite before pushing:
   ```bash
   poetry run pytest --cov=mpl_panel_builder
   ```

## Style

- The project targets Python 3.11+ and uses `ruff` (line length 88) for
  formatting and linting (target version 3.11, auto-fix enabled).
- Mypy runs in strict mode, so type hints must be complete.
- **All docstrings must follow [Google's style guide](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).**

Follow these rules for all files in this repository.
