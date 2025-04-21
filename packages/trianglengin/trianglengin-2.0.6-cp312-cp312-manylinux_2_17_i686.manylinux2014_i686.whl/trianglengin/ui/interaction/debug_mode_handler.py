# src/trianglengin/ui/interaction/debug_mode_handler.py
import logging
from typing import TYPE_CHECKING

# Imports are now direct
import pygame

# Use absolute imports for core components
from trianglengin.ui.visualization import core as vis_core

if TYPE_CHECKING:
    # Use absolute import for InputHandler as well
    from trianglengin.game_interface import GameState
    from trianglengin.ui.interaction.input_handler import InputHandler

logger = logging.getLogger(__name__)


def handle_debug_click(event: pygame.event.Event, handler: "InputHandler") -> None:
    """Handles mouse clicks in debug mode (toggle triangle state via C++)."""
    if not (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
        return

    game_state: GameState = handler.game_state  # Type hint uses wrapper
    visualizer = handler.visualizer
    mouse_pos = handler.mouse_pos

    layout_rects = visualizer.ensure_layout()
    grid_rect = layout_rects.get("grid")
    if not grid_rect:
        logger.error("Grid layout rectangle not available for debug click.")
        return

    grid_coords = vis_core.coord_mapper.get_grid_coords_from_screen(
        mouse_pos, grid_rect, game_state.env_config
    )
    if not grid_coords:
        return

    r, c = grid_coords
    try:
        # Call the debug toggle method on the wrapper, which calls C++
        game_state.debug_toggle_cell(r, c)
        logger.debug(f"Debug: Toggled cell ({r},{c}) via C++ backend.")
    except Exception as e:
        logger.error(f"Error calling debug_toggle_cell for ({r},{c}): {e}")


def update_debug_hover(handler: "InputHandler") -> None:
    """Updates the debug highlight position within the InputHandler."""
    handler.debug_highlight_coord = None

    game_state: GameState = handler.game_state  # Type hint uses wrapper
    visualizer = handler.visualizer
    mouse_pos = handler.mouse_pos

    layout_rects = visualizer.ensure_layout()
    grid_rect = layout_rects.get("grid")
    if not grid_rect or not grid_rect.collidepoint(mouse_pos):
        return

    grid_coords = vis_core.coord_mapper.get_grid_coords_from_screen(
        mouse_pos, grid_rect, game_state.env_config
    )

    if grid_coords:
        r, c = grid_coords
        # Get grid data to check validity and death zone status
        grid_data_np = game_state.get_grid_data_np()
        rows, cols = grid_data_np["death"].shape
        if 0 <= r < rows and 0 <= c < cols and not grid_data_np["death"][r, c]:
            handler.debug_highlight_coord = grid_coords
