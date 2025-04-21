import logging

import numpy as np

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
from trianglengin.config import EnvConfig

# Import DisplayConfig from the correct UI location
from trianglengin.ui.config import DisplayConfig

log = logging.getLogger(__name__)


def draw_grid_background(
    surface: pygame.Surface,
    env_config: EnvConfig,  # Core config
    display_config: DisplayConfig,  # UI config
    cw: float,
    ch: float,
    ox: float,
    oy: float,
    game_over: bool = False,
    debug_mode: bool = False,
    death_mask_np: np.ndarray | None = None,
) -> None:
    """Draws the background grid structure using pre-calculated render parameters."""
    bg_color = colors.GRID_BG_GAME_OVER if game_over else colors.GRID_BG_DEFAULT
    surface.fill(bg_color)

    if cw <= 0 or ch <= 0:
        log.warning("Cannot draw grid background with zero cell dimensions.")
        return

    rows, cols = env_config.ROWS, env_config.COLS
    if death_mask_np is None or death_mask_np.shape != (rows, cols):
        log.warning(
            "Death mask not provided or shape mismatch, cannot draw death zones accurately."
        )
        # Attempt to reconstruct death mask from config if not provided
        death_mask_np = np.full((rows, cols), True, dtype=bool)
        for r_idx in range(rows):
            if r_idx < len(env_config.PLAYABLE_RANGE_PER_ROW):
                start_c, end_c = env_config.PLAYABLE_RANGE_PER_ROW[r_idx]
                if start_c < end_c:
                    death_mask_np[r_idx, start_c:end_c] = False
            else:
                log.warning(f"Missing playable range definition for row {r_idx}")

    for r in range(rows):
        for c in range(cols):
            is_up = (r + c) % 2 != 0
            is_death = death_mask_np[r, c]

            if is_death:
                cell_color = colors.DEATH_ZONE_COLOR
            else:
                # Alternate background color based on checkerboard pattern
                cell_color = (
                    colors.GRID_BG_LIGHT if (r % 2 == c % 2) else colors.GRID_BG_DARK
                )

            points = get_triangle_points(r, c, is_up, ox, oy, cw, ch)
            pygame.draw.polygon(surface, cell_color, points)
            pygame.draw.polygon(surface, colors.GRID_LINE_COLOR, points, 1)

            # Draw debug coordinates if in debug mode and font is available
            if debug_mode:
                debug_font = display_config.DEBUG_FONT
                if debug_font:
                    text = f"{r},{c}"
                    text_surf = debug_font.render(text, True, colors.DEBUG_TOGGLE_COLOR)
                    center_x = sum(p[0] for p in points) / 3
                    center_y = sum(p[1] for p in points) / 3
                    text_rect = text_surf.get_rect(center=(center_x, center_y))
                    surface.blit(text_surf, text_rect)


def draw_grid_state(
    surface: pygame.Surface,
    occupied_np: np.ndarray,
    color_id_np: np.ndarray,
    death_np: np.ndarray,
    rows: int,
    cols: int,
    cw: float,
    ch: float,
    ox: float,
    oy: float,
) -> None:
    """Draws the occupied triangles with their colors using pre-calculated parameters."""
    if cw <= 0 or ch <= 0:
        log.warning("Cannot draw grid state with zero cell dimensions.")
        return

    if (
        occupied_np.shape != (rows, cols)
        or color_id_np.shape != (rows, cols)
        or death_np.shape != (rows, cols)
    ):
        log.error("Grid state array shape mismatch.")
        return

    for r in range(rows):
        for c in range(cols):
            if death_np[r, c]:
                continue  # Skip death zones

            if occupied_np[r, c]:
                color_id = int(color_id_np[r, c])
                color = colors.ID_TO_COLOR_MAP.get(color_id)
                is_up = (r + c) % 2 != 0
                points = get_triangle_points(r, c, is_up, ox, oy, cw, ch)

                if color is not None:
                    pygame.draw.polygon(surface, color, points)
                elif color_id == colors.DEBUG_COLOR_ID:
                    # Draw debug-toggled cells with a specific color
                    pygame.draw.polygon(surface, colors.DEBUG_TOGGLE_COLOR, points)
                else:
                    # Fallback for unexpected color IDs
                    log.warning(
                        f"Occupied cell ({r},{c}) has invalid color ID: {color_id}"
                    )
                    pygame.draw.polygon(surface, colors.TRIANGLE_EMPTY_COLOR, points)


def draw_debug_grid_overlay(
    surface: pygame.Surface,
    display_config: DisplayConfig,  # UI config
    rows: int,
    cols: int,
    cw: float,
    ch: float,
    ox: float,
    oy: float,
) -> None:
    """Draws debug information (coordinates) using pre-calculated render parameters."""
    font = display_config.DEBUG_FONT
    if not font:
        log.warning("Debug font not available for overlay.")
        return
    if cw <= 0 or ch <= 0:
        log.warning("Cannot draw debug overlay with zero cell dimensions.")
        return

    for r in range(rows):
        for c in range(cols):
            is_up = (r + c) % 2 != 0
            points = get_triangle_points(r, c, is_up, ox, oy, cw, ch)
            text = f"{r},{c}"
            text_surf = font.render(text, True, colors.DEBUG_TOGGLE_COLOR)
            center_x = sum(p[0] for p in points) / 3
            center_y = sum(p[1] for p in points) / 3
            text_rect = text_surf.get_rect(center=(center_x, center_y))
            surface.blit(text_surf, text_rect)


def draw_grid(
    surface: pygame.Surface,
    grid_data_np: dict[str, np.ndarray],
    env_config: EnvConfig,  # Core config
    display_config: DisplayConfig,  # UI config
    cw: float,
    ch: float,
    ox: float,
    oy: float,
    game_over: bool = False,
    debug_mode: bool = False,
) -> None:
    """Main function to draw the entire grid including background and state."""
    draw_grid_background(
        surface,
        env_config,
        display_config,
        cw,
        ch,
        ox,
        oy,
        game_over,
        debug_mode,
        grid_data_np["death"],
    )
    draw_grid_state(
        surface,
        grid_data_np["occupied"],
        grid_data_np["color_id"],
        grid_data_np["death"],
        env_config.ROWS,
        env_config.COLS,
        cw,
        ch,
        ox,
        oy,
    )
    # Overlay debug coordinates only if in debug mode
    # Note: draw_grid_background already handles drawing coords if debug_mode=True
    # This function might be redundant if the background function does it.
    # Keeping it separate allows potentially different debug info later.
    # if debug_mode:
    #     draw_debug_grid_overlay(
    #         surface, display_config, env_config.ROWS, env_config.COLS, cw, ch, ox, oy
    #     )
