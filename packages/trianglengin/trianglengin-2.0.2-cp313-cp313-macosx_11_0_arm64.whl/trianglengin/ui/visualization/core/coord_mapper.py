# Guard UI imports
try:
    import pygame
except ImportError as e:
    raise ImportError(
        "UI components require 'pygame'. Install with 'pip install trianglengin[ui]'."
    ) from e

# Use absolute imports for core components
from trianglengin.config import EnvConfig
from trianglengin.utils import geometry

# Correct the import path for the drawing utility (relative within UI)
from ..drawing.utils import get_triangle_points


def _calculate_render_params(
    width: int, height: int, config: EnvConfig
) -> tuple[float, float, float, float]:
    """Calculates scale (cw, ch) and offset (ox, oy) for rendering the grid."""
    rows, cols = config.ROWS, config.COLS
    cols_eff = cols * 0.75 + 0.25 if cols > 0 else 1
    scale_w = width / cols_eff if cols_eff > 0 else 1
    scale_h = height / rows if rows > 0 else 1
    scale = max(1.0, min(scale_w, scale_h))
    cell_size = scale
    grid_w_px = cols_eff * cell_size
    grid_h_px = rows * cell_size
    offset_x = (width - grid_w_px) / 2
    offset_y = (height - grid_h_px) / 2
    return cell_size, cell_size, offset_x, offset_y


def get_grid_coords_from_screen(
    screen_pos: tuple[int, int], grid_area_rect: pygame.Rect, config: EnvConfig
) -> tuple[int, int] | None:
    """Maps screen coordinates (relative to screen) to grid row/column."""
    if not grid_area_rect or not grid_area_rect.collidepoint(screen_pos):
        return None

    local_x = screen_pos[0] - grid_area_rect.left
    local_y = screen_pos[1] - grid_area_rect.top
    cw, ch, ox, oy = _calculate_render_params(
        grid_area_rect.width, grid_area_rect.height, config
    )
    if cw <= 0 or ch <= 0:
        return None

    # Estimate row/col based on overall position
    row = int((local_y - oy) / ch) if ch > 0 else -1
    # Approximate column based on horizontal position, accounting for 0.75 width factor
    approx_col_center_index = (local_x - ox - cw / 4) / (cw * 0.75) if cw > 0 else -1
    col = int(round(approx_col_center_index))

    # Check the estimated cell and its immediate neighbors using point-in-polygon
    # This is more accurate near triangle boundaries
    for r_check in [row, row - 1, row + 1]:
        if not (0 <= r_check < config.ROWS):
            continue
        # Check a slightly wider range of columns due to triangular nature
        for c_check in [col - 1, col, col + 1, col + 2]:
            if not (0 <= c_check < config.COLS):
                continue
            is_up = (r_check + c_check) % 2 != 0
            pts = get_triangle_points(r_check, c_check, is_up, ox, oy, cw, ch)
            # Use the geometry utility function
            if geometry.is_point_in_polygon((local_x, local_y), pts):
                return r_check, c_check

    # Fallback if point-in-polygon check fails (should be rare)
    if 0 <= row < config.ROWS and 0 <= col < config.COLS:
        return row, col
    return None


def get_preview_index_from_screen(
    screen_pos: tuple[int, int], preview_rects: dict[int, pygame.Rect]
) -> int | None:
    """Maps screen coordinates to a shape preview index."""
    if not preview_rects:
        return None
    for idx, rect in preview_rects.items():
        if rect and rect.collidepoint(screen_pos):
            return idx
    return None
