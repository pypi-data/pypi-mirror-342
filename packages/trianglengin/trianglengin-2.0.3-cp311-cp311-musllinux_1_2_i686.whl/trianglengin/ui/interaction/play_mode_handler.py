# src/trianglengin/ui/interaction/play_mode_handler.py
import logging
from typing import TYPE_CHECKING, cast

# Guard UI imports
try:
    import pygame

    # Use absolute import
    from trianglengin.ui.visualization import core as vis_core
except ImportError as e:
    raise ImportError(
        "UI components require 'pygame'. Install with 'pip install trianglengin[ui]'."
    ) from e

# Use absolute imports for core components
from trianglengin.config import EnvConfig

if TYPE_CHECKING:
    # Use absolute import for InputHandler as well
    from trianglengin.game_interface import GameState, Shape
    from trianglengin.ui.interaction.input_handler import InputHandler

logger = logging.getLogger(__name__)


# Add EnvConfig type hint for config
def _encode_action(shape_idx: int, r: int, c: int, config: EnvConfig) -> int:
    """Helper to encode action based on config. Matches C++ internal logic."""
    grid_size = config.ROWS * config.COLS
    if not (
        0 <= shape_idx < config.NUM_SHAPE_SLOTS
        and 0 <= r < config.ROWS
        and 0 <= c < config.COLS
    ):
        return -1
    # Cast the result to int for mypy
    return cast("int", shape_idx * grid_size + r * config.COLS + c)


def handle_play_click(event: pygame.event.Event, handler: "InputHandler") -> None:
    """Handles mouse clicks in play mode (select preview, place shape). Modifies handler state."""
    if not (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
        return

    game_state: GameState = handler.game_state
    visualizer = handler.visualizer
    mouse_pos = handler.mouse_pos

    if game_state.is_over():
        logger.info("Game is over, ignoring click.")
        return

    layout_rects = visualizer.ensure_layout()
    grid_rect = layout_rects.get("grid")
    preview_rects = visualizer.preview_rects
    current_shapes = game_state.get_shapes()

    preview_idx = vis_core.coord_mapper.get_preview_index_from_screen(
        mouse_pos, preview_rects
    )
    if preview_idx is not None:
        if handler.selected_shape_idx == preview_idx:
            handler.selected_shape_idx = -1
            handler.hover_grid_coord = None
            handler.hover_shape = None
            logger.info("Deselected shape.")
        elif (
            0 <= preview_idx < len(current_shapes)
            and current_shapes[preview_idx] is not None
        ):
            handler.selected_shape_idx = preview_idx
            logger.info(f"Selected shape index: {preview_idx}")
            update_play_hover(handler)
        else:
            logger.info(f"Clicked empty/invalid preview slot: {preview_idx}")
            if handler.selected_shape_idx != -1:
                handler.selected_shape_idx = -1
                handler.hover_grid_coord = None
                handler.hover_shape = None
        return

    selected_idx = handler.selected_shape_idx
    if selected_idx != -1 and grid_rect and grid_rect.collidepoint(mouse_pos):
        grid_coords = vis_core.coord_mapper.get_grid_coords_from_screen(
            mouse_pos, grid_rect, game_state.env_config
        )
        shape_to_place: Shape | None = (
            current_shapes[selected_idx]
            if 0 <= selected_idx < len(current_shapes)
            else None
        )

        if grid_coords and shape_to_place:
            r, c = grid_coords
            potential_action = _encode_action(selected_idx, r, c, game_state.env_config)

            if (
                potential_action != -1
                and potential_action in game_state.valid_actions()
            ):
                reward, done = game_state.step(potential_action)
                logger.info(
                    f"Placed shape {selected_idx} at {grid_coords}. R={reward:.1f}, Done={done}"
                )
                handler.selected_shape_idx = -1
                handler.hover_grid_coord = None
                handler.hover_shape = None
            else:
                logger.info(
                    f"Clicked grid at {grid_coords}, but placement invalid (action {potential_action} not found in valid set)."
                )
        else:
            logger.info(f"Clicked grid at {grid_coords}, but shape or coords invalid.")


def update_play_hover(handler: "InputHandler") -> None:
    """Updates the hover state within the InputHandler."""
    handler.hover_grid_coord = None
    handler.hover_is_valid = False
    handler.hover_shape = None

    game_state: GameState = handler.game_state
    visualizer = handler.visualizer
    mouse_pos = handler.mouse_pos

    if game_state.is_over() or handler.selected_shape_idx == -1:
        return

    layout_rects = visualizer.ensure_layout()
    grid_rect = layout_rects.get("grid")
    selected_idx = handler.selected_shape_idx
    current_shapes = game_state.get_shapes()
    if not (0 <= selected_idx < len(current_shapes)):
        return
    shape: Shape | None = current_shapes[selected_idx]
    if not shape:
        return

    handler.hover_shape = shape

    if not grid_rect or not grid_rect.collidepoint(mouse_pos):
        return

    grid_coords = vis_core.coord_mapper.get_grid_coords_from_screen(
        mouse_pos, grid_rect, game_state.env_config
    )

    if grid_coords:
        r, c = grid_coords
        potential_action = _encode_action(selected_idx, r, c, game_state.env_config)
        is_valid = (
            potential_action != -1 and potential_action in game_state.valid_actions()
        )
        handler.hover_grid_coord = grid_coords
        handler.hover_is_valid = is_valid
