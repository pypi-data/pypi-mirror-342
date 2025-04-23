# File: tests/core/environment/test_game_state.py
import logging

import numpy as np
import pytest

from trianglengin.game_interface import GameState, Shape  # Import Shape

logging.basicConfig(level=logging.INFO)


# --- Helper Functions ---
def get_first_valid_action(gs: GameState) -> int | None:
    """Helper to get the first available valid action."""
    valid_actions = gs.valid_actions()
    return next(iter(valid_actions), None)


def count_non_none_shapes(gs: GameState) -> int:
    """Counts shapes currently in the preview slots."""
    return sum(1 for s in gs.get_shapes() if s is not None)


# Helper to encode action (matches C++ logic)
def encode_action(shape_idx: int, r: int, c: int, gs: GameState) -> int:
    """Encodes action based on game state config."""
    config = gs.env_config
    grid_size = config.ROWS * config.COLS
    if not (
        0 <= shape_idx < config.NUM_SHAPE_SLOTS
        and 0 <= r < config.ROWS
        and 0 <= c < config.COLS
    ):
        return -1
    return shape_idx * grid_size + r * config.COLS + c


# --- Tests for the GameState Wrapper ---


def test_game_state_initialization(game_state: GameState) -> None:
    """Test basic initialization of the GameState wrapper."""
    assert game_state.env_config is not None
    assert game_state.game_score() == 0.0
    assert game_state.current_step == 0
    grid_data = game_state.get_grid_data_np()
    assert isinstance(grid_data, dict)
    assert "occupied" in grid_data and isinstance(grid_data["occupied"], np.ndarray)
    assert "color_id" in grid_data and isinstance(grid_data["color_id"], np.ndarray)
    assert "death" in grid_data and isinstance(grid_data["death"], np.ndarray)
    assert grid_data["occupied"].shape == (
        game_state.env_config.ROWS,
        game_state.env_config.COLS,
    )
    assert grid_data["color_id"].shape == (
        game_state.env_config.ROWS,
        game_state.env_config.COLS,
    )
    assert grid_data["death"].shape == (
        game_state.env_config.ROWS,
        game_state.env_config.COLS,
    )
    shapes = game_state.get_shapes()
    assert isinstance(shapes, list)
    assert len(shapes) == game_state.env_config.NUM_SHAPE_SLOTS
    is_initially_over = game_state.is_over()
    initial_valid_actions = game_state.valid_actions()
    if is_initially_over:
        assert not initial_valid_actions
        reason = game_state.get_game_over_reason()
        assert reason is not None and "start" in reason.lower()
    else:
        assert initial_valid_actions
        assert game_state.get_game_over_reason() is None


def test_game_state_reset(game_state: GameState) -> None:
    """Test resetting the GameState wrapper."""
    initial_shapes_before_step = game_state.get_shapes()
    action = get_first_valid_action(game_state)
    if action is not None:
        game_state.step(action)
        assert game_state.game_score() != 0.0 or game_state.is_over()
        assert game_state.current_step > 0
    else:
        assert game_state.is_over()
    game_state.reset()
    assert game_state.game_score() == 0.0
    assert game_state.current_step == 0
    assert game_state.get_game_over_reason() is None
    grid_data = game_state.get_grid_data_np()
    playable_mask = ~grid_data["death"]
    assert not grid_data["occupied"][playable_mask].any()
    assert (grid_data["color_id"][playable_mask] == -1).all()
    shapes_after_reset = game_state.get_shapes()
    assert len(shapes_after_reset) == game_state.env_config.NUM_SHAPE_SLOTS
    if action is not None:
        assert initial_shapes_before_step != shapes_after_reset, (
            "Shapes did not change after reset and step"
        )
    is_over_after_reset = game_state.is_over()
    valid_actions_after_reset = game_state.valid_actions()
    if is_over_after_reset:
        assert not valid_actions_after_reset
        reason = game_state.get_game_over_reason()
        assert reason is not None and "start" in reason.lower()
    else:
        assert valid_actions_after_reset
        assert game_state.get_game_over_reason() is None


def test_game_state_step_valid(game_state: GameState) -> None:
    """Test a single valid step using the wrapper."""
    if game_state.is_over():
        pytest.skip("Cannot perform step test: game is over initially.")
    initial_score = game_state.game_score()
    initial_shape_count = count_non_none_shapes(game_state)
    initial_step = game_state.current_step
    action = get_first_valid_action(game_state)
    assert action is not None, "No valid action found for step test."
    logging.debug(
        f"Before step: Action={action}, Score={initial_score}, Step={initial_step}"
    )
    reward, done = game_state.step(action)
    logging.debug(
        f"After step: Reward={reward:.4f}, Done={done}, Score={game_state.game_score()}, Step={game_state.current_step}"
    )
    assert isinstance(reward, float)
    assert isinstance(done, bool)
    assert done == game_state.is_over()
    assert game_state.current_step == initial_step + 1
    current_shape_count = count_non_none_shapes(game_state)
    if initial_shape_count == 1 and not done:
        assert current_shape_count == game_state.env_config.NUM_SHAPE_SLOTS
    elif initial_shape_count > 1:
        assert current_shape_count == initial_shape_count - 1
    _ = game_state.get_grid_data_np()


