import logging

# Guard UI imports
try:
    import pygame

    # Import DisplayConfig from the correct UI location
    from trianglengin.ui.config import DisplayConfig

    from ..core import colors  # Relative import
    from .shapes import draw_shape  # Relative import
    from .utils import get_triangle_points  # Relative import
except ImportError as e:
    raise ImportError(
        "UI components require 'pygame'. Install with 'pip install trianglengin[ui]'."
    ) from e

# Use absolute imports for core components
from trianglengin.config import EnvConfig
from trianglengin.game_interface import Shape

logger = logging.getLogger(__name__)


def render_previews(
    surface: pygame.Surface,
    shapes: list[Shape | None],  # Core Shape
    area_topleft: tuple[int, int],
    _mode: str,
    env_config: EnvConfig,  # Core EnvConfig
    display_config: DisplayConfig,  # UI DisplayConfig
    selected_shape_idx: int = -1,
) -> dict[int, pygame.Rect]:
    """Renders shape previews in their area. Returns dict {index: screen_rect}."""
    surface.fill(colors.PREVIEW_BG_COLOR)
    preview_rects_screen: dict[int, pygame.Rect] = {}
    num_slots = env_config.NUM_SHAPE_SLOTS
    pad = display_config.PREVIEW_PADDING
    inner_pad = display_config.PREVIEW_INNER_PADDING
    border = display_config.PREVIEW_BORDER_WIDTH
    selected_border = display_config.PREVIEW_SELECTED_BORDER_WIDTH

    if num_slots <= 0:
        return {}

    total_pad_h = (num_slots + 1) * pad
    available_h = surface.get_height() - total_pad_h
    slot_h = available_h / num_slots if num_slots > 0 else 0
    slot_w = surface.get_width() - 2 * pad
    current_y = float(pad)

    for i in range(num_slots):
        slot_rect_local = pygame.Rect(pad, int(current_y), int(slot_w), int(slot_h))
        # Calculate absolute screen rect for collision detection later
        slot_rect_screen = slot_rect_local.move(area_topleft)
        preview_rects_screen[i] = slot_rect_screen

        shape: Shape | None = shapes[i] if i < len(shapes) else None
        is_selected = selected_shape_idx == i
        border_width = selected_border if is_selected else border
        border_color = (
            colors.PREVIEW_SELECTED_BORDER if is_selected else colors.PREVIEW_BORDER
        )
        # Draw border onto the local surface
        pygame.draw.rect(surface, border_color, slot_rect_local, border_width)

        if shape:
            # Calculate drawing area inside the border and padding
            draw_area_w = slot_w - 2 * (border_width + inner_pad)
            draw_area_h = slot_h - 2 * (border_width + inner_pad)
            if draw_area_w > 0 and draw_area_h > 0:
                min_r, min_c, max_r, max_c = shape.bbox()
                shape_rows = max_r - min_r + 1
                # Effective columns considering 0.75 width factor for triangles
                shape_cols_eff = (
                    (max_c - min_c + 1) * 0.75 + 0.25 if shape.triangles else 1
                )
                # Calculate scale to fit shape within draw area
                scale_w = (
                    draw_area_w / shape_cols_eff if shape_cols_eff > 0 else draw_area_w
                )
                scale_h = draw_area_h / shape_rows if shape_rows > 0 else draw_area_h
                cell_size = max(1.0, min(scale_w, scale_h))  # Use smallest scale

                # Calculate centered top-left position for drawing the shape
                shape_render_w = shape_cols_eff * cell_size
                shape_render_h = shape_rows * cell_size
                draw_topleft_x = (
                    slot_rect_local.left
                    + border_width
                    + inner_pad
                    + (draw_area_w - shape_render_w) / 2
                )
                draw_topleft_y = (
                    slot_rect_local.top
                    + border_width
                    + inner_pad
                    + (draw_area_h - shape_render_h) / 2
                )
                # Draw the shape onto the local surface
                draw_shape(
                    surface,
                    shape,
                    (int(draw_topleft_x), int(draw_topleft_y)),
                    cell_size,
                    _is_selected=is_selected,
                    origin_offset=(-min_r, -min_c),  # Adjust drawing origin
                )
        current_y += slot_h + pad
    return preview_rects_screen


def draw_placement_preview(
    surface: pygame.Surface,
    shape: Shape,  # Core Shape
    r: int,
    c: int,
    is_valid: bool,
    cw: float,
    ch: float,
    ox: float,
    oy: float,
) -> None:
    """Draws a semi-transparent shape snapped to the grid using pre-calculated parameters."""
    if not shape or not shape.triangles:
        return
    if cw <= 0 or ch <= 0:
        return

    alpha = 100
    base_color = (
        colors.PLACEMENT_VALID_COLOR if is_valid else colors.PLACEMENT_INVALID_COLOR
    )
    color: colors.ColorRGBA = (base_color[0], base_color[1], base_color[2], alpha)
    # Create a temporary surface for alpha blending
    temp_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    temp_surface.fill((0, 0, 0, 0))  # Transparent background

    for dr, dc, is_up in shape.triangles:
        tri_r, tri_c = r + dr, c + dc
        # Use helper to get points relative to grid origin
        pts = get_triangle_points(tri_r, tri_c, is_up, ox, oy, cw, ch)
        pygame.draw.polygon(temp_surface, color, pts)

    # Blit the temporary surface onto the main surface
    surface.blit(temp_surface, (0, 0))


def draw_floating_preview(
    surface: pygame.Surface,
    shape: Shape,  # Core Shape
    screen_pos: tuple[int, int],
) -> None:
    """Draws a semi-transparent shape floating at the screen position."""
    if not shape or not shape.triangles:
        return

    cell_size = 20.0  # Fixed size for floating preview
    alpha = 100
    color: colors.ColorRGBA = (shape.color[0], shape.color[1], shape.color[2], alpha)
    # Create a temporary surface for alpha blending
    temp_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    temp_surface.fill((0, 0, 0, 0))  # Transparent background

    # Center the shape around the screen_pos
    min_r, min_c, max_r, max_c = shape.bbox()
    center_r = (min_r + max_r) / 2.0
    center_c = (min_c + max_c) / 2.0

    for dr, dc, is_up in shape.triangles:
        # Calculate position relative to the center of the shape bbox
        pt_x = screen_pos[0] + (dc - center_c) * (cell_size * 0.75)
        pt_y = screen_pos[1] + (dr - center_r) * cell_size
        # Use helper to get points relative to (0,0) for local drawing
        rel_pts = get_triangle_points(0, 0, is_up, 0, 0, cell_size, cell_size)
        # Translate points to the calculated screen position
        pts = [(px + pt_x, py + pt_y) for px, py in rel_pts]
        pygame.draw.polygon(temp_surface, color, pts)

    # Blit the temporary surface onto the main surface
    surface.blit(temp_surface, (0, 0))
