"""
Functions to calculate the layout of UI elements based on screen size and config.
"""

import logging

import pygame  # Required dependency

# Use absolute imports
from trianglengin.ui.config import DisplayConfig

logger = logging.getLogger(__name__)


def calculate_interactive_layout(
    screen_width: int, screen_height: int, config: DisplayConfig
) -> dict[str, pygame.Rect]:
    """
    Calculates layout rectangles for interactive modes (play/debug).

    Args:
        screen_width: Current width of the screen/window.
        screen_height: Current height of the screen/window.
        config: The DisplayConfig object.

    Returns:
        A dictionary mapping area names ('grid', 'preview') to pygame.Rect objects.
    """
    pad = config.PADDING
    hud_h = config.HUD_HEIGHT
    preview_w = config.PREVIEW_AREA_WIDTH

    # Available height after accounting for top/bottom padding and HUD
    available_h = screen_height - 2 * pad - hud_h
    # Available width after accounting for left/right padding and preview area
    available_w = screen_width - 3 * pad - preview_w

    if available_w <= 0 or available_h <= 0:
        logger.warning(
            f"Screen size ({screen_width}x{screen_height}) too small for layout."
        )
        # Return minimal valid rects to avoid errors downstream
        return {
            "grid": pygame.Rect(pad, pad, 1, 1),
            "preview": pygame.Rect(screen_width - pad - preview_w, pad, 1, 1),
        }

    # Grid area takes up the main left space
    grid_rect = pygame.Rect(pad, pad, available_w, available_h)

    # Preview area is on the right
    preview_rect = pygame.Rect(grid_rect.right + pad, pad, preview_w, available_h)

    # HUD area (optional, could be drawn directly without a rect)
    # hud_rect = pygame.Rect(pad, grid_rect.bottom + pad, screen_width - 2 * pad, hud_h)

    return {"grid": grid_rect, "preview": preview_rect}


def calculate_training_layout(
    screen_width: int, screen_height: int, config: DisplayConfig
) -> dict[str, pygame.Rect]:
    """
    Calculates layout rectangles for training/headless visualization (if needed).
    Currently simple, just uses the whole screen for the grid.

    Args:
        screen_width: Current width of the screen/window.
        screen_height: Current height of the screen/window.
        config: The DisplayConfig object.

    Returns:
        A dictionary mapping area names ('grid') to pygame.Rect objects.
    """
    pad = config.PADDING
    grid_rect = pygame.Rect(pad, pad, screen_width - 2 * pad, screen_height - 2 * pad)
    return {"grid": grid_rect}
