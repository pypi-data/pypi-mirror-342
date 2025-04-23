# File: tests/conftest.py
import random
from collections.abc import Generator

import pytest

from trianglengin.config import EnvConfig

# Use new interface types
from trianglengin.game_interface import GameState, Shape

# Import moved DisplayConfig if needed by UI tests (not needed here)
# from trianglengin.ui.config import DisplayConfig
# Import colors from the core vis module (if needed by fixtures)
# Note: Colors are now part of UI, avoid using them in core tests if possible
# from trianglengin.ui.visualization.core import colors

# Default color for fixture shapes
DEFAULT_TEST_COLOR = (100, 100, 100)  # Keep as tuple
DEFAULT_TEST_COLOR_ID = -10  # Assign an arbitrary negative ID for test shapes


@pytest.fixture(scope="session")
def default_env_config() -> EnvConfig:
    """Provides the default EnvConfig used in the specification (session-scoped)."""
    return EnvConfig()


@pytest.fixture
def game_state(default_env_config: EnvConfig) -> GameState:
    """Provides a fresh GameState wrapper instance for testing."""
    return GameState(config=default_env_config, initial_seed=123)


@pytest.fixture
def game_state_3x3() -> GameState:
    """Provides a game state wrapper for a 3x3 grid."""
    config_3x3 = EnvConfig(
        ROWS=3,
        COLS=3,
        PLAYABLE_RANGE_PER_ROW=[(0, 3), (0, 3), (0, 3)],
        NUM_SHAPE_SLOTS=3,
    )
    return GameState(config=config_3x3, initial_seed=456)


@pytest.fixture
def game_state_4x4() -> GameState:
    """Provides a game state wrapper for a 4x4 grid."""
    config_4x4 = EnvConfig(
        ROWS=4,
        COLS=4,
        PLAYABLE_RANGE_PER_ROW=[(0, 4), (0, 4), (0, 4), (0, 4)],
        NUM_SHAPE_SLOTS=3,
    )
    return GameState(config=config_4x4, initial_seed=789)


@pytest.fixture
def simple_shape() -> Shape:
    """Provides a simple 3-triangle connected shape (Down, Up, Down)."""
    triangles = [(0, 0, False), (0, 1, True), (1, 1, False)]
    color = (255, 0, 0)
    # Use the new Shape constructor
    return Shape(triangles, color, color_id=0)


@pytest.fixture
def single_up_triangle_shape() -> Shape:
    """Provides a shape consisting of a single Up triangle."""
    triangles = [(0, 0, True)]
    color = (0, 255, 0)  # Green
    return Shape(triangles, color, color_id=2)  # Assign an ID


@pytest.fixture
def game_state_almost_full(
    default_env_config: EnvConfig,
) -> Generator[GameState, None, None]:
    """
    Provides a game state (default config) where only a few placements are possible.
    Uses debug_toggle_cell to fill the grid.
    Yields the state and resets it afterwards.
    """
    gs = GameState(config=default_env_config, initial_seed=987)
    grid_data_np = gs.get_grid_data_np()
    rows, cols = grid_data_np["death"].shape

    for r in range(rows):
        for c in range(cols):
            if not grid_data_np["death"][r, c]:
                current_grid_data = gs.get_grid_data_np()
                if not current_grid_data["occupied"][r, c]:
                    gs.debug_toggle_cell(r, c)

    empty_spots = [(0, 4), (0, 5)]
    for r_empty, c_empty in empty_spots:
        current_grid_data = gs.get_grid_data_np()
        if (
            r_empty < gs.env_config.ROWS
            and c_empty < gs.env_config.COLS
            and not current_grid_data["death"][r_empty, c_empty]
            and current_grid_data["occupied"][r_empty, c_empty]
        ):
            gs.debug_toggle_cell(r_empty, c_empty)

    yield gs


@pytest.fixture
def fixed_rng() -> random.Random:
    """Provides a Random instance with a fixed seed."""
    return random.Random(12345)
