# MPL Panel Builder Refactoring Plan

## Target Structure

```
src/mpl_panel_builder/
├── __init__.py                    # Main API exports
├── panel_config/                  # Everything for PanelConfig
│   ├── __init__.py
│   ├── panel_config/             # Everything for PanelConfig            
│   ├── factory.py                # PanelConfigFactory
│   ├── utils.py                  # override_config
│   ├── base.py                   # FrozenConfigBase, DotDict
│   └── types/
│       ├── __init__.py           
│       ├── layout.py             # PanelDimensions, PanelMargins, AxesSpacing
│       ├── appearance.py         # FontSizes, LineStyle
│       ├── features.py           # ScaleBar, ColorBar, TextAnnotation, DebugPanel
│       └── output.py             # PanelOutput
├── panel_builder/                 # Everything for PanelBuilder
│   ├── __init__.py            
│   ├── panel_builder.py          # PanelBuilder class  
│   ├── figure.py                 # Figure creation
│   ├── axes.py                   # Axes layout  
│   ├── features.py               # Feature rendering
│   └── styles.py                 # Style management
└── mpl_helpers.py                # Matplotlib-specific utilities (unchanged)
```

## Key Name Changes

### Class Names
- `PanelBuilderConfig` → `PanelConfig`
- `Dimensions` → `PanelDimensions`
- `Margins` → `PanelMargins`
- `AxesSeparation` → `AxesSpacing`
- `ScaleBarConfig` → `ScaleBar`
- `ColorBarConfig` → `ColorBar`
- `DescriptionConfig` → `TextAnnotation`
- `CustomConfigDotDict` → `DotDict`
- `PanelConfigBuilder` → `PanelConfigFactory`

### File Organization
- Current `panel_builder_config.py` content split across `panel_config/` directory
- Current `panel_builder.py` main class stays, rendering logic moves to `panel_builder/`
- `mpl_helpers.py` remains unchanged

## Migration Steps

### Phase 1: Create Config Structure (Tests should pass)
1. Create `panel_config/` directory structure
2. Split `panel_builder_config.py` content:
   - Move base classes to `panel_config/base.py`
   - Move dataclasses to appropriate `panel_config/types/*.py` files
   - Create main `PanelConfig` class in `panel_config.py`
   - Add `panel_config/factory.py` with `PanelConfigFactory`
3. Update imports in `panel_config.py` to use new structure
4. Keep old `panel_builder_config.py` with re-exports and deprecation warnings
5. Update main `__init__.py` to export from new locations
6. **Test checkpoint**: All existing tests should pass

### Phase 2: Update PanelBuilder (Tests should pass)
1. Update `panel_builder.py` to import from new config structure
2. **Test checkpoint**: All existing tests should pass

### Phase 3: Create PanelBuilder Structure (Tests should pass)
1. Create `panel_builder/` directory structure
2. Extract rendering methods from `panel_builder.py`:
   - Figure creation → `panel_builder/figure.py`
   - Axes management → `panel_builder/axes.py`
   - Feature rendering → `panel_builder/features.py`
   - Style management → `panel_builder/styles.py`
3. Refactor main `PanelBuilder` class to use new managers
4. **Test checkpoint**: All existing tests should pass

### Phase 4: Cleanup (Tests should pass)
1. Remove old `panel_builder_config.py`
2. Remove deprecation warnings
3. **Test checkpoint**: All existing tests should pass

## Critical Migration Rules

### Maintain API Compatibility
- Keep all public method signatures identical
- Ensure `from mpl_panel_builder import PanelBuilder, PanelConfig` works
- All existing user code should work without changes

### Test Compatibility
- Tests should pass after each phase
- Only edit tests if imports break (change import paths only)
- Do not change test logic unless absolutely necessary
- Add new tests for new functionality (factory pattern) separately

### Import Strategy
```python
# Phase 1: panel_config.py should import from new structure
from .panel_config.base import FrozenConfigBase, DotDict
from .panel_config.types.layout import PanelDimensions, PanelMargins, AxesSpacing
from .panel_config.types.appearance import FontSizes, LineStyle
from .panel_config.types.features import ScaleBar, ColorBar, TextAnnotation, DebugPanel
from .panel_config.types.output import PanelOutput

# Phase 2: panel_builder.py should import from panel_config.py (not panel_builder_config.py)
from .panel_config import PanelConfig

# Phase 3: panel_builder.py should delegate to managers
from .panel_builder.figure import FigureManager
from .panel_builder.axes import AxesManager
# etc.
```

