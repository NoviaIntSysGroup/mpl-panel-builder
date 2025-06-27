#!/usr/bin/env python3
"""Script to generate and compile the configuration visualization panels.

This script runs the example script, compiles the LaTeX file, and converts the
resulting PDF to a high-resolution PNG for documentation purposes.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

# Add the project root to sys.path to allow importing helpers module
sys.path.append(str(Path(__file__).parent.parent.parent.absolute()))
from examples.helpers import get_logger, get_project_root

logger = get_logger(__name__)

def check_dependencies() -> None:
    """Check if required external dependencies are installed.

    Raises:
        RuntimeError: If any required dependency is not found.
    """
    dependencies = {
        "pdflatex": "LaTeX",
        "pdftoppm": "poppler-utils"
    }
    
    missing = []
    for cmd, package in dependencies.items():
        if shutil.which(cmd) is None:
            missing.append(f"{package} (provides {cmd})")
    
    if missing:
        raise RuntimeError(
            "Missing required dependencies:\n"
            + "\n".join(f"- {dep}" for dep in missing)
            + "\n\nPlease install them using your system's package manager."
        )


def run_command(cmd: list[str], cwd: Path | None = None) -> None:
    """Run a shell command and raise an exception if it fails.

    Args:
        cmd: List of command and arguments to run.
        cwd: Working directory to run the command in.
    """
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"Command failed: {' '.join(cmd)}\n"
            f"Error: {result.stderr}"
        )


def to_unix_path(path: Path) -> str:
    """Convert a Windows path to Unix-style path format.

    Args:
        path: Path to convert.

    Returns:
        Unix-style path string.
    """
    # Convert to absolute path and normalize
    abs_path = str(path.absolute())
    # Replace backslashes with forward slashes
    unix_path = abs_path.replace("\\", "/")
    # Convert drive letter format (e.g., C: to /c/)
    if unix_path[1] == ":":
        unix_path = f"/{unix_path[0].lower()}/{unix_path[3:]}"
    return unix_path


def main() -> None:
    """Main function to generate and compile the visualization."""
    # Check for required dependencies
    check_dependencies()
    
    # Get the project root directory and current example directory
    project_root = get_project_root()
    current_dir = Path(__file__).parent
    example_name = current_dir.name
    outputs_dir = project_root / "outputs" / example_name

    # Run the example script
    logger.info("Running example script...")
    run_command(
        ["python", str(current_dir / "create_panels.py")],
        cwd=current_dir
    )

    # Compile the LaTeX file
    logger.info("Compiling LaTeX file...")
    run_command(
        [
            "pdflatex",
            "-interaction=nonstopmode",
            "figure.tex"
        ],
        cwd=current_dir
    )

    # Move the PDF to outputs directory
    pdf_source = current_dir / "figure.pdf"
    pdf_dest = outputs_dir / "figure.pdf"
    pdf_dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(pdf_source, pdf_dest)

    # Clean up pdflatex auxiliary files
    aux_files = [".aux", ".log", ".out", ".synctex.gz"]
    for ext in aux_files:
        aux_file = current_dir / f"figure{ext}"
        if aux_file.exists():
            aux_file.unlink()

    # Convert PDF to PNG
    logger.info("Converting PDF to PNG...")
    png_output = outputs_dir / "figure.png"
    
    try:
        run_command(
            [
                "pdftoppm",
                "-png",
                "-r", "600",
                str(pdf_dest),
                str(png_output.with_suffix(""))
            ]
        )
        # Rename the file to remove the -1 suffix
        png_generated = Path(f"{png_output.with_suffix('')}-1.png")
        if png_output.exists():
            os.remove(png_output)
        os.rename(png_generated, png_output)
    except RuntimeError as e:
        logger.warning(f"Failed to convert PDF to PNG: {e}")

    logger.info("Done! Files generated:")
    logger.info(f"- PDF: {pdf_dest}")
    logger.info(f"- PNG: {png_output}")


if __name__ == "__main__":
    main() 
