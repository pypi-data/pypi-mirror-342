# File: trianglengin/core/environment/grid/grid_data.py
import logging

import numpy as np

from trianglengin.config.env_config import EnvConfig
from trianglengin.core.environment.grid.line_cache import (
    CoordMap,
    Line,
    get_precomputed_lines_and_map,
)

log = logging.getLogger(__name__)


class GridData:
    """Stores and manages the state of the game grid."""

    __slots__ = (
        "config",
        "rows",
        "cols",
        "_occupied_np",
        "_color_id_np",
        "_death_np",
        "_lines",
        "_coord_to_lines_map",
    )

    def __init__(self, config: EnvConfig):
        """
        Initializes the grid based on the provided configuration.
        Death zones are set based on PLAYABLE_RANGE_PER_ROW.

        Args:
            config: The environment configuration dataclass.
        """
        self.config: EnvConfig = config
        self.rows: int = config.ROWS
        self.cols: int = config.COLS

        self._occupied_np: np.ndarray = np.full(
            (self.rows, self.cols), False, dtype=bool
        )
        self._color_id_np: np.ndarray = np.full(
            (self.rows, self.cols), -1, dtype=np.int8
        )
        # Initialize all as death, then mark playable area as not death
        self._death_np: np.ndarray = np.full((self.rows, self.cols), True, dtype=bool)

        for r in range(self.rows):
            start_col, end_col = config.PLAYABLE_RANGE_PER_ROW[r]
            if start_col < end_col:  # Ensure valid range
                self._death_np[r, start_col:end_col] = False  # Mark playable cols

        # Get Precomputed Lines and Map from Cache
        self._lines: list[Line]
        self._coord_to_lines_map: CoordMap
        self._lines, self._coord_to_lines_map = get_precomputed_lines_and_map(config)

        log.debug(
            f"GridData initialized: {self.rows}x{self.cols}, "
            f"{np.sum(self._death_np)} death cells, "
            f"{len(self._lines)} precomputed lines, "
            f"{len(self._coord_to_lines_map)} mapped coords."
        )

    def reset(self) -> None:
        """Resets the grid to an empty state (occupied and colors)."""
        self._occupied_np.fill(False)
        self._color_id_np.fill(-1)
        log.debug("GridData reset.")

    def is_empty(self) -> bool:
        """Checks if the grid has any occupied cells (excluding death zones)."""
        # Consider only non-death cells for emptiness check
        playable_mask = ~self._death_np
        return not self._occupied_np[playable_mask].any()

    def valid(self, r: int, c: int) -> bool:
        """Checks if the coordinates (r, c) are within the grid bounds."""
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_death(self, r: int, c: int) -> bool:
        """
        Checks if the cell (r, c) is a death zone.

        Raises:
            IndexError: If (r, c) is out of bounds.
        """
        if not self.valid(r, c):
            raise IndexError(
                f"Coordinates ({r},{c}) out of bounds ({self.rows}x{self.cols})."
            )
        return bool(self._death_np[r, c])

    def is_occupied(self, r: int, c: int) -> bool:
        """
        Checks if the cell (r, c) is occupied by a triangle piece.
        Returns False for death zones, regardless of the underlying array value.

        Raises:
            IndexError: If (r, c) is out of bounds.
        """
        if not self.valid(r, c):
            raise IndexError(
                f"Coordinates ({r},{c}) out of bounds ({self.rows}x{self.cols})."
            )
        if self._death_np[r, c]:
            return False
        return bool(self._occupied_np[r, c])

    def get_color_id(self, r: int, c: int) -> int | None:
        """
        Gets the color ID of the triangle at (r, c).

        Returns None if the cell is empty, a death zone, or out of bounds.
        """
        if not self.valid(r, c) or self._death_np[r, c] or not self._occupied_np[r, c]:
            return None
        return int(self._color_id_np[r, c])

    def __deepcopy__(self, memo):
        """Custom deepcopy implementation."""
        new_grid = GridData.__new__(GridData)
        memo[id(self)] = new_grid

        new_grid.config = self.config
        new_grid.rows = self.rows
        new_grid.cols = self.cols
        new_grid._occupied_np = self._occupied_np.copy()
        new_grid._color_id_np = self._color_id_np.copy()
        new_grid._death_np = self._death_np.copy()

        # Lines list and map are obtained from cache, but need copying for the instance
        new_grid._lines, new_grid._coord_to_lines_map = get_precomputed_lines_and_map(
            self.config
        )

        return new_grid