### Backward Compatibility During Migration
```python
# old panel_builder_config.py (Phase 1 only)
import warnings
from .panel_config import *

warnings.warn(
    "Importing from panel_builder_config is deprecated. Use 'from mpl_panel_builder import PanelConfig' instead.",
    DeprecationWarning,
    stacklevel=2
)
```

## New Features to Add (After Core Migration)

### PanelConfigFactory (Fluent Interface)
```python
# panel_config/factory.py
class PanelConfigFactory:
    def __init__(self):
        self._config = {}
    
    def dimensions(self, width_cm: float, height_cm: float) -> 'PanelConfigFactory':
        self._config['panel_dimensions'] = {'width_cm': width_cm, 'height_cm': height_cm}
        return self
    
    def margins(self, top_cm: float, bottom_cm: float, left_cm: float, right_cm: float) -> 'PanelConfigFactory':
        self._config['panel_margins'] = {
            'top_cm': top_cm, 'bottom_cm': bottom_cm,
            'left_cm': left_cm, 'right_cm': right_cm
        }
        return self
    
    def fonts(self, axes_pt: float, text_pt: float) -> 'PanelConfigFactory':
        self._config['font_sizes'] = {'axes_pt': axes_pt, 'text_pt': text_pt}
        return self
    
    def build(self) -> PanelConfig:
        return PanelConfig.from_dict(self._config)
```

## File Contents Preview

### panel_config/types/layout.py
```python
"""Layout and dimensional configuration types."""

from dataclasses import dataclass, field
from ..base import FrozenConfigBase

@dataclass(frozen=True)
class PanelDimensions(FrozenConfigBase):
    """Panel size specification in centimeters."""
    width_cm: float = field(metadata={"description": "Width dimension in centimeters"})
    height_cm: float = field(metadata={"description": "Height dimension in centimeters"})
    
    def __post_init__(self) -> None:
        if self.width_cm < 0 or self.height_cm < 0:
            raise ValueError("Dimensions must be positive.")

@dataclass(frozen=True)
class PanelMargins(FrozenConfigBase):
    """Panel margin specification in centimeters."""
    top_cm: float = field(metadata={"description": "Top margin in centimeters"})
    bottom_cm: float = field(metadata={"description": "Bottom margin in centimeters"})
    left_cm: float = field(metadata={"description": "Left margin in centimeters"})
    right_cm: float = field(metadata={"description": "Right margin in centimeters"})
    
    def __post_init__(self) -> None:
        if (self.top_cm < 0 or self.bottom_cm < 0 or self.left_cm < 0 or self.right_cm < 0):
            raise ValueError("Margins must be non-negative.")

@dataclass(frozen=True)
class AxesSpacing(FrozenConfigBase):
    """Spacing between subplot axes in centimeters."""
    x_cm: float = field(
        default=0.0,
        metadata={"description": "Horizontal spacing between adjacent axes in centimeters"}
    )
    y_cm: float = field(
        default=0.0,
        metadata={"description": "Vertical spacing between adjacent axes in centimeters"}
    )
    
    def __post_init__(self) -> None:
        if self.x_cm < 0 or self.y_cm < 0:
            raise ValueError("Axis spacing must be non-negative.")
```

### Main __init__.py Updates
```python
"""MPL Panel Builder - Publication-quality scientific figure panels.

Main Classes:
    PanelBuilder: Abstract base for creating figure panels
    PanelConfig: Configuration for panel layout and styling
"""

# ⭐ TWO MAIN CLASSES ⭐
from .panel_builder import PanelBuilder
from .panel_config import PanelConfig

# Convenience utilities  
from .panel_config import PanelConfigFactory, override_config

# Type definitions (for advanced users)
from .panel_config.types import *

__all__ = [
    # Main API
    "PanelBuilder",     # ⭐ Create panels
    "PanelConfig",      # ⭐ Configure panels
    
    # Utilities
    "PanelConfigFactory",
    "override_config",
    
    # Types
    *types.__all__
]
```

## Success Criteria

✅ All existing tests pass after each phase  
✅ All existing user code works without changes  
✅ New factory pattern available for users  
✅ Clear separation between config and rendering logic  
✅ Maintainable codebase with logical organization  
✅ No breaking changes to public API