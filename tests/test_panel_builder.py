from typing import TypeAlias

import matplotlib
import pytest

matplotlib.use('Agg')
from matplotlib.figure import Figure as MatplotlibFigure

from mpl_panel_builder.panel_builder import PanelBuilder

ConfigDict: TypeAlias = dict[str, dict[str, float]]


def make_dummy_panel_class(n_rows: int = 1, n_cols: int = 1) -> type[PanelBuilder]:
    """Create a dummy PanelBuilder subclass for testing.
    
    Args:
        n_rows: Number of rows in the panel grid.
        n_cols: Number of columns in the panel grid.
        
    Returns:
        A PanelBuilder subclass with the specified dimensions.
    """
    # Use locals to assign class attributes via metaprogramming
    return type(
        "DummyPanel",
        (PanelBuilder,),
        {
            "n_rows": n_rows,
            "n_cols": n_cols,
            "build_panel": lambda self: self.axs_grid[0][0].plot([0, 1], [0, 1]),
        }
    )


def test_subclass_validation_raises_without_n_rows_n_cols() -> None:
    """Ensure PanelBuilder subclass requires n_rows and n_cols.
    
    Raises:
        TypeError: When attempting to create a PanelBuilder subclass without 
            defining n_rows and n_cols class attributes.
    """

    with pytest.raises(TypeError):

        class InvalidPanel(PanelBuilder):
            pass


def test_build_returns_matplotlib_figure(sample_config_dict: ConfigDict) -> None:
    """Test that calling the builder returns a matplotlib figure.
    
    Args:
        sample_config_dict: A configuration dictionary for panel building.
        
    Returns:
        None
    """

    dummy_builder = make_dummy_panel_class()
    builder = dummy_builder(sample_config_dict)
    fig = builder()
    assert isinstance(fig, MatplotlibFigure)


def test_fig_property_raises_before_build(sample_config_dict: ConfigDict) -> None:
    """Ensure fig property raises if accessed before creation.
    
    Args:
        sample_config_dict: A configuration dictionary for panel building.
        
    Raises:
        RuntimeError: When accessing the fig property before building the figure.
    """

    dummy_builder = make_dummy_panel_class()
    builder = dummy_builder(sample_config_dict)
    with pytest.raises(RuntimeError):
        _ = builder.fig


def test_axs_grid_property_raises_before_build(sample_config_dict: ConfigDict) -> None:
    """Ensure axs_grid raises if accessed before creation.
    
    Args:
        sample_config_dict: A configuration dictionary for panel building.
        
    Raises:
        RuntimeError: When accessing the axs_grid property before building the figure.
    """

    dummy_builder = make_dummy_panel_class()
    builder = dummy_builder(sample_config_dict)
    with pytest.raises(RuntimeError):
        _ = builder.axs_grid


@pytest.mark.parametrize("n_rows,n_cols", [
    (1, 1),
    (2, 2),
    (3, 1),
    (1, 3),
])
def test_axs_grid_has_correct_dimensions(
    n_rows: int, 
    n_cols: int, 
    sample_config_dict: ConfigDict
) -> None:
    """Ensure axs_grid has the correct dimensions after building.
    
    Args:
        n_rows: Number of rows in the panel grid.
        n_cols: Number of columns in the panel grid.
        sample_config_dict: A configuration dictionary for panel building.
        
    Returns:
        None
    """

    dummy_builder = make_dummy_panel_class(n_rows, n_cols)
    builder = dummy_builder(sample_config_dict)
    _ = builder()

    axs_grid = builder.axs_grid
    assert len(axs_grid) == n_rows
    for row in axs_grid:
        assert len(row) == n_cols


def test_fig_has_correct_margins(sample_config_dict: ConfigDict) -> None:
    """Ensure fig has the correct margins after building.
    
    Args:
        sample_config_dict: A configuration dictionary for panel building.
        
    Returns:
        None
    """
    
    dummy_builder = make_dummy_panel_class()
    builder = dummy_builder(sample_config_dict)
    _ = builder()
    ax = builder.axs_grid[0][0]

    # Expected positions in figure coordinates (normalized 0–1)
    total_width_cm = sample_config_dict["panel_dimensions_cm"]["width"]
    total_height_cm = sample_config_dict["panel_dimensions_cm"]["height"]
    margins = sample_config_dict["panel_margins_cm"]

    expected_x = margins["left"] / total_width_cm
    expected_y = margins["bottom"] / total_height_cm
    expected_width = (total_width_cm 
                      - margins["left"] 
                      - margins["right"]) / total_width_cm
    expected_height = (total_height_cm 
                       - margins["top"] 
                       - margins["bottom"]) / total_height_cm

    assert pytest.approx(ax.get_position().x0) == expected_x
    assert pytest.approx(ax.get_position().y0) == expected_y
    assert pytest.approx(ax.get_position().width) == expected_width
    assert pytest.approx(ax.get_position().height) == expected_height
