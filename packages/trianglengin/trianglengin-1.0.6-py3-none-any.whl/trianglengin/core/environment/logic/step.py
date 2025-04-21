# trianglengin/core/environment/logic/step.py
import logging
from typing import TYPE_CHECKING

# Import shapes module itself for ShapeLogic reference if needed later,
# though direct calls are used here.
from trianglengin.core.environment.grid import logic as GridLogic
from trianglengin.core.structs.constants import COLOR_TO_ID_MAP, NO_COLOR_ID

if TYPE_CHECKING:
    # Keep EnvConfig import for reward calculation
    from trianglengin.config import EnvConfig
    from trianglengin.core.environment.game_state import GameState
    from trianglengin.core.environment.grid.line_cache import Coord


logger = logging.getLogger(__name__)


def calculate_reward(
    placed_count: int,
    cleared_count: int,
    is_game_over: bool,
    config: "EnvConfig",
) -> float:
    """
    Calculates the step reward based on the new specification (v3).

    Args:
        placed_count: Number of triangles successfully placed.
        cleared_count: Number of unique triangles cleared this step.
        is_game_over: Boolean indicating if the game ended *after* this step.
        config: Environment configuration containing reward constants.

    Returns:
        The calculated step reward.
    """
    reward = 0.0

    # 1. Placement Reward
    reward += placed_count * config.REWARD_PER_PLACED_TRIANGLE

    # 2. Line Clear Reward
    reward += cleared_count * config.REWARD_PER_CLEARED_TRIANGLE

    # 3. Survival Reward OR Game Over Penalty
    if is_game_over:
        # Apply penalty only if game ended THIS step
        reward += config.PENALTY_GAME_OVER
    else:
        reward += config.REWARD_PER_STEP_ALIVE

    logger.debug(
        f"Calculated Reward: Placement({placed_count * config.REWARD_PER_PLACED_TRIANGLE:.3f}) "
        f"+ LineClear({cleared_count * config.REWARD_PER_CLEARED_TRIANGLE:.3f}) "
        f"+ {'GameOver' if is_game_over else 'Survival'}({config.PENALTY_GAME_OVER if is_game_over else config.REWARD_PER_STEP_ALIVE:.3f}) "
        f"= {reward:.3f}"
    )
    return reward


def execute_placement(
    game_state: "GameState", shape_idx: int, r: int, c: int
) -> tuple[int, int]:
    """
    Places a shape, clears lines, and updates grid/score state.
    Refill logic and reward calculation are handled by the caller (GameState.step).

    Args:
        game_state: The current game state (will be modified).
        shape_idx: Index of the shape to place.
        r: Target row for placement.
        c: Target column for placement.

    Returns:
        Tuple[int, int]: (cleared_triangle_count, placed_triangle_count)
                         Stats needed for reward calculation.
    Raises:
        ValueError: If placement is invalid (should be pre-checked).
        IndexError: If shape_idx is invalid.
    """
    if not (0 <= shape_idx < len(game_state.shapes)):
        raise IndexError(f"Invalid shape index: {shape_idx}")

    shape = game_state.shapes[shape_idx]
    if not shape:
        # This case should ideally be prevented by GameState.step checking valid_actions first.
        logger.error(f"Attempted to place an empty shape slot: {shape_idx}")
        raise ValueError("Cannot place an empty shape slot.")

    # Check placement validity using GridLogic - raise error if invalid
    if not GridLogic.can_place(game_state.grid_data, shape, r, c):
        # This case should ideally be prevented by GameState.step checking valid_actions first.
        logger.error(
            f"Invalid placement attempted in execute_placement: Shape {shape_idx} at ({r},{c}). "
            "This should have been caught earlier."
        )
        raise ValueError("Invalid placement location.")

    # --- Place the shape ---
    placed_coords: set[Coord] = set()
    placed_count = 0
    color_id = COLOR_TO_ID_MAP.get(shape.color, NO_COLOR_ID)
    if color_id == NO_COLOR_ID:
        # Use default color ID 0 if the test color isn't found
        logger.warning(
            f"Shape color {shape.color} not found in COLOR_TO_ID_MAP! Using ID 0."
        )
        color_id = 0

    for dr, dc, _ in shape.triangles:
        tri_r, tri_c = r + dr, c + dc
        # Assume valid coordinates as can_place passed and raised error otherwise
        game_state.grid_data._occupied_np[tri_r, tri_c] = True
        game_state.grid_data._color_id_np[tri_r, tri_c] = color_id
        placed_coords.add((tri_r, tri_c))
        placed_count += 1

    game_state.shapes[shape_idx] = None  # Remove shape from slot

    # --- Check and clear lines ---
    lines_cleared_count, unique_coords_cleared, _ = GridLogic.check_and_clear_lines(
        game_state.grid_data, placed_coords
    )
    cleared_count = len(unique_coords_cleared)

    # --- Update Score ---
    game_state._game_score += placed_count + cleared_count * 2

    # --- REMOVED REFILL LOGIC ---
    # --- REMOVED REWARD CALCULATION ---

    # Return stats needed by GameState.step for reward calculation
    return cleared_count, placed_count
