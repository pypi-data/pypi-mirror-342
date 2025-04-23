"""
Visualization module for rendering the game state using Pygame.
Provides components for interactive play/debug modes.
"""

# Imports are now direct. If pygame is missing, errors will occur upon use.

# Import core components needed externally
# Import core EnvConfig for type hinting if needed
# from trianglengin.config import EnvConfig # REMOVED Re-export
# from ..config import DisplayConfig  # REMOVED Re-export

from .core import colors  # Import the colors module
from .core.coord_mapper import (  # Import specific functions
    get_grid_coords_from_screen,
    get_preview_index_from_screen,
)
from .core.fonts import load_fonts  # Import specific function
from .core.visualizer import Visualizer  # Import the class

# Import drawing functions directly
from .drawing.grid import (
    draw_debug_grid_overlay,
    draw_grid_background,
    draw_grid_state,
)
from .drawing.highlight import draw_debug_highlight
from .drawing.hud import render_hud
from .drawing.previews import (
    draw_floating_preview,
    draw_placement_preview,
    render_previews,
)
from .drawing.shapes import draw_shape
from .drawing.utils import get_triangle_points

__all__ = [
    # Core Renderer & Layout related
    "Visualizer",
    "load_fonts",
    "colors",  # Export the colors module
    "get_grid_coords_from_screen",
    "get_preview_index_from_screen",
    # Drawing Functions
    "draw_grid_background",
    "draw_grid_state",
    "draw_debug_grid_overlay",
    "draw_shape",
    "render_previews",
    "draw_placement_preview",
    "draw_floating_preview",
    "render_hud",
    "draw_debug_highlight",
    "get_triangle_points",
    # Configs are NOT re-exported here
    # "DisplayConfig",
    # "EnvConfig",
]
