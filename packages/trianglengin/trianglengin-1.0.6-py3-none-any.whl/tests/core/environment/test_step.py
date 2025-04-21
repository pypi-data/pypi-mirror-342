# File: tests/core/environment/test_step.py

import pytest

# Import mocker fixture from pytest-mock
from pytest_mock import MockerFixture

# Import directly from the library being tested
from trianglengin.config import EnvConfig
from trianglengin.core.environment import GameState
from trianglengin.core.environment.grid import GridData
from trianglengin.core.environment.grid import logic as GridLogic
from trianglengin.core.environment.logic.step import calculate_reward, execute_placement
from trianglengin.core.structs import Shape

# Use fixtures from the local conftest.py
# Fixtures are implicitly injected by pytest


# Removed deprecated occupy_line function


def occupy_coords(grid_data: GridData, coords: set[tuple[int, int]]):
    """Helper to occupy specific coordinates."""
    for r, c in coords:
        if grid_data.valid(r, c) and not grid_data.is_death(r, c):
            grid_data._occupied_np[r, c] = True


# --- New Reward Calculation Tests (v3) ---


def test_calculate_reward_v3_placement_only(
    simple_shape: Shape, default_env_config: EnvConfig
):
    """Test reward: only placement, game not over."""
    placed_count = len(simple_shape.triangles)
    unique_coords_cleared: set[tuple[int, int]] = set()
    is_game_over = False
    reward = calculate_reward(
        placed_count, len(unique_coords_cleared), is_game_over, default_env_config
    )
    expected_reward = (
        placed_count * default_env_config.REWARD_PER_PLACED_TRIANGLE
        + default_env_config.REWARD_PER_STEP_ALIVE
    )
    assert reward == pytest.approx(expected_reward)


def test_calculate_reward_v3_single_line_clear(
    simple_shape: Shape, default_env_config: EnvConfig
):
    """Test reward: placement + line clear, game not over."""
    placed_count = len(simple_shape.triangles)
    unique_coords_cleared: set[tuple[int, int]] = {(0, i) for i in range(9)}
    is_game_over = False
    reward = calculate_reward(
        placed_count, len(unique_coords_cleared), is_game_over, default_env_config
    )
    expected_reward = (
        placed_count * default_env_config.REWARD_PER_PLACED_TRIANGLE
        + len(unique_coords_cleared) * default_env_config.REWARD_PER_CLEARED_TRIANGLE
        + default_env_config.REWARD_PER_STEP_ALIVE
    )
    assert reward == pytest.approx(expected_reward)


def test_calculate_reward_v3_multi_line_clear(
    simple_shape: Shape, default_env_config: EnvConfig
):
    """Test reward: placement + multi-line clear (overlapping coords), game not over."""
    placed_count = len(simple_shape.triangles)
    line1_coords = {(0, i) for i in range(9)}
    line2_coords = {(i, 0) for i in range(5)}
    unique_coords_cleared = line1_coords.union(line2_coords)
    is_game_over = False
    reward = calculate_reward(
        placed_count, len(unique_coords_cleared), is_game_over, default_env_config
    )
    expected_reward = (
        placed_count * default_env_config.REWARD_PER_PLACED_TRIANGLE
        + len(unique_coords_cleared) * default_env_config.REWARD_PER_CLEARED_TRIANGLE
        + default_env_config.REWARD_PER_STEP_ALIVE
    )
    assert reward == pytest.approx(expected_reward)


def test_calculate_reward_v3_game_over(
    simple_shape: Shape, default_env_config: EnvConfig
):
    """Test reward: placement, no line clear, game IS over."""
    placed_count = len(simple_shape.triangles)
    unique_coords_cleared: set[tuple[int, int]] = set()
    is_game_over = True
    reward = calculate_reward(
        placed_count, len(unique_coords_cleared), is_game_over, default_env_config
    )
    expected_reward = (
        placed_count * default_env_config.REWARD_PER_PLACED_TRIANGLE
        + default_env_config.PENALTY_GAME_OVER
    )
    assert reward == pytest.approx(expected_reward)


def test_calculate_reward_v3_game_over_with_clear(
    simple_shape: Shape, default_env_config: EnvConfig
):
    """Test reward: placement + line clear, game IS over."""
    placed_count = len(simple_shape.triangles)
    unique_coords_cleared: set[tuple[int, int]] = {(0, i) for i in range(9)}
    is_game_over = True
    reward = calculate_reward(
        placed_count, len(unique_coords_cleared), is_game_over, default_env_config
    )
    expected_reward = (
        placed_count * default_env_config.REWARD_PER_PLACED_TRIANGLE
        + len(unique_coords_cleared) * default_env_config.REWARD_PER_CLEARED_TRIANGLE
        + default_env_config.PENALTY_GAME_OVER
    )
    assert reward == pytest.approx(expected_reward)


