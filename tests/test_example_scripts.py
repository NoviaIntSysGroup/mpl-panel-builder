"""Tests to verify that all example scripts run without errors.

These tests are marked with @pytest.mark.example and are not part of the 
core test suite. They are used to ensure that all example scripts 
remain functional.
To run only these tests: pytest -m example
To exclude these tests: pytest -m "not example"
"""

import importlib.util
import pathlib
from collections.abc import Generator

import pytest


def find_create_panels_scripts() -> Generator[pathlib.Path, None, None]:
    """Find all create_panels.py scripts in the examples directory.
    
    Yields:
        Path objects pointing to create_panels.py files.
    """
    examples_dir = pathlib.Path(__file__).parent.parent / "examples"
    yield from examples_dir.rglob("create_panels.py")


@pytest.mark.example
@pytest.mark.parametrize("script_path", find_create_panels_scripts())
def test_create_panels_script_runs(script_path: pathlib.Path) -> None:
    """Verify that each create_panels.py script runs without errors.
    
    Args:
        script_path: Path to the create_panels.py script to test.
        
    Raises:
        AssertionError: If the script fails to run or raises any exceptions.
    """
    # Load and execute the script
    spec = importlib.util.spec_from_file_location(
        script_path.stem, script_path
    )
    if spec is None or spec.loader is None:
        raise AssertionError(f"Could not load script: {script_path}")
    
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
