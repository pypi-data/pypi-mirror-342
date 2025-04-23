import logging

import numpy as np
import pygame  # Now a required dependency

# Use absolute imports for core components
from trianglengin.config import EnvConfig
from trianglengin.game_interface import GameState, Shape

# Use absolute imports within UI package where needed
from trianglengin.ui.config import DisplayConfig

# Import specific modules directly from the core package
from trianglengin.ui.visualization.core import colors, coord_mapper
from trianglengin.ui.visualization.core import (
    layout as layout_module,
)  # Import layout directly

# Import drawing functions using absolute paths
from trianglengin.ui.visualization.drawing import grid as grid_drawing
from trianglengin.ui.visualization.drawing import highlight as highlight_drawing
from trianglengin.ui.visualization.drawing import hud as hud_drawing
from trianglengin.ui.visualization.drawing import previews as preview_drawing
from trianglengin.ui.visualization.drawing.previews import (
    draw_floating_preview,
    draw_placement_preview,
)

logger = logging.getLogger(__name__)


class Visualizer:
    """
    Orchestrates rendering of a single game state for interactive modes.
    Uses the GameState wrapper to access C++ state.
    Receives interaction state (hover, selection) via render parameters.
    """

    def __init__(
        self,
        screen: pygame.Surface,
        display_config: DisplayConfig,  # From UI config
        env_config: EnvConfig,  # From core config
        fonts: dict[str, pygame.font.Font | None],
    ) -> None:
        self.screen = screen
        self.display_config = display_config
        self.env_config = env_config
        self.fonts = fonts
        self.layout_rects: dict[str, pygame.Rect] | None = None
        self.preview_rects: dict[int, pygame.Rect] = {}
        self._layout_calculated_for_size: tuple[int, int] = (0, 0)
        self.ensure_layout()

    def ensure_layout(self) -> dict[str, pygame.Rect]:
        """Returns cached layout or calculates it if needed."""
        current_w, current_h = self.screen.get_size()
        current_size = (current_w, current_h)

        if (
            self.layout_rects is None
            or self._layout_calculated_for_size != current_size
        ):
            # Call the function via the imported module
            self.layout_rects = layout_module.calculate_interactive_layout(
                current_w,
                current_h,
                self.display_config,
            )
            self._layout_calculated_for_size = current_size
            logger.info(
                f"Recalculated interactive layout for size {current_size}: {self.layout_rects}"
            )
            self.preview_rects = {}  # Clear preview rect cache on layout change

        return self.layout_rects if self.layout_rects is not None else {}

    def render(
        self,
        game_state: GameState,  # Core GameState
        mode: str,
        selected_shape_idx: int = -1,
        hover_shape: Shape | None = None,  # Core Shape
        hover_grid_coord: tuple[int, int] | None = None,
        hover_is_valid: bool = False,
        hover_screen_pos: tuple[int, int] | None = None,
        debug_highlight_coord: tuple[int, int] | None = None,
    ) -> None:
        """Renders the entire game visualization for interactive modes."""
        self.screen.fill(colors.GRID_BG_DEFAULT)
        layout_rects = self.ensure_layout()
        grid_rect = layout_rects.get("grid")
        preview_rect = layout_rects.get("preview")

        grid_data_np = game_state.get_grid_data_np()

        if grid_rect and grid_rect.width > 0 and grid_rect.height > 0:
            try:
                grid_surf = self.screen.subsurface(grid_rect)
                cw, ch, ox, oy = coord_mapper._calculate_render_params(
                    grid_rect.width, grid_rect.height, self.env_config
                )
                self._render_grid_area(
                    grid_surf,
                    game_state,
                    grid_data_np,
                    mode,
                    grid_rect,
                    hover_shape,
                    hover_grid_coord,
                    hover_is_valid,
                    hover_screen_pos,
                    debug_highlight_coord,
                    cw,
                    ch,
                    ox,
                    oy,
                )
            except ValueError as e:
                logger.error(f"Error creating grid subsurface ({grid_rect}): {e}")
                pygame.draw.rect(self.screen, colors.RED, grid_rect, 1)

        if preview_rect and preview_rect.width > 0 and preview_rect.height > 0:
            try:
                preview_surf = self.screen.subsurface(preview_rect)
                self._render_preview_area(
                    preview_surf, game_state, mode, preview_rect, selected_shape_idx
                )
            except ValueError as e:
                logger.error(f"Error creating preview subsurface ({preview_rect}): {e}")
                pygame.draw.rect(self.screen, colors.RED, preview_rect, 1)

        hud_drawing.render_hud(
            surface=self.screen,
            mode=mode,
            fonts=self.fonts,
        )

    def _render_grid_area(
        self,
        grid_surf: pygame.Surface,
        game_state: GameState,
        grid_data_np: dict[str, np.ndarray],
        mode: str,
        grid_rect: pygame.Rect,
        hover_shape: Shape | None,
        hover_grid_coord: tuple[int, int] | None,
        hover_is_valid: bool,
        hover_screen_pos: tuple[int, int] | None,
        debug_highlight_coord: tuple[int, int] | None,
        cw: float,
        ch: float,
        ox: float,
        oy: float,
    ) -> None:
        """Renders the main game grid and overlays onto the provided grid_surf."""
        grid_drawing.draw_grid_background(
            grid_surf,
            self.env_config,
            self.display_config,
            cw,
            ch,
            ox,
            oy,
            game_state.is_over(),
            mode == "debug",
            death_mask_np=grid_data_np["death"],
        )

        grid_drawing.draw_grid_state(
            grid_surf,
            occupied_np=grid_data_np["occupied"],
            color_id_np=grid_data_np["color_id"],
            death_np=grid_data_np["death"],
            rows=self.env_config.ROWS,
            cols=self.env_config.COLS,
            cw=cw,
            ch=ch,
            ox=ox,
            oy=oy,
        )

        if mode == "play" and hover_shape:
            if hover_grid_coord:
                draw_placement_preview(
                    grid_surf,
                    hover_shape,
                    hover_grid_coord[0],
                    hover_grid_coord[1],
                    is_valid=hover_is_valid,
                    cw=cw,
                    ch=ch,
                    ox=ox,
                    oy=oy,
                )
            elif hover_screen_pos:
                local_hover_pos = (
                    hover_screen_pos[0] - grid_rect.left,
                    hover_screen_pos[1] - grid_rect.top,
                )
                if grid_surf.get_rect().collidepoint(local_hover_pos):
                    draw_floating_preview(
                        grid_surf,
                        hover_shape,
                        local_hover_pos,
                    )

        if mode == "debug" and debug_highlight_coord:
            r, c = debug_highlight_coord
            highlight_drawing.draw_debug_highlight(
                grid_surf,
                r,
                c,
                cw=cw,
                ch=ch,
                ox=ox,
                oy=oy,
            )

        score_font = self.fonts.get("score")
        if score_font:
            score_text = f"Score: {game_state.game_score():.0f}"
            score_surf = score_font.render(score_text, True, colors.YELLOW)
            score_rect = score_surf.get_rect(topleft=(5, 5))
            grid_surf.blit(score_surf, score_rect)

    def _render_preview_area(
        self,
        preview_surf: pygame.Surface,
        game_state: GameState,
        mode: str,
        preview_rect: pygame.Rect,
        selected_shape_idx: int,
    ) -> None:
        """Renders the shape preview slots onto preview_surf and caches rects."""
        current_shapes = game_state.get_shapes()
        current_preview_rects = preview_drawing.render_previews(
            preview_surf,
            current_shapes,
            preview_rect.topleft,
            mode,
            self.env_config,
            self.display_config,
            selected_shape_idx=selected_shape_idx,
        )
        # Cache the absolute screen coordinates of the preview slots
        if not self.preview_rects or self.preview_rects != current_preview_rects:
            self.preview_rects = current_preview_rects
