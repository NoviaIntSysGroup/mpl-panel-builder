"""Utilities for example scripts and tutorials.

This module provides simple helper functions to reduce boilerplate
in example scripts without including the examples themselves.
"""

import logging
from pathlib import Path


def get_repo_root(start_path: Path | str | None = None) -> Path:
    """Find the root directory of the repository.
    
    Searches upward from the start_path for common repository markers
    like pyproject.toml, setup.py, .git, etc.
    
    Args:
        start_path: Starting path to search from (defaults to current directory)
        
    Returns:
        Path to the repository root directory
        
    Raises:
        RuntimeError: If no repository root is found
    """
    if start_path is None:
        start_path = Path.cwd()
    else:
        start_path = Path(start_path)
    
    # Repository markers to look for (in order of preference)
    markers = [
        "pyproject.toml",
        "setup.py", 
        ".git",
        "setup.cfg",
        "requirements.txt",
        "Pipfile",
        "poetry.lock",
        "uv.lock"
    ]
    
    current_path = start_path.resolve()
    
    while current_path != current_path.parent:  # Stop at filesystem root
        for marker in markers:
            if (current_path / marker).exists():
                return current_path
        current_path = current_path.parent
    
    # If no markers found, raise an error
    raise RuntimeError(
        f"Could not find repository root from {start_path}. "
        f"Looked for markers: {', '.join(markers)}"
    )


def setup_output_dir(example_name: str, base_dir: Path | str | None = None) -> Path:
    """Set up output directory for an example.
    
    Args:
        example_name: Name of the example (used for output folder)
        base_dir: Base directory for outputs (defaults to repository_root/outputs)
        
    Returns:
        Path to the example's output directory
    """
    if base_dir is None:
        repo_root = get_repo_root()
        base_dir = repo_root / "outputs"
    else:
        base_dir = Path(base_dir)
    
    output_dir = base_dir / example_name
    output_dir.mkdir(parents=True, exist_ok=True)
    
    return output_dir


def get_logger(example_name: str) -> logging.Logger:
    """Get a configured logger for an example.
    
    Args:
        example_name: Name of the example
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(f"mpl_panel_builder.examples.{example_name}")

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt='[%(asctime)s] %(levelname)s: %(message)s',
            datefmt='%H:%M:%S'
        )
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.propagate = False

    return logger