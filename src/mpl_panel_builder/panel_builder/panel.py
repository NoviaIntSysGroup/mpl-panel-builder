"""Main PanelBuilder class using manager pattern."""

from typing import Any, Literal

import matplotlib.pyplot as plt
from matplotlib.axes import Axes as MatplotlibAxes
from matplotlib.cm import ScalarMappable
from matplotlib.colorbar import Colorbar
from matplotlib.figure import Figure as MatplotlibFigure

from ..panel_config import PanelConfig
from .axes import AxesManager
from .features import FeatureManager
from .figure import FigureManager
from .output import OutputManager
from .styles import StyleManager


class PanelBuilder:
    """Base class for constructing matplotlib panels with consistent layout.

    This class provides a framework for creating publication-quality figure panels
    with precise sizing in centimeters, consistent margins, and customizable styling.
    Subclasses must define n_rows and n_cols class attributes.

    Attributes:
        config (PanelConfig): Configuration object containing panel dimensions,
            margins, font sizes, and axis separation settings.
        panel_name (str): Name of the panel to use for saving the figure.
        n_rows (int): Number of subplot rows defined by the user.
        n_cols (int): Number of subplot columns defined by the user.
        fig (Optional[MatplotlibFigure]): Created matplotlib figure object.
        axs (Optional[List[List[MatplotlibAxes]]]): Grid of axes objects.
    """

    # Private class attributes that must be defined by subclasses
    _panel_name: str
    _n_rows: int
    _n_cols: int

    def __init__(self, config: dict[str, Any]):
        """Initializes the PanelBuilder with config and grid layout.

        Args:
            config (Dict[str, Any]): Layout and styling configuration.
        """
        self.config = PanelConfig.from_dict(config)

        # Initialize managers
        self._figure_manager = FigureManager(self.config)
        self._axes_manager = AxesManager(self.config)
        self._feature_manager = FeatureManager(self.config)
        self._style_manager = StyleManager(self.config)
        self._output_manager = OutputManager(self.config)

        self._fig: MatplotlibFigure | None = None
        self._axs: list[list[MatplotlibAxes]] | None = None

    def __init_subclass__(cls) -> None:
        """Validates that subclasses define required class attributes.
        
        This method ensures that any class inheriting from PanelBuilder properly
        defines the required panel_name, n_rows and n_cols class attributes that
        specify the panel grid dimensions.
        
        Args:
            cls: The class being defined that inherits from PanelBuilder.
            
        Raises:
            TypeError: If the subclass does not define panel_name, n_rows or
                n_cols.
        """
        super().__init_subclass__()
        required_attrs = ["_panel_name", "_n_rows", "_n_cols"]
        missing = [attr for attr in required_attrs if not hasattr(cls, attr)]
        if missing:
            raise TypeError(
                "Subclasses of PanelBuilder must define class attributes: "
                + ", ".join(missing)
            )

    def __call__(self, *args: Any, **kwargs: Any) -> MatplotlibFigure:
        """Initializes and builds the panel, returning the resulting figure.

        Any positional and keyword arguments are forwarded to
        :meth:`build_panel`. If :meth:`build_panel` returns a string, it is
        treated as a filename *suffix* appended to :pyattr:`panel_name` when the
        panel is saved. Returning ``None`` keeps the default filename.

        Returns:
            MatplotlibFigure: The constructed matplotlib figure.
        """
        style_context = self._style_manager.get_default_style_rc()
        with plt.rc_context(rc=style_context):
            self._fig = self._figure_manager.create_fig()
            self._figure_manager.draw_debug_lines(self._fig)
            self._axs = self._axes_manager.create_axes(
                self._fig, self.n_rows, self.n_cols
            )
            filename_suffix = self.build_panel(*args, **kwargs)
            self._output_manager.save_fig(self._fig, self.panel_name, filename_suffix)
        return self.fig

    def build_panel(self, *args: Any, **kwargs: Any) -> str | None:
        """Populates the panel with plot content.

        Subclasses should implement their plotting logic here.  The return value
        may optionally be a string which will be appended to
        :pyattr:`panel_name` when the panel is saved.  Any positional and
        keyword arguments passed to :py:meth:`__call__` are forwarded to this
        method.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement build_panel() method")

    # Delegate methods to managers
    def get_default_style_rc(self) -> dict[str, Any]:
        """Returns a style dictionary (rcParams) for use in rc_context."""
        return self._style_manager.get_default_style_rc()

    def create_fig(self) -> MatplotlibFigure:
        """Creates a matplotlib figure with the specified size."""
        return self._figure_manager.create_fig()

    def create_axes(self) -> list[list[MatplotlibAxes]]:
        """Creates the grid of axes based on layout configuration."""
        return self._axes_manager.create_axes(self.fig, self.n_rows, self.n_cols)
    
    def draw_x_scale_bar(
        self, 
        ax: MatplotlibAxes, 
        length: float, 
        label: str
    ) -> None:
        """Draws a horizontal scale bar for the given axes."""
        self._feature_manager.draw_x_scale_bar(self.fig, ax, length, label)
    
    def draw_y_scale_bar(
        self, 
        ax: MatplotlibAxes, 
        length: float, 
        label: str
    ) -> None:
        """Draws a vertical scale bar for the given axes."""
        self._feature_manager.draw_y_scale_bar(self.fig, ax, length, label)
    
    def add_colorbar(
        self, 
        mappable: ScalarMappable,
        ax: MatplotlibAxes, 
        position: Literal["left", "right", "bottom", "top"],
        shrink_axes: bool = True
    ) -> Colorbar:
        """Add a colorbar adjacent to the given axes."""
        return self._feature_manager.add_colorbar(
            self.fig, mappable, ax, position, shrink_axes
        )
    
    def add_annotation(
        self,
        ax: MatplotlibAxes,
        text: str,
        loc: str = "northwest",
        color: tuple[float, float, float] | str = (0, 0, 0),
        bg_color: tuple[float, float, float] | str = "none",
    ) -> None:
        """Add a annotation text inside the axes at a specified corner location."""
        self._feature_manager.add_annotation(ax, text, loc, color, bg_color)
    
    def draw_debug_lines(self) -> None:
        """Draw debug grid lines if enabled in the configuration."""
        self._feature_manager.draw_debug_lines(self.fig)

    def save_fig(self, filename_suffix: str | None = None) -> None:
        """Saves the figure to the output directory."""
        self._output_manager.save_fig(self.fig, self.panel_name, filename_suffix)

    # Properties
    @property
    def fig(self) -> MatplotlibFigure:
        """matplotlib.figure.Figure: The figure object, guaranteed to be initialized.

        Raises:
            RuntimeError: If the figure has not been created yet.
        """
        if self._fig is None:
            raise RuntimeError("Figure has not been created yet.")
        return self._fig

    @property
    def axs(self) -> list[list[MatplotlibAxes]]:
        """List[List[matplotlib.axes.Axes]]: The grid of axes, guaranteed to exist.

        Raises:
            RuntimeError: If the axes grid has not been created yet.
        """
        if self._axs is None:
            raise RuntimeError("Axes grid has not been created yet.")
        return self._axs
    
    @property
    def panel_name(self) -> str:
        """str: The name of the panel, read-only."""
        return type(self)._panel_name

    @property
    def n_rows(self) -> int:
        """int: The number of rows in the panel grid, read-only."""
        return type(self)._n_rows

    @property
    def n_cols(self) -> int:
        """int: The number of columns in the panel grid, read-only."""
        return type(self)._n_cols