# trianglengin/core/environment/logic/actions.py
"""
Logic for determining valid actions in the game state.
"""

import logging
from typing import TYPE_CHECKING  # Changed List to Set

from trianglengin.core.environment.action_codec import ActionType, encode_action
from trianglengin.core.environment.grid import logic as GridLogic

if TYPE_CHECKING:
    from trianglengin.core.environment.game_state import GameState


logger = logging.getLogger(__name__)


def get_valid_actions(state: "GameState") -> set[ActionType]:  # Return Set
    """
    Calculates and returns a set of all valid encoded action indices
    for the current game state.
    """
    valid_actions: set[ActionType] = set()  # Use set directly
    for shape_idx, shape in enumerate(state.shapes):
        if shape is None:
            continue

        # Iterate through potential placement locations (r, c)
        # Optimization: Could potentially limit r, c range based on shape bbox
        for r in range(state.env_config.ROWS):
            for c in range(state.env_config.COLS):
                # Check if placement is valid using GridLogic
                if GridLogic.can_place(state.grid_data, shape, r, c):
                    action_index = encode_action(shape_idx, r, c, state.env_config)
                    valid_actions.add(action_index)  # Add to set

    return valid_actions
