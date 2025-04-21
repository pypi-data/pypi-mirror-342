import logging

# Use absolute imports for core components
from trianglengin.config import EnvConfig
from trianglengin.game_interface import GameState, Shape

# Guard UI imports
try:
    import pygame

    from ..visualization import Visualizer  # Relative import within UI package
    from . import debug_mode_handler, event_processor, play_mode_handler  # Relative
except ImportError as e:
    raise ImportError(
        "UI components require 'pygame'. Install with 'pip install trianglengin[ui]'."
    ) from e


logger = logging.getLogger(__name__)


class InputHandler:
    """
    Handles user input, manages interaction state (selection, hover),
    and delegates actions to mode-specific handlers. Uses the GameState wrapper.
    """

    def __init__(
        self,
        game_state: GameState,  # Uses the core GameState wrapper
        visualizer: Visualizer,  # Uses the UI Visualizer
        mode: str,
        env_config: EnvConfig,  # Uses the core EnvConfig
    ):
        self.game_state = game_state
        self.visualizer = visualizer
        self.mode = mode
        self.env_config = env_config

        # Interaction state managed here
        self.selected_shape_idx: int = -1
        self.hover_grid_coord: tuple[int, int] | None = None
        self.hover_is_valid: bool = False
        self.hover_shape: Shape | None = None  # Uses the core Shape struct
        self.debug_highlight_coord: tuple[int, int] | None = None
        self.mouse_pos: tuple[int, int] = (0, 0)

    def handle_input(self) -> bool:
        """Processes Pygame events and updates state based on mode. Returns False to quit."""
        self.mouse_pos = pygame.mouse.get_pos()

        # Reset hover/highlight state each frame before processing events/updates
        self.hover_grid_coord = None
        self.hover_is_valid = False
        self.hover_shape = None
        self.debug_highlight_coord = None

        running = True
        event_generator = event_processor.process_pygame_events(self.visualizer)
        try:
            while True:
                event = next(event_generator)
                # Pass self to handlers so they can modify interaction state
                if self.mode == "play":
                    play_mode_handler.handle_play_click(event, self)
                elif self.mode == "debug":
                    debug_mode_handler.handle_debug_click(event, self)
        except StopIteration as e:
            running = e.value  # False if quit requested

        # Update hover state after processing events
        if running:
            if self.mode == "play":
                play_mode_handler.update_play_hover(self)
            elif self.mode == "debug":
                debug_mode_handler.update_debug_hover(self)

        return running

    def get_render_interaction_state(self) -> dict:
        """Returns interaction state needed by Visualizer.render"""
        return {
            "selected_shape_idx": self.selected_shape_idx,
            "hover_shape": self.hover_shape,
            "hover_grid_coord": self.hover_grid_coord,
            "hover_is_valid": self.hover_is_valid,
            "hover_screen_pos": self.mouse_pos,
            "debug_highlight_coord": self.debug_highlight_coord,
        }
