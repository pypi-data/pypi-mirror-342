# File: src/trianglengin/ui/app.py
import logging

# UI imports are now direct as dependencies are required
import pygame

# Use absolute imports from core engine
from trianglengin.config import EnvConfig
from trianglengin.game_interface import GameState
from trianglengin.ui import config as ui_config
from trianglengin.ui import interaction, visualization

logger = logging.getLogger(__name__)


class Application:
    """Main application integrating visualization and interaction for trianglengin."""

    def __init__(self, mode: str = "play") -> None:
        self.display_config = ui_config.DisplayConfig()  # Use UI config
        self.env_config = EnvConfig()  # Use core EnvConfig
        self.mode = mode

        pygame.init()
        pygame.font.init()
        self.screen = self._setup_screen()
        self.clock = pygame.time.Clock()
        self.fonts = visualization.load_fonts()  # From ui.visualization

        if self.mode in ["play", "debug"]:
            # GameState comes from the core engine
            self.game_state = GameState(self.env_config)
            # Visualizer and InputHandler come from the UI package
            self.visualizer = visualization.Visualizer(
                self.screen,
                self.display_config,
                self.env_config,
                self.fonts,
            )
            self.input_handler = interaction.InputHandler(
                self.game_state, self.visualizer, self.mode, self.env_config
            )
        else:
            logger.error(f"Unsupported application mode: {self.mode}")
            raise ValueError(f"Unsupported application mode: {self.mode}")

        self.running = True

    def _setup_screen(self) -> pygame.Surface:
        """Initializes the Pygame screen."""
        screen = pygame.display.set_mode(
            (
                self.display_config.SCREEN_WIDTH,
                self.display_config.SCREEN_HEIGHT,
            ),
            pygame.RESIZABLE,
        )
        pygame.display.set_caption(f"Triangle Engine - {self.mode.capitalize()} Mode")
        return screen

    def run(self) -> None:
        """Main application loop."""
        logger.info(f"Starting application in {self.mode} mode.")
        while self.running:
            self.clock.tick(self.display_config.FPS)

            if self.input_handler:
                self.running = self.input_handler.handle_input()
                if not self.running:
                    break
            else:
                # Basic event handling if input_handler fails (shouldn't happen)
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
