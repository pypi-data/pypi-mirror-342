# trianglengin/visualization/__init__.py
"""
Visualization module for rendering the game state using Pygame.
Provides components for interactive play/debug modes.
"""

# Import core components needed externally
# Import DisplayConfig from the new location
from ..config import DisplayConfig, EnvConfig
from .core import colors
from .core.coord_mapper import (
    get_grid_coords_from_screen,
    get_preview_index_from_screen,
)
from .core.fonts import load_fonts
from .core.layout import (
    calculate_interactive_layout,
    calculate_training_layout,
)
from .core.visualizer import Visualizer

# Import drawing functions that might be useful externally (optional)
from .drawing.grid import (
    draw_debug_grid_overlay,
    draw_grid_background,
    # draw_grid_indices, # Removed
    draw_grid_state,  # Renamed
)
from .drawing.highlight import draw_debug_highlight
from .drawing.hud import render_hud
from .drawing.previews import (
    draw_floating_preview,
    draw_placement_preview,
    render_previews,
)
from .drawing.shapes import draw_shape

__all__ = [
    # Core Renderer & Layout
    "Visualizer",
    "calculate_interactive_layout",
    "calculate_training_layout",
    "load_fonts",
    "colors",
    "get_grid_coords_from_screen",
    "get_preview_index_from_screen",
    # Drawing Functions
    "draw_grid_background",
    "draw_grid_state",  # Export renamed
    "draw_debug_grid_overlay",
    # "draw_grid_indices", # Removed
    "draw_shape",
    "render_previews",
    "draw_placement_preview",
    "draw_floating_preview",
    "render_hud",
    "draw_debug_highlight",
    # Config
    "DisplayConfig",  # Export DisplayConfig
    "EnvConfig",
]
