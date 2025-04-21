import logging

import pygame

# Import DisplayConfig from trianglengin
from trianglengin.config import DisplayConfig

logger = logging.getLogger(__name__)


def calculate_interactive_layout(
    screen_width: int, screen_height: int, display_config: DisplayConfig
) -> dict[str, pygame.Rect]:
    """
    Calculates layout rectangles for interactive modes (play/debug).
    Places grid on the left and preview on the right.
    Uses DisplayConfig for padding and dimensions.
    """
    sw, sh = screen_width, screen_height
    pad = display_config.PADDING
    hud_h = display_config.HUD_HEIGHT
    preview_w = display_config.PREVIEW_AREA_WIDTH

    available_h = max(0, sh - hud_h - 2 * pad)
    available_w = max(0, sw - 3 * pad)

    grid_w = max(0, available_w - preview_w)
    grid_h = available_h

    grid_rect = pygame.Rect(pad, pad, grid_w, grid_h)
    preview_rect = pygame.Rect(grid_rect.right + pad, pad, preview_w, grid_h)

    screen_rect = pygame.Rect(0, 0, sw, sh)
    grid_rect = grid_rect.clip(screen_rect)
    preview_rect = preview_rect.clip(screen_rect)

    logger.debug(
        f"Interactive Layout calculated: Grid={grid_rect}, Preview={preview_rect}"
    )

    return {
        "grid": grid_rect,
        "preview": preview_rect,
    }


def calculate_training_layout(
    screen_width: int,
    screen_height: int,
    display_config: DisplayConfig,
    progress_bars_total_height: int,  # Height needed for progress bars
) -> dict[str, pygame.Rect]:
    """
    Calculates layout rectangles for a potential training visualization mode.
    MINIMAL SPACING. Worker grid top, progress bars bottom (above HUD), plots fill middle.
    Uses DisplayConfig for padding and dimensions.
    """
    sw, sh = screen_width, screen_height
    pad = 2  # Minimal padding
    hud_h = display_config.HUD_HEIGHT

    # --- Worker Grid Area (Top) ---
    total_available_h_for_grid_plots_bars = max(0, sh - hud_h - 2 * pad)
    top_area_h = min(
        int(total_available_h_for_grid_plots_bars * 0.10), 80
    )  # 10% or 80px max
    top_area_w = sw - 2 * pad
    worker_grid_rect = pygame.Rect(pad, pad, top_area_w, top_area_h)

    # --- Progress Bar Area (Bottom, above HUD) ---
    pb_area_y = sh - hud_h - pad - progress_bars_total_height
    pb_area_w = sw - 2 * pad
    progress_bar_area_rect = pygame.Rect(
        pad, pb_area_y, pb_area_w, progress_bars_total_height
    )

    # --- Plot Area (Middle) ---
    plot_area_y = worker_grid_rect.bottom + pad
    plot_area_w = sw - 2 * pad
    plot_area_h = max(0, progress_bar_area_rect.top - plot_area_y - pad)  # Fill space
    plot_rect = pygame.Rect(pad, plot_area_y, plot_area_w, plot_area_h)

    # Clip all rects to screen bounds
    screen_rect = pygame.Rect(0, 0, sw, sh)
    worker_grid_rect = worker_grid_rect.clip(screen_rect)
    plot_rect = plot_rect.clip(screen_rect)
    progress_bar_area_rect = progress_bar_area_rect.clip(screen_rect)

    logger.debug(
        f"Training Layout calculated: WorkerGrid={worker_grid_rect}, PlotRect={plot_rect}, ProgressBarArea={progress_bar_area_rect}"
    )

    return {
        "worker_grid": worker_grid_rect,
        "plots": plot_rect,
        "progress_bar_area": progress_bar_area_rect,
    }


# Default export can remain if desired, or be removed if only specific layouts are used.
calculate_layout = calculate_interactive_layout
