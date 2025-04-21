# Guard UI imports
try:
    import pygame

    from ..core import colors  # Relative import
    from .utils import get_triangle_points  # Relative import
except ImportError as e:
    raise ImportError(
        "UI components require 'pygame'. Install with 'pip install trianglengin[ui]'."
    ) from e

# Use absolute imports for core components
from trianglengin.game_interface import Shape


def draw_shape(
    surface: pygame.Surface,
    shape: Shape,  # Core Shape
    topleft: tuple[int, int],
    cell_size: float,
    _is_selected: bool = False,  # Keep underscore if not used visually
    origin_offset: tuple[int, int] = (0, 0),
) -> None:
    """Draws a single shape onto a surface."""
    if not shape or not shape.triangles or cell_size <= 0:
        return

    shape_color = shape.color
    border_color = colors.GRAY  # Use a defined border color
    cw = cell_size
    ch = cell_size  # Assuming square aspect ratio for cells in preview

    for dr, dc, is_up in shape.triangles:
        # Adjust relative coords by origin offset (used for centering in previews)
        adj_r, adj_c = dr + origin_offset[0], dc + origin_offset[1]
        # Calculate top-left corner of the bounding box for this triangle
        tri_x = topleft[0] + adj_c * (cw * 0.75)
        tri_y = topleft[1] + adj_r * ch
        # Use helper to get points relative to (0,0) for local drawing
        # then translate them to the calculated tri_x, tri_y
        pts = [
            (px + tri_x, py + tri_y)
            for px, py in get_triangle_points(0, 0, is_up, 0, 0, cw, ch)
        ]
        pygame.draw.polygon(surface, shape_color, pts)
        pygame.draw.polygon(surface, border_color, pts, 1)  # Draw border
