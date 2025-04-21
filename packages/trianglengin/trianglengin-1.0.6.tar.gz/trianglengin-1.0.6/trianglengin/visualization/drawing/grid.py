# File: trianglengin/visualization/drawing/grid.py
import logging
from typing import TYPE_CHECKING

import pygame

from trianglengin.core.structs.triangle import Triangle
from trianglengin.visualization.core import colors

if TYPE_CHECKING:
    from trianglengin.config import DisplayConfig, EnvConfig
    from trianglengin.core.environment.grid.grid_data import GridData


log = logging.getLogger(__name__)


def draw_grid_background(
    surface: pygame.Surface,
    env_config: "EnvConfig",
    display_config: "DisplayConfig",
    cw: float,
    ch: float,
    ox: float,
    oy: float,
    game_over: bool = False,
    debug_mode: bool = False,
) -> None:
    """Draws the background grid structure using pre-calculated render parameters."""
    bg_color = colors.GRID_BG_GAME_OVER if game_over else colors.GRID_BG_DEFAULT
    surface.fill(bg_color)

    if cw <= 0 or ch <= 0:
        log.warning("Cannot draw grid background with zero cell dimensions.")
        return

    for r in range(env_config.ROWS):
        # Use PLAYABLE_RANGE_PER_ROW to determine death zones
        start_col, end_col = env_config.PLAYABLE_RANGE_PER_ROW[r]
        for c in range(env_config.COLS):
            is_up = (r + c) % 2 != 0
            is_death = not (start_col <= c < end_col)  # Check if outside playable range
            tri = Triangle(r, c, is_up, is_death)

            if is_death:
                cell_color = colors.DEATH_ZONE_COLOR
            else:
                cell_color = (
                    colors.GRID_BG_LIGHT if (r % 2 == c % 2) else colors.GRID_BG_DARK
                )

            points = tri.get_points(ox, oy, cw, ch)
            pygame.draw.polygon(surface, cell_color, points)
            pygame.draw.polygon(surface, colors.GRID_LINE_COLOR, points, 1)

            if debug_mode:
                font = display_config.DEBUG_FONT
                text = f"{r},{c}"
                text_surf = font.render(text, True, colors.DEBUG_TOGGLE_COLOR)
                center_x = sum(p[0] for p in points) / 3
                center_y = sum(p[1] for p in points) / 3
                text_rect = text_surf.get_rect(center=(center_x, center_y))
                surface.blit(text_surf, text_rect)


def draw_grid_state(
    surface: pygame.Surface,
    grid_data: "GridData",
    cw: float,
    ch: float,
    ox: float,
    oy: float,
) -> None:
    """Draws the occupied triangles with their colors using pre-calculated parameters."""
    rows, cols = grid_data.rows, grid_data.cols
    occupied_np = grid_data._occupied_np
    color_id_np = grid_data._color_id_np
    death_np = grid_data._death_np

    if cw <= 0 or ch <= 0:
        log.warning("Cannot draw grid state with zero cell dimensions.")
        return

    for r in range(rows):
        for c in range(cols):
            if death_np[r, c]:
                continue

            if occupied_np[r, c]:
                color_id = int(color_id_np[r, c])
                color = colors.ID_TO_COLOR_MAP.get(color_id)

                is_up = (r + c) % 2 != 0
                tri = Triangle(r, c, is_up, False)
                points = tri.get_points(ox, oy, cw, ch)

                if color is not None:
                    pygame.draw.polygon(surface, color, points)
                elif color_id == colors.DEBUG_COLOR_ID:
                    pygame.draw.polygon(surface, colors.DEBUG_TOGGLE_COLOR, points)
                else:
                    log.warning(
                        f"Occupied cell ({r},{c}) has invalid color ID: {color_id}"
                    )
                    pygame.draw.polygon(surface, colors.TRIANGLE_EMPTY_COLOR, points)


def draw_debug_grid_overlay(
    surface: pygame.Surface,
    grid_data: "GridData",
    display_config: "DisplayConfig",
    cw: float,
    ch: float,
    ox: float,
    oy: float,
) -> None:
    """Draws debug information using pre-calculated render parameters."""
    font = display_config.DEBUG_FONT
    rows, cols = grid_data.rows, grid_data.cols

    if cw <= 0 or ch <= 0:
        log.warning("Cannot draw debug overlay with zero cell dimensions.")
        return

    for r in range(rows):
        for c in range(cols):
            is_up = (r + c) % 2 != 0
            is_death = grid_data.is_death(r, c)
            tri = Triangle(r, c, is_up, is_death)
            points = tri.get_points(ox, oy, cw, ch)

            text = f"{r},{c}"
            text_surf = font.render(text, True, colors.DEBUG_TOGGLE_COLOR)
            center_x = sum(p[0] for p in points) / 3
            center_y = sum(p[1] for p in points) / 3
            text_rect = text_surf.get_rect(center=(center_x, center_y))
            surface.blit(text_surf, text_rect)


def draw_grid(
    surface: pygame.Surface,
    grid_data: "GridData",
    env_config: "EnvConfig",
    display_config: "DisplayConfig",
    cw: float,
    ch: float,
    ox: float,
    oy: float,
    game_over: bool = False,
    debug_mode: bool = False,
) -> None:
    """Main function to draw the entire grid including background and state."""
    draw_grid_background(
        surface, env_config, display_config, cw, ch, ox, oy, game_over, debug_mode
    )
    draw_grid_state(surface, grid_data, cw, ch, ox, oy)