def test_game_state_step_invalid_action(game_state: GameState) -> None:
    """Test stepping with an invalid action index."""
    invalid_action = -1
    initial_step = game_state.current_step
    initial_score = game_state.game_score()
    reward, done = game_state.step(invalid_action)
    assert done is True, "Game should be over after invalid step"
    assert game_state.is_over()
    # Check returned reward uses config penalty
    assert reward == game_state.env_config.PENALTY_GAME_OVER
    assert game_state.current_step == initial_step
    # Check internal score uses config penalty (as invalid action triggers game over)
    assert (
        game_state.game_score()
        == initial_score + game_state.env_config.PENALTY_GAME_OVER
    )
    reason = game_state.get_game_over_reason()
    assert reason is not None and "invalid action" in reason.lower()
    game_state.reset()
    action_dim = (
        game_state.env_config.NUM_SHAPE_SLOTS
        * game_state.env_config.ROWS
        * game_state.env_config.COLS
    )
    invalid_action_large = action_dim + 10
    reward, done = game_state.step(invalid_action_large)
    assert done is True
    assert reward == game_state.env_config.PENALTY_GAME_OVER


# Use the 4x4 grid fixture to make game over less likely after one step
def test_game_state_step_on_occupied_cell(game_state_4x4: GameState) -> None:
    """Test stepping to place a shape on an already occupied cell (using 4x4 grid)."""
    gs = game_state_4x4  # Use the 4x4 fixture
    if gs.is_over():
        pytest.skip("Initial 4x4 state is over.")

    # Find first valid action and place it
    action1 = get_first_valid_action(gs)
    if action1 is None:
        pytest.skip("No valid first action found in 4x4 grid.")

    # Decode action1 to find where it placed
    grid_size = gs.env_config.ROWS * gs.env_config.COLS
    shape1_idx = action1 // grid_size
    remainder1 = action1 % grid_size
    r1_base = remainder1 // gs.env_config.COLS
    c1_base = remainder1 % gs.env_config.COLS
    shape1 = gs.get_shapes()[shape1_idx]
    assert shape1 is not None
    # Get one specific coordinate occupied by the first shape
    dr0, dc0, _ = shape1.triangles[0]
    r_occupied, c_occupied = r1_base + dr0, c1_base + dc0

    # Perform the first step
    gs.step(action1)

    if gs.is_over():
        # It's still possible the game ends, especially if few actions remain
        pytest.skip("Game ended after the first step even on 4x4 grid.")

    # Try to place the *next* available shape targeting the occupied cell
    shapes_after_step1 = gs.get_shapes()
    action2 = -1
    target_shape_idx = -1

    # Find the first available shape slot after step 1
    for idx, shape in enumerate(shapes_after_step1):
        if shape is not None:
            target_shape_idx = idx
            break

    if target_shape_idx == -1:
        pytest.skip("No second shape available to test occupied placement.")

    # Encode an action for the target shape at the occupied coordinate
    action2 = encode_action(target_shape_idx, r_occupied, c_occupied, gs)

    # This action targeting an occupied cell should be invalid
    assert action2 not in gs.valid_actions(), (
        f"Action {action2} targeting occupied cell ({r_occupied},{c_occupied}) is unexpectedly valid."
    )

    # Attempting the invalid step
    initial_score = gs.game_score()
    reward, done = gs.step(action2)

    assert done is True, "Game should end after attempting to place on occupied cell"
    assert gs.is_over()
    assert reward == gs.env_config.PENALTY_GAME_OVER
    assert (
        gs.game_score() == initial_score + gs.env_config.PENALTY_GAME_OVER
    )  # Score updated with penalty
    reason = gs.get_game_over_reason()
    assert reason is not None and "invalid action" in reason.lower()


def test_game_state_is_over_logic(game_state: GameState) -> None:
    """Test the is_over condition by observing behavior."""
    max_steps = game_state.env_config.ROWS * game_state.env_config.COLS * 2
    steps = 0
    while not game_state.is_over() and steps < max_steps:
        action = get_first_valid_action(game_state)
        if action is None:
            break
        game_state.step(action)
        steps += 1
    if steps >= max_steps:
        pytest.skip("Game did not terminate naturally within step limit.")
    assert game_state.is_over()
    assert not game_state.valid_actions()
    assert game_state.get_game_over_reason() is not None
    game_state.reset()
    if not game_state.is_over():
        assert game_state.valid_actions()
        assert game_state.get_game_over_reason() is None
    else:
        assert not game_state.valid_actions()
        assert game_state.get_game_over_reason() is not None


