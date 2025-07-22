#!/usr/bin/env python3
"""Script to generate and compile the configuration visualization panels.

This script runs the example script, compiles the LaTeX file, and converts the
resulting PDF to a high-resolution PNG for documentation purposes.
"""

import os
import shutil
import subprocess
from pathlib import Path

from mpl_panel_builder.helpers.examples import get_logger, setup_output_dir

# Simple setup
example_name = Path(__file__).parent.name
output_dir = setup_output_dir(example_name)
logger = get_logger(example_name)

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


def run_command(
    cmd: list[str], cwd: Path | None = None, capture_output: bool = False
) -> None:
    """Run a shell command and raise an exception if it fails.

    Args:
        cmd: List of command and arguments to run.
        cwd: Working directory to run the command in.
        capture_output: Whether to capture output (hide it) or let it stream to console.
    """
    # Ensure we inherit the system PATH so external tools are accessible
    env = os.environ.copy()
    
    if capture_output:
        result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=env)
        if result.returncode != 0:
            raise RuntimeError(
                f"Command failed: {' '.join(cmd)}\n"
                f"Error: {result.stderr}"
            )
    else:
        result = subprocess.run(cmd, cwd=cwd, env=env)
        if result.returncode != 0:
            raise RuntimeError(f"Command failed: {' '.join(cmd)}")


def main() -> None:
    """Main function to generate and compile the visualization."""
    # Check for required dependencies
    check_dependencies()
    
    # Get the current example directory and outputs
    current_dir = Path(__file__).parent
    outputs_dir = output_dir

    # Run the example script
    logger.info("Running example script...")
    panels_script = current_dir / "create_panels.py"
    run_command(
        ["uv", "run", "python", str(panels_script)],
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
        cwd=current_dir,
        capture_output=True
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
                "-r", "300",
                str(pdf_dest),
                str(png_output.with_suffix(""))
            ],
            capture_output=True
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