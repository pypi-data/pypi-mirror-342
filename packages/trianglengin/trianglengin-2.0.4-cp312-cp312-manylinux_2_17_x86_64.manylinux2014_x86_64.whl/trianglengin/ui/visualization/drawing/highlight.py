# Guard UI imports
try:
    import pygame

    from ..core import colors  # Relative import
    from .utils import get_triangle_points  # Relative import
except ImportError as e:
    raise ImportError(
        "UI components require 'pygame'. Install with 'pip install trianglengin[ui]'."
    ) from e


def draw_debug_highlight(
    surface: pygame.Surface,
    r: int,
    c: int,
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
    # Use helper
    pts = get_triangle_points(r, c, is_up, ox, oy, cw, ch)
    pygame.draw.polygon(surface, colors.DEBUG_TOGGLE_COLOR, pts, 3)  # Draw border
