# File: trianglengin/trianglengin/core/environment/shapes/logic.py
import logging
import random
from typing import TYPE_CHECKING

from ...structs import SHAPE_COLORS, Shape  # Import from library's structs
from .templates import PREDEFINED_SHAPE_TEMPLATES

if TYPE_CHECKING:
    # Use relative import for GameState within the library
    from ..game_state import GameState

logger = logging.getLogger(__name__)


def generate_random_shape(rng: random.Random) -> Shape:
    """Generates a random shape from predefined templates and colors."""
    template = rng.choice(PREDEFINED_SHAPE_TEMPLATES)
    color = rng.choice(SHAPE_COLORS)
    return Shape(template, color)


def refill_shape_slots(game_state: "GameState", rng: random.Random) -> None:
    """
    Refills ALL empty shape slots in the GameState, but ONLY if ALL slots are currently empty.
    This implements batch refilling.
    """
    if all(shape is None for shape in game_state.shapes):
        logger.debug("All shape slots are empty. Refilling all slots.")
        for i in range(game_state.env_config.NUM_SHAPE_SLOTS):
            game_state.shapes[i] = generate_random_shape(rng)
            logger.debug(f"Refilled slot {i} with {game_state.shapes[i]}")
    else:
        logger.debug("Not all shape slots are empty. Skipping refill.")


def get_neighbors(r: int, c: int, is_up: bool) -> list[tuple[int, int]]:
    """Gets potential neighbor coordinates for connectivity check."""
    if is_up:
        # Up triangle neighbors: (r, c-1), (r, c+1), (r+1, c)
        return [(r, c - 1), (r, c + 1), (r + 1, c)]
    else:
        # Down triangle neighbors: (r, c-1), (r, c+1), (r-1, c)
        return [(r, c - 1), (r, c + 1), (r - 1, c)]


def is_shape_connected(shape: Shape) -> bool:
    """Checks if all triangles in a shape are connected using BFS."""
    if not shape.triangles or len(shape.triangles) <= 1:
        return True

    # --- CORRECTED BFS LOGIC V2 ---
    # Store the actual triangle tuples (r, c, is_up) in a set for quick lookup
    all_triangles_set = set(shape.triangles)
    # Also store just the coordinates for quick neighbor checking
    all_coords_set = {(r, c) for r, c, _ in shape.triangles}

    start_triangle = shape.triangles[0]  # (r, c, is_up)

    visited: set[tuple[int, int, bool]] = set()
    queue: list[tuple[int, int, bool]] = [start_triangle]
    visited.add(start_triangle)

    while queue:
        current_r, current_c, current_is_up = queue.pop(0)

        # Check neighbors based on the current triangle's orientation
        for nr, nc in get_neighbors(current_r, current_c, current_is_up):
            # Check if the neighbor *coordinate* exists in the shape
            if (nr, nc) in all_coords_set:
                # Find the full neighbor triangle tuple (r, c, is_up)
                neighbor_triangle: tuple[int, int, bool] | None = None
                for tri_tuple in all_triangles_set:
                    if tri_tuple[0] == nr and tri_tuple[1] == nc:
                        neighbor_triangle = tri_tuple
                        break

                # If the neighbor exists in the shape and hasn't been visited
                if neighbor_triangle and neighbor_triangle not in visited:
                    visited.add(neighbor_triangle)
                    queue.append(neighbor_triangle)
    # --- END CORRECTED BFS LOGIC V2 ---

    return len(visited) == len(all_triangles_set)
