# File: trianglengin/core/environment/grid/line_cache.py
import logging
from typing import Final, cast

import numpy as np

from trianglengin.config.env_config import EnvConfig

log = logging.getLogger(__name__)

# Type aliases
Coord = tuple[int, int]
Line = tuple[Coord, ...]
LineFsSet = set[frozenset[Coord]]
CoordMap = dict[Coord, LineFsSet]
ConfigKey = tuple[int, int, tuple[tuple[int, int], ...]]
CachedData = tuple[list[Line], CoordMap]
_LINE_CACHE: dict[ConfigKey, CachedData] = {}

# Directions
HORIZONTAL: Final = "h"
DIAGONAL_TL_BR: Final = "d1"
DIAGONAL_BL_TR: Final = "d2"


def _create_cache_key(config: EnvConfig) -> ConfigKey:
    """Creates an immutable cache key from relevant EnvConfig fields."""
    playable_ranges_tuple: tuple[tuple[int, int], ...] = cast(
        "tuple[tuple[int, int], ...]",
        tuple(tuple(item) for item in config.PLAYABLE_RANGE_PER_ROW),
    )
    return (
        config.ROWS,
        config.COLS,
        playable_ranges_tuple,
    )


def get_precomputed_lines_and_map(config: EnvConfig) -> CachedData:
    """
    Retrieves the precomputed maximal lines and the coordinate-to-lines map
    for a given configuration, using a cache. Computes if not found.
    """
    key = _create_cache_key(config)
    if key not in _LINE_CACHE:
        log.info(f"Cache miss for grid config: {key}. Computing maximal lines and map.")
        # Use the computation function v4
        _LINE_CACHE[key] = _compute_lines_and_map_v4(config)

    lines, coord_map = _LINE_CACHE[key]
    # Return copies to prevent modification of the cache
    return list(lines), {coord: set(lineset) for coord, lineset in coord_map.items()}


def _is_live(r: int, c: int, config: EnvConfig, playable_mask: np.ndarray) -> bool:
    """Checks if a cell is within bounds and the playable range for its row using precomputed mask."""
    # Bounds check first
    if not (0 <= r < config.ROWS and 0 <= c < config.COLS):
        return False
    # Check precomputed mask and cast to bool for mypy
    return bool(playable_mask[r, c])


def _get_neighbor(
    r: int, c: int, direction: str, backward: bool, config: EnvConfig
) -> Coord | None:
    """
    Gets the neighbor coordinate in a given direction (forward or backward).
    Requires config for bounds checking.
    """
    is_up = (r + c) % 2 != 0

    if direction == HORIZONTAL:
        dc = -1 if backward else 1
        nr, nc = r, c + dc
    elif direction == DIAGONAL_TL_BR:  # Top-Left to Bottom-Right
        if backward:  # Moving Up-Left
            nr, nc = (r - 1, c) if not is_up else (r, c - 1)
        else:  # Moving Down-Right
            nr, nc = (r + 1, c) if is_up else (r, c + 1)
    elif direction == DIAGONAL_BL_TR:  # Bottom-Left to Top-Right
        if backward:  # Moving Down-Left
            nr, nc = (r + 1, c) if is_up else (r, c - 1)
        else:  # Moving Up-Right
            nr, nc = (r - 1, c) if not is_up else (r, c + 1)
    else:
        raise ValueError(f"Unknown direction: {direction}")

    # Return None if neighbor is out of grid bounds (simplifies tracing loops)
    if not (0 <= nr < config.ROWS and 0 <= nc < config.COLS):
        return None
    return (nr, nc)


def _compute_lines_and_map_v4(config: EnvConfig) -> CachedData:
    """
    Generates all maximal potential horizontal and diagonal lines based on grid geometry
    and playable ranges. Builds the coordinate map.
    V4: Use trace-back-then-forward approach for each cell and direction.
    """
    rows, cols = config.ROWS, config.COLS
    maximal_lines_set: set[Line] = set()
    processed_starts: set[tuple[Coord, str]] = set()

    # --- Determine playable cells based on config ---
    playable_mask = np.zeros((rows, cols), dtype=bool)
    for r in range(rows):
        if r < len(config.PLAYABLE_RANGE_PER_ROW):
            start_col, end_col = config.PLAYABLE_RANGE_PER_ROW[r]
            if start_col < end_col:
                playable_mask[r, start_col:end_col] = True
    # --- End Playable Mask ---

    for r_init in range(rows):
        for c_init in range(cols):
            if not _is_live(r_init, c_init, config, playable_mask):
                continue

            current_coord = (r_init, c_init)

            for direction in [HORIZONTAL, DIAGONAL_TL_BR, DIAGONAL_BL_TR]:
                # 1. Trace backwards to find the true start of the segment
                line_start_coord = current_coord
                while True:
                    prev_coord_tuple = _get_neighbor(
                        line_start_coord[0],
                        line_start_coord[1],
                        direction,
                        backward=True,
                        config=config,  # Pass config here
                    )
                    if prev_coord_tuple and _is_live(
                        prev_coord_tuple[0], prev_coord_tuple[1], config, playable_mask
                    ):
                        line_start_coord = prev_coord_tuple
                    else:
                        break  # Found the start or hit boundary/non-playable

                # 2. Check if we've already processed this line from its start
                if (line_start_coord, direction) in processed_starts:
                    continue

                # 3. Trace forwards from the true start to build the maximal line
                current_line: list[Coord] = []
                trace_coord: Coord | None = line_start_coord
                while trace_coord and _is_live(
                    trace_coord[0], trace_coord[1], config, playable_mask
                ):
                    current_line.append(trace_coord)
                    trace_coord = _get_neighbor(
                        trace_coord[0],
                        trace_coord[1],
                        direction,
                        backward=False,
                        config=config,  # Pass config here
                    )

                # 4. Store the maximal line if it's not empty
                if current_line:
                    maximal_lines_set.add(tuple(current_line))
                    # Mark the start coordinate as processed for this direction
                    processed_starts.add((line_start_coord, direction))

    # --- Build Final List and Map ---
    final_lines_list = sorted(
        maximal_lines_set,
        key=lambda line: (
            line[0][0],
            line[0][1],
            len(line),
            line,
        ),  # Sort for deterministic order
    )

    coord_map: CoordMap = {}
    for line_tuple in final_lines_list:
        line_fs = frozenset(line_tuple)  # Use frozenset for map values
        for coord in line_tuple:
            if coord not in coord_map:
                coord_map[coord] = set()
            coord_map[coord].add(line_fs)

    key = _create_cache_key(config)
    log.info(
        f"Computed {len(final_lines_list)} unique maximal lines (v4) "
        f"and map for {len(coord_map)} coords for config {key}."
    )

    return final_lines_list, coord_map
