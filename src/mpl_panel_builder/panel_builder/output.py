"""Output management for panels."""

import warnings
from pathlib import Path

from matplotlib.figure import Figure as MatplotlibFigure

from ..panel_config import PanelConfig


class OutputManager:
    """Manages figure output and saving for panels."""

    def __init__(self, config: PanelConfig):
        """Initialize output manager.
        
        Args:
            config: Panel configuration object.
        """
        self.config = config

    def save_fig(
        self, fig: MatplotlibFigure, panel_name: str, filename_suffix: str | None = None
    ) -> None:
        """Saves the figure to the output directory.

        Args:
            fig: The matplotlib figure to save.
            panel_name: The base name for the panel file.
            filename_suffix: Optional string to append to panel_name when naming 
                the saved file.
                
        Note:
            If no output directory is configured, a warning will be issued and
            the figure will not be saved.
        """
        try:
            if not self.config.panel_output.directory:
                warnings.warn(
                    "No output directory configured. Figure will not be saved.",
                    UserWarning,
                    stacklevel=2,
                )
                return

            directory = Path(self.config.panel_output.directory)
            if not directory.exists():
                warnings.warn(
                    f"Output directory does not exist: {directory}. "
                    "Figure will not be saved.",
                    UserWarning,
                    stacklevel=2,
                )
                return

            # Save the figure
            file_format = self.config.panel_output.format
            dpi = self.config.panel_output.dpi
            if filename_suffix:
                panel_name = f"{panel_name}_{filename_suffix}"
            
            output_path = directory / f"{panel_name}.{file_format}"
            fig.savefig(output_path, dpi=dpi)

        except Exception as e:
            warnings.warn(
                f"Failed to save figure: {e!s}",
                UserWarning,
                stacklevel=2,
            )