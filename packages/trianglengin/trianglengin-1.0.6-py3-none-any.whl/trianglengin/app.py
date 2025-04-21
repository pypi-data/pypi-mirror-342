import logging

import pygame

# Use internal imports
from . import config as tg_config
from . import core as tg_core
from . import interaction, visualization

logger = logging.getLogger(__name__)


class Application:
    """Main application integrating visualization and interaction for trianglengin."""

    def __init__(self, mode: str = "play"):
        # Use DisplayConfig from this library now
        self.display_config = tg_config.DisplayConfig()  # Use DisplayConfig
        self.env_config = tg_config.EnvConfig()
        self.mode = mode

        pygame.init()
        pygame.font.init()
        self.screen = self._setup_screen()
        self.clock = pygame.time.Clock()
        self.fonts = visualization.load_fonts()

        if self.mode in ["play", "debug"]:
            # Create GameState using trianglengin core
            self.game_state = tg_core.environment.GameState(self.env_config)
            # Create Visualizer using trianglengin visualization
            self.visualizer = visualization.Visualizer(
                self.screen,
                self.display_config,
                self.env_config,
                self.fonts,  # Pass DisplayConfig
            )
            # Create InputHandler using trianglengin interaction
            self.input_handler = interaction.InputHandler(
                self.game_state, self.visualizer, self.mode, self.env_config
            )
        else:
            # Handle other modes or raise error if necessary
            logger.error(f"Unsupported application mode: {self.mode}")
            raise ValueError(f"Unsupported application mode: {self.mode}")

        self.running = True

    def _setup_screen(self) -> pygame.Surface:
        """Initializes the Pygame screen."""
        screen = pygame.display.set_mode(
            (
                self.display_config.SCREEN_WIDTH,
                self.display_config.SCREEN_HEIGHT,
            ),  # Use DisplayConfig
            pygame.RESIZABLE,
        )
        # Use a generic name or make APP_NAME part of trianglengin config later
        pygame.display.set_caption(f"Triangle Engine - {self.mode.capitalize()} Mode")
        return screen

    def run(self):
        """Main application loop."""
        logger.info(f"Starting application in {self.mode} mode.")
        while self.running:
            self.clock.tick(self.display_config.FPS)  # Use DisplayConfig

            # Handle Input using InputHandler
            if self.input_handler:
                self.running = self.input_handler.handle_input()
                if not self.running:
                    break
            else:
                # Fallback event handling (should not happen in play/debug)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.type == pygame.VIDEORESIZE and self.visualizer:
                        try:
                            w, h = max(320, event.w), max(240, event.h)
                            self.visualizer.screen = pygame.display.set_mode(
                                (w, h), pygame.RESIZABLE
                            )
                            self.visualizer.layout_rects = None
                        except pygame.error as e:
                            logger.error(f"Error resizing window: {e}")
                if not self.running:
                    break

            # Render using Visualizer
            if (
                self.mode in ["play", "debug"]
                and self.visualizer
                and self.game_state
                and self.input_handler
            ):
                interaction_render_state = (
                    self.input_handler.get_render_interaction_state()
                )
                self.visualizer.render(
                    self.game_state,
                    self.mode,
                    **interaction_render_state,
                )
                pygame.display.flip()

        logger.info("Application loop finished.")
        pygame.quit()