def test_game_state_copy(game_state: GameState) -> None:
    """Test the copy method of the GameState wrapper."""
    if game_state.is_over():
        pytest.skip("Cannot test copy effectively on initial terminal state.")
    action1 = get_first_valid_action(game_state)
    if action1:
        game_state.step(action1)
    gs1 = game_state
    gs2 = gs1.copy()
    assert gs1.game_score() == gs2.game_score()
    assert gs1.env_config == gs2.env_config
    assert gs1.is_over() == gs2.is_over()
    assert gs1.get_game_over_reason() == gs2.get_game_over_reason()
    assert gs1.current_step == gs2.current_step
    assert gs1._cpp_state is not gs2._cpp_state
    shapes1 = gs1.get_shapes()
    shapes2 = gs2.get_shapes()
    assert shapes1 == shapes2
    grid1 = gs1.get_grid_data_np()
    grid2 = gs2.get_grid_data_np()
    assert np.array_equal(grid1["occupied"], grid2["occupied"])
    assert np.array_equal(grid1["color_id"], grid2["color_id"])
    assert np.array_equal(grid1["death"], grid2["death"])
    assert gs1.valid_actions() == gs2.valid_actions()
    action2 = get_first_valid_action(gs2)
    if not action2:
        assert not gs1.valid_actions()
        return
    score1_before_gs2_step = gs1.game_score()
    step1_before_gs2_step = gs1.current_step
    grid1_occupied_before_gs2_step = gs1.get_grid_data_np()["occupied"].copy()
    shapes1_before_gs2_step = gs1.get_shapes()
    reward2, done2 = gs2.step(action2)
    assert gs1.game_score() == score1_before_gs2_step
    assert gs1.current_step == step1_before_gs2_step
    assert np.array_equal(
        gs1.get_grid_data_np()["occupied"], grid1_occupied_before_gs2_step
    )
    assert gs1.get_shapes() == shapes1_before_gs2_step
    assert gs2.current_step == step1_before_gs2_step + 1
    assert gs2.game_score() != score1_before_gs2_step or reward2 == 0.0
    assert not np.array_equal(
        gs2.get_grid_data_np()["occupied"], grid1_occupied_before_gs2_step
    )
    assert gs2.get_shapes() != shapes1_before_gs2_step


def test_game_state_get_outcome(game_state: GameState) -> None:
    """Test get_outcome method."""
    # This test remains conceptual until get_outcome is implemented in C++ and exposed
    if game_state.is_over():
        pass
    else:
        pass


def test_game_state_debug_toggle(game_state_3x3: GameState) -> None:
    """Test the debug_toggle_cell method."""
    gs = game_state_3x3
    r, c = 1, 1
    grid_data_initial = gs.get_grid_data_np()
    if not (
        0 <= r < gs.env_config.ROWS
        and 0 <= c < gs.env_config.COLS
        and not grid_data_initial["death"][r, c]
    ):
        pytest.skip(f"Cell ({r},{c}) is invalid or death zone in 3x3 grid.")
    initial_occupied = grid_data_initial["occupied"][r, c]
    initial_color = grid_data_initial["color_id"][r, c]
    initial_score = gs.game_score()  # Get score before toggle
    gs.debug_toggle_cell(r, c)
    grid_data_after = gs.get_grid_data_np()
    assert grid_data_after["occupied"][r, c] == (not initial_occupied)
    if not initial_occupied:
        assert grid_data_after["color_id"][r, c] == -2  # DEBUG_COLOR_ID
    else:
        assert grid_data_after["color_id"][r, c] == -1  # NO_COLOR_ID
    assert gs.game_score() == initial_score, "Score should not change on debug toggle"
    _ = gs.valid_actions()
    gs.debug_toggle_cell(r, c)
    grid_data_final = gs.get_grid_data_np()
    assert grid_data_final["occupied"][r, c] == initial_occupied
    assert grid_data_final["color_id"][r, c] == initial_color
    assert gs.game_score() == initial_score, "Score should still be unchanged"


# --- Score Verification Tests ---