# --- Test execute_placement ---


def test_execute_placement_simple_no_refill_v3(
    game_state: GameState,
):
    """Test placing a shape without clearing lines, verify stats."""
    gs = game_state
    config = gs.env_config
    shape_idx = -1
    shape_to_place = None
    for i, s in enumerate(gs.shapes):
        if s:
            shape_idx = i
            shape_to_place = s
            break
    if shape_idx == -1 or not shape_to_place:
        pytest.skip("Requires at least one initial shape in game state")

    original_other_shapes = [
        s.copy() if s else None for j, s in enumerate(gs.shapes) if j != shape_idx
    ]
    placed_count_expected = len(shape_to_place.triangles)

    r, c = -1, -1
    found_spot = False
    for r_try in range(config.ROWS):
        start_c, end_c = config.PLAYABLE_RANGE_PER_ROW[r_try]
        for c_try in range(start_c, end_c):
            if GridLogic.can_place(gs.grid_data, shape_to_place, r_try, c_try):
                r, c = r_try, c_try
                found_spot = True
                break
        if found_spot:
            break
    if not found_spot:
        pytest.skip(f"Could not find valid placement for shape {shape_idx}")

    gs.game_score()
    cleared_count_ret, placed_count_ret = execute_placement(gs, shape_idx, r, c)

    assert placed_count_ret == placed_count_expected
    assert cleared_count_ret == 0
    # Score calculation is handled by GameState.step, not tested here directly
    # expected_score_increase = placed_count_expected + cleared_count_ret * 2
    # assert gs.game_score() == initial_score + expected_score_increase
    for dr, dc, _ in shape_to_place.triangles:
        assert gs.grid_data._occupied_np[r + dr, c + dc]
    assert gs.shapes[shape_idx] is None
    current_other_shapes = [s for j, s in enumerate(gs.shapes) if j != shape_idx]
    assert current_other_shapes == original_other_shapes


def test_execute_placement_clear_line_no_refill_v3(
    game_state: GameState,
):
    """Test placing a shape that clears a line, verify stats."""
    gs = game_state

    shape_idx = -1
    shape_single = None
    for i, s in enumerate(gs.shapes):
        if s and len(s.triangles) == 1:
            shape_idx = i
            shape_single = s
            break
    if shape_idx == -1 or not shape_single:
        gs.reset()
        for i, s in enumerate(gs.shapes):
            if s and len(s.triangles) == 1:
                shape_idx = i
                shape_single = s
                break
        if shape_idx == -1 or not shape_single:
            pytest.skip("Requires a single-triangle shape")

    placed_count_expected = len(shape_single.triangles)
    original_other_shapes = [
        s.copy() if s else None for j, s in enumerate(gs.shapes) if j != shape_idx
    ]

    # Find any precomputed maximal line
    target_line_coords_tuple = None
    if not gs.grid_data._lines:
        pytest.skip("No precomputed lines found.")
    # Just pick the first one for the test
    target_line_coords_tuple = gs.grid_data._lines[0]
    target_line_coords_fs = frozenset(target_line_coords_tuple)

    r, c = -1, -1
    placement_coord = None
    for r_place, c_place in target_line_coords_tuple:
        if GridLogic.can_place(gs.grid_data, shape_single, r_place, c_place):
            r, c = r_place, c_place
            placement_coord = (r, c)
            break
    if placement_coord is None:
        pytest.skip(
            f"Could not find valid placement for shape {shape_idx} on target line"
        )

    line_coords_to_occupy = set(target_line_coords_fs) - {
        placement_coord
    }  # Convert to set
    occupy_coords(gs.grid_data, line_coords_to_occupy)
    gs.game_score()

    cleared_count_ret, placed_count_ret = execute_placement(gs, shape_idx, r, c)

    assert placed_count_ret == placed_count_expected
    assert cleared_count_ret == len(target_line_coords_fs)
    # Score calculation is handled by GameState.step, not tested here directly
    # expected_score_increase = placed_count_expected + cleared_count_ret * 2
    # assert gs.game_score() == initial_score + expected_score_increase
    for row, col in target_line_coords_fs:
        assert not gs.grid_data._occupied_np[row, col]
    assert gs.shapes[shape_idx] is None
    current_other_shapes = [s for j, s in enumerate(gs.shapes) if j != shape_idx]
    assert current_other_shapes == original_other_shapes


