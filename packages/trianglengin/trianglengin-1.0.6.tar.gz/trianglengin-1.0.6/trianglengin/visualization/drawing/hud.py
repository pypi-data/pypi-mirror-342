# File: trianglengin/trianglengin/visualization/drawing/hud.py
from typing import Any

import pygame

# Use internal imports
from ..core import colors


def render_hud(
    surface: pygame.Surface,
    mode: str,
    fonts: dict[str, pygame.font.Font | None],
    _display_stats: dict[str, Any] | None = None,  # Prefix with underscore
) -> None:
    """
    Renders HUD elements for interactive modes (play/debug).
    Displays only help text relevant to the mode.
    Ignores _display_stats.
    """
    screen_w, screen_h = surface.get_size()
    help_font = fonts.get("help")

    if not help_font:
        return

    bottom_y = screen_h - 10  # Position from bottom

    # --- Render Help Text Only ---
    help_text = "[ESC] Quit"
    if mode == "play":
        help_text += " | [Click] Select/Place Shape"
    elif mode == "debug":
        help_text += " | [Click] Toggle Cell"

    help_surf = help_font.render(help_text, True, colors.LIGHT_GRAY)
    # Position help text at the bottom right
    help_rect = help_surf.get_rect(bottomright=(screen_w - 15, bottom_y))
    surface.blit(help_surf, help_rect)
