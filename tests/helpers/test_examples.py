"""Tests for examples helper module."""

import logging
import tempfile
from pathlib import Path

from mpl_panel_builder.helpers.examples import get_logger, setup_output_dir


def test_setup_output_dir_with_default_base() -> None:
    """Test setup_output_dir with default base directory."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        old_cwd = Path.cwd()
        try:
            # Change to temp directory
            Path(tmp_dir).cwd()
            
            output_dir = setup_output_dir("test_example")
            
            # Should create outputs/test_example
            assert output_dir.exists()
            assert output_dir.is_dir()
            
        finally:
            # Restore original working directory
            old_cwd.cwd() if old_cwd.exists() else None


def test_setup_output_dir_with_custom_base() -> None:
    """Test setup_output_dir with custom base directory."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        base_dir = Path(tmp_dir) / "custom_base"
        output_dir = setup_output_dir("test_example", base_dir)
        
        expected_path = base_dir / "test_example"
        assert output_dir == expected_path
        assert output_dir.exists()
        assert output_dir.is_dir()


def test_setup_output_dir_with_string_base() -> None:
    """Test setup_output_dir with string base directory."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        output_dir = setup_output_dir("test_example", tmp_dir)
        
        expected_path = Path(tmp_dir) / "test_example"
        assert output_dir == expected_path
        assert output_dir.exists()
        assert output_dir.is_dir()


def test_get_logger() -> None:
    """Test get_logger creates properly configured logger."""
    logger = get_logger("test_example")
    
    # Check logger properties
    assert isinstance(logger, logging.Logger)
    assert logger.name == "mpl_panel_builder.examples.test_example"
    assert logger.level == logging.INFO
    assert len(logger.handlers) == 1
    
    # Check handler configuration
    handler = logger.handlers[0]
    assert isinstance(handler, logging.StreamHandler)
    assert handler.formatter is not None


def test_get_logger_reuse() -> None:
    """Test that get_logger reuses existing logger instances."""
    logger1 = get_logger("test_example")
    logger2 = get_logger("test_example")
    
    # Should return the same logger instance
    assert logger1 is logger2
    # Should not duplicate handlers
    assert len(logger1.handlers) == 1