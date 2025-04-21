# trianglengin/core/environment/game_state.py
import copy
import logging
import random
from typing import TYPE_CHECKING

from trianglengin.config.env_config import EnvConfig
from trianglengin.core.environment.action_codec import (
    ActionType,
    decode_action,
)
from trianglengin.core.environment.grid.grid_data import GridData
from trianglengin.core.environment.logic.actions import get_valid_actions

# Import calculate_reward and execute_placement from step logic
from trianglengin.core.environment.logic.step import calculate_reward, execute_placement
from trianglengin.core.environment.shapes import logic as ShapeLogic

if TYPE_CHECKING:
    from trianglengin.core.structs.shape import Shape


log = logging.getLogger(__name__)


class GameState:
    """
    Represents the mutable state of the game environment.
    """

    def __init__(
        self, config: EnvConfig | None = None, initial_seed: int | None = None
    ):
        self.env_config: EnvConfig = config if config else EnvConfig()
        self._rng = random.Random(initial_seed)
        self.grid_data: GridData = GridData(self.env_config)
        self.shapes: list[Shape | None] = [None] * self.env_config.NUM_SHAPE_SLOTS
        self._game_score: float = 0.0
        self._game_over: bool = False
        self._game_over_reason: str | None = None
        self.current_step: int = 0
        self._valid_actions_cache: set[ActionType] | None = None
        self.reset()

    def reset(self) -> None:
        """Resets the game to an initial state."""
        self.grid_data.reset()
        self.shapes = [None] * self.env_config.NUM_SHAPE_SLOTS
        self._game_score = 0.0
        self._game_over = False
        self._game_over_reason = None
        self.current_step = 0
        self._valid_actions_cache = None
        ShapeLogic.refill_shape_slots(self, self._rng)  # Initial fill
        if not self.valid_actions():  # Check if initial state is game over
            self._game_over = True
            self._game_over_reason = "No valid actions available at start."
            log.warning(self._game_over_reason)

    def step(self, action_index: ActionType) -> tuple[float, bool]:
        """
        Performs one game step based on the chosen action.
        Handles placement, line clearing, scoring, refilling, and game over checks.
        Returns: (reward, done)
        Raises: ValueError if action is invalid or placement fails.
        """
        if self.is_over():
            log.warning("Attempted to step in a game that is already over.")
            return 0.0, True

        # Check action validity before execution
        current_valid_actions = self.valid_actions()
        if action_index not in current_valid_actions:
            log.error(
                f"Invalid action {action_index} provided. Valid: {current_valid_actions}"
            )
            raise ValueError("Action is not in the set of valid actions")

        shape_idx, r, c = decode_action(action_index, self.env_config)

        # --- Execute Placement and Get Stats ---
        try:
            # execute_placement now only returns counts and raises error on failure
            cleared_count, placed_count = execute_placement(self, shape_idx, r, c)
        except (ValueError, IndexError) as e:
            # Catch errors from execute_placement (e.g., invalid placement attempt)
            log.critical(
                f"Critical error during placement execution: {e}", exc_info=True
            )
            # Force game over with a penalty
            self.force_game_over(f"Placement execution error: {e}")
            # Return penalty, game is over
            return calculate_reward(0, 0, True, self.env_config), True

        # --- Refill shapes IF AND ONLY IF all slots are now empty ---
        if all(s is None for s in self.shapes):
            log.debug("All shape slots empty after placement, triggering refill.")
            ShapeLogic.refill_shape_slots(self, self._rng)
            # Refill might make new actions available, so clear cache before final check
            self._valid_actions_cache = None
        else:
            # Invalidate cache anyway as grid state or shapes list changed
            self._valid_actions_cache = None

        self.current_step += 1

        # --- Final Game Over Check ---
        # Check if any valid actions exist *after* placement and potential refill.
        # Calling valid_actions() populates the cache and returns the set.
        has_valid_moves_now = bool(self.valid_actions())

        # Update the game over state based on the check
        is_final_step_game_over = not has_valid_moves_now
        if is_final_step_game_over and not self._game_over:
            self._game_over = True
            self._game_over_reason = "No valid actions available after step."
            log.info(f"Game over at step {self.current_step}: {self._game_over_reason}")
        # Note: If game was already over, self._game_over remains True

        # --- Calculate Reward ---
        # Reward depends on placement/clear counts and the final game over state for THIS step
        reward = calculate_reward(
            placed_count=placed_count,
            cleared_count=cleared_count,
            is_game_over=self._game_over,  # Use the definitive game over state
            config=self.env_config,
        )

        # Return the calculated reward and the definitive game over status
        return reward, self._game_over

    def valid_actions(self, force_recalculate: bool = False) -> set[ActionType]:
        """
        Returns a set of valid encoded action indices for the current state.
        Uses a cache for performance unless force_recalculate is True.
        """
        if not force_recalculate and self._valid_actions_cache is not None:
            return self._valid_actions_cache

        # If game is already marked as over, no need to calculate, return empty set
        if self._game_over:
            if (
                self._valid_actions_cache is None
            ):  # Ensure cache is set if accessed after forced over
                self._valid_actions_cache = set()
            return set()

        # Calculate fresh valid actions
        current_valid_actions = get_valid_actions(self)
        # Update cache before returning
        self._valid_actions_cache = current_valid_actions
        return current_valid_actions

    def is_over(self) -> bool:
        """Checks if the game is over by checking for valid actions."""
        if self._game_over:  # If already marked, return true
            return True
        # If not marked, check if valid actions exist. This call populates cache.
        has_valid_actions = bool(self.valid_actions())
        if not has_valid_actions:
            # If no actions found, mark game as over now
            self._game_over = True
            if not self._game_over_reason:  # Set reason if not already set
                self._game_over_reason = "No valid actions available."
            log.info(
                f"Game determined over by is_over() check: {self._game_over_reason}"
            )
            return True
        # If actions exist, game is not over
        return False

    def get_outcome(self) -> float:
        """Returns terminal outcome: -1.0 for loss, 0.0 for ongoing."""
        return -1.0 if self.is_over() else 0.0

    def game_score(self) -> float:
        """Returns the current accumulated score."""
        return self._game_score

    def get_game_over_reason(self) -> str | None:
        """Returns the reason why the game ended, if it's over."""
        return self._game_over_reason

    def force_game_over(self, reason: str) -> None:
        """Forces the game to end immediately."""
        self._game_over = True
        self._game_over_reason = reason
        self._valid_actions_cache = set()  # Ensure cache is cleared
        log.warning(f"Game forced over: {reason}")

    def copy(self) -> "GameState":
        """Creates a deep copy for simulations (e.g., MCTS)."""
        new_state = GameState.__new__(GameState)
        memo = {id(self): new_state}
        new_state.env_config = self.env_config
        new_state._rng = random.Random()
        new_state._rng.setstate(self._rng.getstate())
        new_state.grid_data = copy.deepcopy(self.grid_data, memo)
        new_state.shapes = [s.copy() if s else None for s in self.shapes]
        new_state._game_score = self._game_score
        new_state._game_over = self._game_over
        new_state._game_over_reason = self._game_over_reason
        new_state.current_step = self.current_step
        new_state._valid_actions_cache = (
            self._valid_actions_cache.copy()
            if self._valid_actions_cache is not None
            else None
        )
        return new_state

    def __str__(self) -> str:
        shape_strs = [str(s.color) if s else "None" for s in self.shapes]
        status = "Over" if self.is_over() else "Ongoing"
        return (
            f"GameState(Step:{self.current_step}, Score:{self.game_score():.1f}, "
            f"Status:{status}, Shapes:[{', '.join(shape_strs)}])"
        )
