# File: trianglengin/visualization/drawing/previews.py
import logging

import pygame

# Use internal imports
from trianglengin.config import DisplayConfig, EnvConfig
from trianglengin.core.environment import GameState
from trianglengin.core.structs import Shape, Triangle
from trianglengin.visualization.core import colors

from .shapes import draw_shape

logger = logging.getLogger(__name__)


def render_previews(
    surface: pygame.Surface,
    game_state: GameState,
    area_topleft: tuple[int, int],
    _mode: str,
    env_config: EnvConfig,
    display_config: DisplayConfig,
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
        slot_rect_screen = slot_rect_local.move(area_topleft)
        preview_rects_screen[i] = slot_rect_screen

        shape: Shape | None = game_state.shapes[i]
        is_selected = selected_shape_idx == i

        border_width = selected_border if is_selected else border
        border_color = (
            colors.PREVIEW_SELECTED_BORDER if is_selected else colors.PREVIEW_BORDER
        )
        pygame.draw.rect(surface, border_color, slot_rect_local, border_width)

        if shape:
            draw_area_w = slot_w - 2 * (border_width + inner_pad)
            draw_area_h = slot_h - 2 * (border_width + inner_pad)

            if draw_area_w > 0 and draw_area_h > 0:
                min_r, min_c, max_r, max_c = shape.bbox()
                shape_rows = max_r - min_r + 1
                shape_cols_eff = (
                    (max_c - min_c + 1) * 0.75 + 0.25 if shape.triangles else 1
                )

                scale_w = (
                    draw_area_w / shape_cols_eff if shape_cols_eff > 0 else draw_area_w
                )
                scale_h = draw_area_h / shape_rows if shape_rows > 0 else draw_area_h
                cell_size = max(1.0, min(scale_w, scale_h))

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

                draw_shape(
                    surface,
                    shape,
                    (int(draw_topleft_x), int(draw_topleft_y)),
                    cell_size,
                    _is_selected=is_selected,
                    origin_offset=(-min_r, -min_c),
                )

        current_y += slot_h + pad

    return preview_rects_screen


def draw_placement_preview(
    surface: pygame.Surface,
    shape: Shape,
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

    temp_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    temp_surface.fill((0, 0, 0, 0))

    for dr, dc, is_up in shape.triangles:
        tri_r, tri_c = r + dr, c + dc
        temp_tri = Triangle(tri_r, tri_c, is_up)
        pts = temp_tri.get_points(ox, oy, cw, ch)
        pygame.draw.polygon(temp_surface, color, pts)

    surface.blit(temp_surface, (0, 0))


def draw_floating_preview(
    surface: pygame.Surface,
    shape: Shape,
    screen_pos: tuple[int, int],
    # _config: EnvConfig, # Removed - not needed with fixed cell_size
    # _mapper_module: "coord_mapper_module", # Removed
) -> None:
    """Draws a semi-transparent shape floating at the screen position."""
    if not shape or not shape.triangles:
        return

    cell_size = 20.0  # Fixed size for floating preview
    alpha = 100
    color: colors.ColorRGBA = (shape.color[0], shape.color[1], shape.color[2], alpha)

    temp_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    temp_surface.fill((0, 0, 0, 0))

    min_r, min_c, max_r, max_c = shape.bbox()
    center_r = (min_r + max_r) / 2.0
    center_c = (min_c + max_c) / 2.0

    for dr, dc, is_up in shape.triangles:
        pt_x = screen_pos[0] + (dc - center_c) * (cell_size * 0.75)
        pt_y = screen_pos[1] + (dr - center_r) * cell_size

        temp_tri = Triangle(0, 0, is_up)
        rel_pts = temp_tri.get_points(0, 0, cell_size, cell_size)
        pts = [(px + pt_x, py + pt_y) for px, py in rel_pts]
        pygame.draw.polygon(temp_surface, color, pts)

    surface.blit(temp_surface, (0, 0))
