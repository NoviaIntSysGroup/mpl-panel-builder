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