def test_execute_placement_batch_refill_v3(
    game_state: GameState, mocker: MockerFixture
):
    """Test execute_placement when placing the last shape - refill handled by caller."""
    gs = game_state
    config = gs.env_config
    if config.NUM_SHAPE_SLOTS != 3:
        pytest.skip("Test requires 3 shape slots")
    if len(gs.shapes) != 3 or any(s is None for s in gs.shapes):
        gs.reset()
        if len(gs.shapes) != 3 or any(s is None for s in gs.shapes):
            pytest.skip("Could not ensure 3 initial shapes")

    placements = []
    temp_gs = gs.copy()
    placed_indices = set()
    for i in range(config.NUM_SHAPE_SLOTS):
        shape_to_place = temp_gs.shapes[i]
        if not shape_to_place:
            continue
        found_spot = False
        for r_try in range(config.ROWS):
            start_c, end_c = config.PLAYABLE_RANGE_PER_ROW[r_try]
            for c_try in range(start_c, end_c):
                if GridLogic.can_place(temp_gs.grid_data, shape_to_place, r_try, c_try):
                    placements.append(
                        {
                            "idx": i,
                            "r": r_try,
                            "c": c_try,
                            "count": len(shape_to_place.triangles),
                        }
                    )
                    for dr, dc, _ in shape_to_place.triangles:
                        if temp_gs.grid_data.valid(r_try + dr, c_try + dc):
                            temp_gs.grid_data._occupied_np[r_try + dr, c_try + dc] = (
                                True
                            )
                    temp_gs.shapes[i] = None
                    placed_indices.add(i)
                    found_spot = True
                    break
            if found_spot:
                break
        if not found_spot:
            pytest.skip(f"Could not find sequential placement for shape {i}")
    if len(placements) != config.NUM_SHAPE_SLOTS:
        pytest.skip("Could not find valid sequential placements for all 3 shapes")

    p1 = placements[0]
    _, _ = execute_placement(gs, p1["idx"], p1["r"], p1["c"])
    assert gs.shapes[p1["idx"]] is None
    assert gs.shapes[placements[1]["idx"]] is not None
    assert gs.shapes[placements[2]["idx"]] is not None

    p2 = placements[1]
    _, _ = execute_placement(gs, p2["idx"], p2["r"], p2["c"])
    assert gs.shapes[p1["idx"]] is None
    assert gs.shapes[p2["idx"]] is None
    assert gs.shapes[placements[2]["idx"]] is not None

    mock_clear = mocker.patch(
        "trianglengin.core.environment.grid.logic.check_and_clear_lines",
        return_value=(0, set(), set()),
    )

    p3 = placements[2]
    cleared3, placed3 = execute_placement(gs, p3["idx"], p3["r"], p3["c"])
    assert cleared3 == 0
    assert placed3 == p3["count"]
    mock_clear.assert_called_once()
    assert all(s is None for s in gs.shapes)


def test_execute_placement_game_over_v3(game_state: GameState, mocker: MockerFixture):
    """Test execute_placement when placement leads to game over state - reward handled by caller."""
    config = game_state.env_config
    playable_mask = ~game_state.grid_data._death_np
    game_state.grid_data._occupied_np[playable_mask] = True

    empty_r, empty_c = -1, -1
    shape_to_place = None
    shape_idx = -1
    found_spot = False
    for idx, s in enumerate(game_state.shapes):
        if not s:
            continue
        for r_try in range(config.ROWS):
            start_c, end_c = config.PLAYABLE_RANGE_PER_ROW[r_try]
            for c_try in range(start_c, end_c):
                if not game_state.grid_data._death_np[r_try, c_try]:
                    original_state = game_state.grid_data._occupied_np[r_try, c_try]
                    game_state.grid_data._occupied_np[r_try, c_try] = False
                    if GridLogic.can_place(game_state.grid_data, s, r_try, c_try):
                        shape_to_place = s
                        shape_idx = idx
                        empty_r, empty_c = r_try, c_try
                        found_spot = True
                        break
                    else:
                        game_state.grid_data._occupied_np[r_try, c_try] = original_state
            if found_spot:
                break
        if found_spot:
            break
    if not found_spot:
        pytest.skip("Could not find suitable shape and empty spot")

    game_state.grid_data._occupied_np[playable_mask] = True
    game_state.grid_data._occupied_np[empty_r, empty_c] = False

    placed_count_expected = 0
    if shape_to_place:  # Check if shape_to_place is not None
        placed_count_expected = len(shape_to_place.triangles)

    mock_clear = mocker.patch(
        "trianglengin.core.environment.grid.logic.check_and_clear_lines",
        return_value=(0, set(), set()),
    )

    cleared_count_ret, placed_count_ret = execute_placement(
        game_state, shape_idx, empty_r, empty_c
    )

    assert placed_count_ret == placed_count_expected
    assert cleared_count_ret == 0
    mock_clear.assert_called_once()
    assert game_state.grid_data._occupied_np[playable_mask].all()
    assert game_state.shapes[shape_idx] is None
