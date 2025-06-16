import logging
from pathlib import Path


def get_project_root() -> Path:
    """
    Return the absolute path to the project root directory.

    Searches for pyproject.toml by walking up the directory tree and returns the
    directory containing it. If not found, raises a ValueError.

    Returns:
        Path: Absolute path to the project root.
    """
    start_path = Path(__file__).resolve().parent
    
    for parent in [start_path, *start_path.parents]:
        pyproject = parent / "pyproject.toml"
        if pyproject.is_file():
            return parent
        
    raise ValueError("Could not locate 'pyproject.toml' in parent directories.")


def get_logger(name: str | None = None) -> logging.Logger:
    """
    Return a configured logger instance.

    Args:
        name (str | None): Name of the logger. If None, returns the root logger.

    Returns:
        logging.Logger: A logger with stream output and a standard formatter.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt='[%(asctime)s] %(levelname)s in %(name)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.propagate = False

    return logger