"""Tests to verify that all example scripts run without errors.

These tests are marked with @pytest.mark.example and are not part of the 
core test suite. They are used to ensure that all example scripts 
remain functional.
To run only these tests: pytest -m example
To exclude these tests: pytest -m "not example"
"""

import pathlib
import subprocess
import sys
from collections.abc import Generator

import pytest

from mpl_panel_builder.helpers.examples import get_repo_root


def find_create_panels_scripts() -> Generator[pathlib.Path, None, None]:
    """Find all create_panels.py scripts in the examples directory.
    
    Yields:
        Path objects pointing to create_panels.py files.
    """
    repo_root = get_repo_root()
    examples_dir = repo_root / "examples"
    yield from examples_dir.rglob("create_panels.py")


@pytest.mark.example
@pytest.mark.parametrize("script_path", find_create_panels_scripts())
def test_create_panels_script_runs(script_path: pathlib.Path) -> None:
    """Verify that each create_panels.py script runs without errors.
    
    This test runs the script as a subprocess to ensure the main execution
    block is actually tested, not just the module imports.
    
    Args:
        script_path: Path to the create_panels.py script to test.
        
    Raises:
        AssertionError: If the script fails to run or returns non-zero exit code.
    """
    
    # Get repo root for consistent working directory
    repo_root = get_repo_root()
    
    # Run the script as a subprocess to execute the main block
    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True,
        cwd=str(repo_root),
    )
    
    if result.returncode != 0:
        error_msg = f"Script {script_path} failed with return code {result.returncode}"
        if result.stderr:
            error_msg += f"\nSTDERR:\n{result.stderr}"
        if result.stdout:
            error_msg += f"\nSTDOUT:\n{result.stdout}"
        raise AssertionError(error_msg)
