# File: trianglengin/tests/conftest.py
import random
from typing import TYPE_CHECKING

import numpy as np
import pytest

# Import directly from the library being tested
from trianglengin.config import EnvConfig
from trianglengin.core.environment import GameState
from trianglengin.core.structs import Shape
from trianglengin.visualization.core.colors import Color

if TYPE_CHECKING:
    from trianglengin.core.environment.grid import GridData


# Use default NumPy random number generator
rng = np.random.default_rng()

# Default color for fixture shapes
DEFAULT_TEST_COLOR: Color = (100, 100, 100)


@pytest.fixture(scope="session")
def default_env_config() -> EnvConfig:
    """Provides the default EnvConfig used in the specification (session-scoped)."""
    return EnvConfig()


@pytest.fixture
def game_state(default_env_config: EnvConfig) -> GameState:
    """Provides a fresh GameState instance for testing."""
    return GameState(config=default_env_config, initial_seed=123)


@pytest.fixture
def game_state_with_fixed_shapes() -> GameState:
    """
    Provides a game state with predictable initial shapes on a 3x3 grid.
    """
    # Create a specific 3x3 config for this fixture
    config_3x3 = EnvConfig(
        ROWS=3,
        COLS=3,
        PLAYABLE_RANGE_PER_ROW=[(0, 3), (0, 3), (0, 3)],  # Full 3x3 is playable
        NUM_SHAPE_SLOTS=3,
    )
    gs = GameState(config=config_3x3, initial_seed=456)

    # Override the random shapes with fixed ones for testing placement/refill
    fixed_shapes = [
        Shape([(0, 0, False)], DEFAULT_TEST_COLOR),  # Single down
        Shape([(0, 0, True)], DEFAULT_TEST_COLOR),  # Single up
        Shape(
            [(0, 0, False), (1, 0, False)], DEFAULT_TEST_COLOR
        ),  # Two downs (vertical)
    ]
    assert len(fixed_shapes) == gs.env_config.NUM_SHAPE_SLOTS

    # Assign copies of the shapes to the game state
    gs.shapes = [shape.copy() for shape in fixed_shapes]

    # Force recalculation of valid actions after manually setting shapes
    gs.valid_actions(force_recalculate=True)
    return gs


@pytest.fixture
def simple_shape() -> Shape:
    """Provides a simple 3-triangle connected shape (Down, Up, Down)."""
    triangles = [(0, 0, False), (0, 1, True), (1, 1, False)]
    color = (255, 0, 0)
    return Shape(triangles, color)


@pytest.fixture
def grid_data(default_env_config: EnvConfig) -> "GridData":
    """Provides a fresh GridData instance using the default config."""
    from trianglengin.core.environment.grid import GridData

    return GridData(config=default_env_config)


@pytest.fixture
def game_state_almost_full(default_env_config: EnvConfig) -> GameState:
    """
    Provides a game state (default config) where only a few placements are possible.
    Grid is filled completely, then specific spots are made empty.
    """
    gs = GameState(config=default_env_config, initial_seed=987)
    playable_mask = ~gs.grid_data._death_np
    gs.grid_data._occupied_np[playable_mask] = True
    empty_spots = [(0, 4), (0, 5)]  # Example empty spots
    for r_empty, c_empty in empty_spots:
        if (
            gs.grid_data.valid(r_empty, c_empty)
            and not gs.grid_data._death_np[r_empty, c_empty]
        ):
            gs.grid_data._occupied_np[r_empty, c_empty] = False
            gs.grid_data._color_id_np[r_empty, c_empty] = -1
    return gs


@pytest.fixture
def fixed_rng() -> random.Random:
    """Provides a Random instance with a fixed seed."""
    return random.Random(12345)
