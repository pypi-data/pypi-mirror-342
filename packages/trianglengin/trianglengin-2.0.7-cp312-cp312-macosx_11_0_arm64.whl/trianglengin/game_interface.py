# File: src/trianglengin/game_interface.py
import logging
import random
from typing import Any, cast

import numpy as np

from .config import EnvConfig

try:
    import trianglengin.trianglengin_cpp as cpp_module
except ImportError as e:
    raise ImportError(
        "Trianglengin C++ extension module ('trianglengin.trianglengin_cpp') not found. "
        "Ensure the package was built correctly (`pip install -e .`). "
        f"Original error: {e}"
    ) from e


class Shape:
    """Python representation of a shape's data returned from C++."""

    def __init__(
        self,
        triangles: list[tuple[int, int, bool]],
        color: tuple[int, int, int],
        color_id: int,
    ):
        self.triangles: list[tuple[int, int, bool]] = sorted(triangles)
        self.color: tuple[int, int, int] = color
        self.color_id: int = color_id

    def bbox(self) -> tuple[int, int, int, int]:
        """Calculates bounding box (min_r, min_c, max_r, max_c) in relative coords."""
        if not self.triangles:
            return (0, 0, 0, 0)
        rows = [t[0] for t in self.triangles]
        cols = [t[1] for t in self.triangles]
        return (min(rows), min(cols), max(rows), max(cols))

    def copy(self) -> "Shape":
        """Creates a shallow copy."""
        return Shape(list(self.triangles), self.color, self.color_id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Shape):
            return NotImplemented
        return (
            self.triangles == other.triangles
            and self.color == other.color
            and self.color_id == other.color_id
        )

    def __hash__(self) -> int:
        return hash((tuple(self.triangles), self.color, self.color_id))

    def __str__(self) -> str:
        return f"Shape(ColorID:{self.color_id}, Tris:{len(self.triangles)})"

    def to_cpp_repr(
        self,
    ) -> tuple[list[tuple[int, int, bool]], tuple[int, int, int], int]:
        """Converts this Python Shape object to the tuple format expected by C++ bindings."""
        return self.triangles, self.color, self.color_id


log = logging.getLogger(__name__)


class GameState:
    """
    Python wrapper for the C++ GameState implementation.
    Provides a Pythonic interface to the core game logic.
    """

    _cpp_state: cpp_module.GameStateCpp

    def __init__(
        self, config: EnvConfig | None = None, initial_seed: int | None = None
    ):
        self.env_config: EnvConfig = config if config else EnvConfig()
        used_seed = (
            initial_seed if initial_seed is not None else random.randint(0, 2**32 - 1)
        )
        try:
            self._cpp_state = cpp_module.GameStateCpp(self.env_config, used_seed)
        except Exception as e:
            log.exception(f"Failed to initialize C++ GameStateCpp: {e}")
            raise
        self._cached_shapes: list[Shape | None] | None = None
        self._cached_grid_data: dict[str, np.ndarray] | None = None

    def reset(self) -> None:
        """Resets the game to an initial state."""
        self._cpp_state.reset()
        self._clear_caches()
        log.debug("Python GameState wrapper reset.")

    def step(self, action: int) -> tuple[float, bool]:
        """
        Performs one game step based on the chosen action index.
        Returns: (reward, done)
        """
        try:
            reward, done = cast("tuple[float, bool]", self._cpp_state.step(action))
            self._clear_caches()
            return reward, done
        except Exception as e:
            log.exception(f"Error during C++ step execution for action {action}: {e}")
            return self.env_config.PENALTY_GAME_OVER, True

    def is_over(self) -> bool:
        """Checks if the game is over."""
        return cast("bool", self._cpp_state.is_over())

    def game_score(self) -> float:
        """Returns the current accumulated score."""
        return cast("float", self._cpp_state.get_score())

    def get_outcome(self) -> float:
        """
        Returns the final outcome of the game if it's over, otherwise 0.0.
        Required by MCTS implementations like trimcts.
        """
        if self.is_over():
            return self.game_score()
        else:
            return 0.0

    def valid_actions(self, force_recalculate: bool = False) -> set[int]:
        """
        Returns a set of valid encoded action indices for the current state.
        """
        return cast(
            "set[int]", set(self._cpp_state.get_valid_actions(force_recalculate))
        )

    def get_shapes(self) -> list[Shape | None]:
        """Returns the list of current shapes in the preview slots."""
        if self._cached_shapes is None:
            shapes_data = self._cpp_state.get_shapes_cpp()
            self._cached_shapes = []
            for data in shapes_data:
                if data is None:
                    self._cached_shapes.append(None)
                else:
                    tris_py, color_py, id_py = cast(
                        "tuple[list[tuple[int, int, bool]], tuple[int, int, int], int]",
                        data,
                    )
                    self._cached_shapes.append(Shape(tris_py, color_py, id_py))
        return self._cached_shapes

    def get_grid_data_np(self) -> dict[str, np.ndarray]:
        """
        Returns the grid state (occupied, colors, death) as NumPy arrays.
        Uses cached data if available.
        """
        if self._cached_grid_data is None:
            occupied_np = self._cpp_state.get_grid_occupied_flat()
            color_id_np = self._cpp_state.get_grid_colors_flat()
            death_np = self._cpp_state.get_grid_death_flat()
            self._cached_grid_data = {
                "occupied": occupied_np,
                "color_id": color_id_np,
                "death": death_np,
            }
        return self._cached_grid_data

    @property
    def current_step(self) -> int:
        """Returns the current step count."""
        return cast("int", self._cpp_state.get_current_step())

    def get_last_cleared_triangles(self) -> int:
        """Returns the number of triangles cleared in the most recent step."""
        return cast("int", self._cpp_state.get_last_cleared_triangles())

    def get_game_over_reason(self) -> str | None:
        """Returns the reason why the game ended, if it's over."""
        return cast("str | None", self._cpp_state.get_game_over_reason())

    def copy(self) -> "GameState":
        """Creates a deep copy of the game state."""
        new_wrapper = GameState.__new__(GameState)
        new_wrapper.env_config = self.env_config
        new_wrapper._cpp_state = self._cpp_state.copy()
        new_wrapper._cached_shapes = None
        new_wrapper._cached_grid_data = None
        return new_wrapper

    def debug_toggle_cell(self, r: int, c: int) -> None:
        """Toggles the state of a cell via the C++ implementation."""
        self._cpp_state.debug_toggle_cell(r, c)
        self._clear_caches()

    def debug_set_shapes(self, shapes: list[Shape | None]) -> None:
        """
        Directly sets the shapes in the preview slots. For debugging/testing.
        """
        shapes_data = [s.to_cpp_repr() if s else None for s in shapes]
        self._cpp_state.debug_set_shapes(shapes_data)
        self._clear_caches()

    def _clear_caches(self) -> None:
        """Clears Python-level caches."""
        self._cached_shapes = None
        self._cached_grid_data = None

    def __str__(self) -> str:
        shapes_repr = [str(s) if s else "None" for s in self.get_shapes()]
        status = "Over" if self.is_over() else "Ongoing"
        return (
            f"GameState(Step:{self.current_step}, Score:{self.game_score():.1f}, "
            f"Status:{status}, Shapes:[{', '.join(shapes_repr)}])"
        )

    @property
    def cpp_state(self) -> Any:
        """Returns the underlying C++ GameState object."""
        return self._cpp_state