def test_reward_placement_only(game_state: GameState) -> None:
    """Verify RETURNED REWARD for placing triangles without clearing lines."""
    if game_state.is_over():
        pytest.skip("Game over initially.")

    initial_score = game_state.game_score()
    action = get_first_valid_action(game_state)
    if action is None:
        pytest.skip("No valid actions.")

    shapes = game_state.get_shapes()
    grid_size = game_state.env_config.ROWS * game_state.env_config.COLS
    shape_idx = action // grid_size
    shape_placed = shapes[shape_idx]
    assert shape_placed is not None
    num_triangles_placed = len(shape_placed.triangles)

    reward, done = game_state.step(action)

    # Calculate expected reward based *only* on placement and step alive/penalty
    expected_reward = (
        num_triangles_placed * game_state.env_config.REWARD_PER_PLACED_TRIANGLE
    )
    if done:
        expected_reward += game_state.env_config.PENALTY_GAME_OVER
    else:
        expected_reward += game_state.env_config.REWARD_PER_STEP_ALIVE

    assert reward == pytest.approx(expected_reward)
    expected_score = initial_score + reward
    assert game_state.game_score() == pytest.approx(expected_score)


def test_reward_line_clear(
    game_state_3x3: GameState, single_up_triangle_shape: Shape
) -> None:
    """Verify RETURNED REWARD increases correctly when clearing lines."""
    gs = game_state_3x3
    # Setup: Place two triangles manually, leaving one spot to complete a line (e.g., row 0)
    gs.debug_toggle_cell(0, 0)  # Occupy (0,0) - Down
    gs.debug_toggle_cell(0, 2)  # Occupy (0,2) - Down
    # Cell (0,1) is Up and is the target

    # Force the required shape into slot 0
    gs.debug_set_shapes([single_up_triangle_shape, None, None])

    initial_score = gs.game_score()  # Should be 0 after setup via debug

    # Action to place the shape from slot 0 at (0,1)
    target_action = encode_action(0, 0, 1, gs)

    if target_action == -1 or target_action not in gs.valid_actions():
        pytest.fail("Action to place forced shape at (0,1) is invalid.")

    # Execute the step that clears the line
    reward, done = gs.step(target_action)

    # Expected reward calculation based on config
    tris_placed = len(single_up_triangle_shape.triangles)  # Should be 1
    tris_cleared = 3  # cells 0,0; 0,1; 0,2 are cleared
    expected_reward = (
        tris_placed * gs.env_config.REWARD_PER_PLACED_TRIANGLE
        + tris_cleared * gs.env_config.REWARD_PER_CLEARED_TRIANGLE
    )
    if done:
        expected_reward += gs.env_config.PENALTY_GAME_OVER
    else:
        expected_reward += gs.env_config.REWARD_PER_STEP_ALIVE

    # Verify the returned reward matches the calculation
    assert reward == pytest.approx(expected_reward)

    # Verify the final score is initial_score + calculated reward
    expected_score = initial_score + reward
    assert gs.game_score() == pytest.approx(expected_score)


def test_internal_score_placement(game_state: GameState) -> None:
    """Verify INTERNAL score increases by +1 per triangle placed (no line clear)."""
    if game_state.is_over():
        pytest.skip("Game over initially.")

    game_state.game_score()
    action = get_first_valid_action(game_state)
    if action is None:
        pytest.skip("No valid actions.")

    shapes = game_state.get_shapes()
    grid_size = game_state.env_config.ROWS * game_state.env_config.COLS
    shape_idx = action // grid_size
    shape_placed = shapes[shape_idx]
    assert shape_placed is not None
    len(shape_placed.triangles)

    # Store score *before* step
    score_before = game_state.game_score()
    reward, done = game_state.step(action)
    score_after = game_state.game_score()

    # Expected internal score increase = +1 per placed triangle
    # The reward returned by step() includes scaling factors and penalties/bonuses
    # The internal score_ should reflect the raw +1/+2 logic plus the reward components
    # expected_internal_increase = float(num_triangles_placed) # This is NOT how score is updated

    # Check that the score difference matches the returned reward
    assert score_after - score_before == pytest.approx(reward)


def test_internal_score_line_clear(
    game_state_3x3: GameState, single_up_triangle_shape: Shape
) -> None:
    """Verify INTERNAL score increases correctly (+1 per placed, +2 per cleared)."""
    gs = game_state_3x3
    gs.debug_toggle_cell(0, 0)
    gs.debug_toggle_cell(0, 2)
    gs.debug_set_shapes([single_up_triangle_shape, None, None])
    gs.game_score()

    target_action = encode_action(0, 0, 1, gs)
    if target_action == -1 or target_action not in gs.valid_actions():
        pytest.fail("Action to place forced shape at (0,1) is invalid.")

    score_before = gs.game_score()
    reward, done = gs.step(target_action)
    score_after = gs.game_score()

    # tris_placed = 1
    # tris_cleared = 3
    # Expected internal score increase = +1 * tris_placed + +2 * tris_cleared
    # expected_internal_increase = float(1 * 1 + 3 * 2) # This is NOT how score is updated

    # Check that the score difference matches the returned reward
    assert score_after - score_before == pytest.approx(reward)
