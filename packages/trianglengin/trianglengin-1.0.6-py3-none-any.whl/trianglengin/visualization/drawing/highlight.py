# File: trianglengin/visualization/drawing/highlight.py
import pygame

# Use internal imports
from ...core.structs import Triangle
from ..core import colors


def draw_debug_highlight(
    surface: pygame.Surface,
    r: int,
    c: int,
    # config: EnvConfig, # Removed - use cw, ch, ox, oy
    cw: float,
    ch: float,
    ox: float,
    oy: float,
) -> None:
    """Highlights a specific triangle border for debugging using pre-calculated parameters."""
    if surface.get_width() <= 0 or surface.get_height() <= 0:
        return

    if cw <= 0 or ch <= 0:
        return

    is_up = (r + c) % 2 != 0
    temp_tri = Triangle(r, c, is_up)
    pts = temp_tri.get_points(ox, oy, cw, ch)

    pygame.draw.polygon(surface, colors.DEBUG_TOGGLE_COLOR, pts, 3)
