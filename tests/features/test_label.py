"""Tests for label feature."""


import mpl_panel_builder as mpb
from mpl_panel_builder.features import add_label


def test_add_label_basic() -> None:
    """Test basic label functionality."""
    mpb.reset_config()
    
    mpb.set_rc_style()
    fig, axs = mpb.create_panel(rows=1, cols=1)
    ax = axs[0][0]
    
    # Should not raise an exception
    add_label(ax, "a")
    
    # Check that text was added
    texts = ax.texts + fig.texts
    assert len(texts) >= 1


def test_add_label_with_config() -> None:
    """Test label with custom configuration."""
    mpb.reset_config()
    
    mpb.configure({
        "features": {
            "label": {
                "x_cm": 1.0,
                "y_cm": 1.0,
                "bold": False,
                "caps": True,
                "prefix": "(",
                "suffix": ")",
                "fontsize_pt": 12
            }
        }
    })
    
    mpb.set_rc_style()
    fig, axs = mpb.create_panel(rows=1, cols=1)
    ax = axs[0][0]
    
    add_label(ax, "test")
    
    # Check that text was added
    texts = ax.texts + fig.texts
    assert len(texts) >= 1
    
    # Check that text formatting was applied
    label_text = None
    for text in texts:
        if text.get_text() == "(TEST)":  # caps=True, prefix/suffix applied
            label_text = text
            break
    
    assert label_text is not None
    assert label_text.get_fontsize() == 12
    assert label_text.get_weight() == "normal"  # bold=False