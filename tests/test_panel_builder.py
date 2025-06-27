import pathlib
from typing import Any, TypeAlias

import matplotlib
import pytest

matplotlib.use('Agg')
from matplotlib.figure import Figure as MatplotlibFigure

from mpl_panel_builder.panel_builder import PanelBuilder

ConfigDict: TypeAlias = dict[str, dict[str, Any]]


def make_dummy_panel_class(
    panel_name: str = "dummy_panel",
    n_rows: int = 1, 
    n_cols: int = 1,
    suffix: str | None = None
) -> type[PanelBuilder]:
    """Create a dummy PanelBuilder subclass for testing.
    
    Args:
        panel_name: Name of the panel to use for saving the figure.
        n_rows: Number of rows in the panel grid.
        n_cols: Number of columns in the panel grid.
        suffix: Optional suffix to append to the panel name.
        
    Returns:
        A PanelBuilder subclass with the specified dimensions.
    """
    # Use locals to assign class attributes via metaprogramming
    return type(
        "DummyPanel",
        (PanelBuilder,),
        {
            "_panel_name": panel_name,
            "_n_rows": n_rows,
            "_n_cols": n_cols,
            "build_panel": lambda self, suffix=suffix: (
                self.axs[0][0].plot([0, 1], [0, 1]), suffix
            )[1],
        }
    )

# Tests for PanelBuilder
@pytest.mark.parametrize("missing_attr", ["_panel_name", "_n_rows", "_n_cols"])
def test_subclass_validation_raises_without_required_attributes(
    missing_attr: str
) -> None:
    """Ensure PanelBuilder subclass requires all required attributes.
    
    Args:
        missing_attr: The attribute to omit from the test class.
        
    Raises:
        TypeError: When attempting to create a PanelBuilder subclass without 
            defining all required class attributes.
    """
    # Create a class dict with all required attributes
    class_dict = {
        "_panel_name": "test_panel",
        "_n_rows": 1,
        "_n_cols": 1
    }
    # Remove the attribute we're testing
    del class_dict[missing_attr]
    
    with pytest.raises(TypeError, match=missing_attr):
        type("InvalidPanel", (PanelBuilder,), class_dict)


def test_build_returns_matplotlib_figure(sample_config_dict: ConfigDict) -> None:
    """Test that calling the builder returns a matplotlib figure.
    
    Args:
        sample_config_dict: A configuration dictionary for panel building.
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


def test_axs_property_raises_before_build(sample_config_dict: ConfigDict) -> None:
    """Ensure axs raises if accessed before creation.
    
    Args:
        sample_config_dict: A configuration dictionary for panel building.
        
    Raises:
        RuntimeError: When accessing the axs property before building the figure.
    """

    dummy_builder = make_dummy_panel_class()
    builder = dummy_builder(sample_config_dict)
    with pytest.raises(RuntimeError):
        _ = builder.axs


@pytest.mark.parametrize("n_rows,n_cols", [
    (1, 1),
    (2, 2),
    (3, 1),
    (1, 3),
])
def test_axs_has_correct_dimensions(
    n_rows: int, 
    n_cols: int, 
    sample_config_dict: ConfigDict
) -> None:
    """Ensure axs has the correct dimensions after building.
    
    Args:
        n_rows: Number of rows in the panel grid.
        n_cols: Number of columns in the panel grid.
        sample_config_dict: A configuration dictionary for panel building.
        
    Returns:
        None
    """

    dummy_builder = make_dummy_panel_class(n_rows=n_rows, n_cols=n_cols)
    builder = dummy_builder(sample_config_dict)
    _ = builder()

    axs = builder.axs
    assert len(axs) == n_rows
    for row in axs:
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
    ax = builder.axs[0][0]

    # Expected positions in figure coordinates (normalized 0–1)
    total_width_cm = sample_config_dict["panel_dimensions"]["width_cm"]
    total_height_cm = sample_config_dict["panel_dimensions"]["height_cm"]
    margins = sample_config_dict["panel_margins"]

    expected_x = margins["left_cm"] / total_width_cm
    expected_y = margins["bottom_cm"] / total_height_cm
    expected_width = (total_width_cm 
                      - margins["left_cm"] 
                      - margins["right_cm"]) / total_width_cm
    expected_height = (total_height_cm 
                       - margins["top_cm"] 
                       - margins["bottom_cm"]) / total_height_cm

    assert pytest.approx(ax.get_position().x0) == expected_x
    assert pytest.approx(ax.get_position().y0) == expected_y
    assert pytest.approx(ax.get_position().width) == expected_width
    assert pytest.approx(ax.get_position().height) == expected_height


def test_filename_suffix(
    tmp_path: pathlib.Path, sample_config_dict: ConfigDict
) -> None:
    """Suffix returned from ``build_panel`` is appended to ``panel_name``."""

    config = dict(sample_config_dict)
    config["panel_output"] = {
        "directory": str(tmp_path),
        "format": "png",
        "dpi": 72,
    }

    # Without suffix → default filename
    dummy_builder = make_dummy_panel_class()
    builder = dummy_builder(config)
    builder()
    assert (tmp_path / "dummy_panel.png").exists()

    # With suffix → suffix appended
    dummy_builder = make_dummy_panel_class(suffix="alt")
    builder = dummy_builder(config)
    builder()
    assert (tmp_path / "dummy_panel_alt.png").exists()
