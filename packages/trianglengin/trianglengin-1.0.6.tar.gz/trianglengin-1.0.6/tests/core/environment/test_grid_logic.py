# File: tests/core/environment/test_grid_logic.py
import logging

import pytest

from trianglengin.config import EnvConfig
from trianglengin.core.environment.grid import GridData
from trianglengin.core.environment.grid import logic as GridLogic
from trianglengin.core.structs import Shape

# Default color for fixture shapes
DEFAULT_TEST_COLOR = (100, 100, 100)
log = logging.getLogger(__name__)


@pytest.fixture
def default_config() -> EnvConfig:
    """Fixture for default environment configuration."""
    return EnvConfig()


@pytest.fixture
def default_grid(default_config: EnvConfig) -> GridData:
    """Fixture for a default GridData instance."""
    # Ensure the cache is populated for the default config before tests run
    # This will now use the fixed _compute_lines_and_map_v4
    GridData(default_config)
    # Return a fresh instance for the test, which will reuse the cache
    return GridData(default_config)


def occupy_coords(grid_data: GridData, coords: set[tuple[int, int]]):
    """Helper to occupy specific coordinates."""
    for r, c in coords:
        if grid_data.valid(r, c) and not grid_data.is_death(r, c):
            grid_data._occupied_np[r, c] = True
            # Assign a dummy color ID
            grid_data._color_id_np[r, c] = 0


# --- Basic Placement Tests ---
# (Keep existing basic placement tests - they should still pass)


def test_can_place_basic(default_grid: GridData):
    """Test basic placement in empty grid."""
    shape = Shape([(0, 0, False), (0, 1, True)], DEFAULT_TEST_COLOR)  # D, U
    start_r, start_c = -1, -1
    for r in range(default_grid.rows):
        for c in range(default_grid.cols):
            if not default_grid.is_death(r, c) and (r + c) % 2 == 0:  # Find Down cell
                start_r, start_c = r, c
                break
        if start_r != -1:
            break
    if start_r == -1:
        pytest.skip("Could not find a valid starting Down cell.")
    assert GridLogic.can_place(default_grid, shape, start_r, start_c)


def test_can_place_occupied(default_grid: GridData):
    """Test placement fails if target is occupied."""
    shape = Shape([(0, 0, False)], DEFAULT_TEST_COLOR)  # Single Down
    start_r, start_c = -1, -1
    for r in range(default_grid.rows):
        for c in range(default_grid.cols):
            if not default_grid.is_death(r, c) and (r + c) % 2 == 0:  # Find Down cell
                start_r, start_c = r, c
                break
        if start_r != -1:
            break
    if start_r == -1:
        pytest.skip("Could not find a valid starting Down cell.")
    default_grid._occupied_np[start_r, start_c] = True
    assert not GridLogic.can_place(default_grid, shape, start_r, start_c)


def test_can_place_death_zone(default_grid: GridData):
    """Test placement fails if target is in death zone."""
    Shape([(0, 0, False)], DEFAULT_TEST_COLOR)  # Single Down
    death_r, death_c = -1, -1
    for r in range(default_grid.rows):
        for c in range(default_grid.cols):
            if default_grid.is_death(r, c):
                death_r, death_c = r, c
                break
        if death_r != -1:
            break
    if death_r == -1:
        pytest.skip("Could not find a death zone cell.")
    shape_to_use = Shape([(0, 0, (death_r + death_c) % 2 != 0)], DEFAULT_TEST_COLOR)
    assert not GridLogic.can_place(default_grid, shape_to_use, death_r, death_c)


def test_can_place_orientation_mismatch(default_grid: GridData):
    """Test placement fails if shape orientation doesn't match grid."""
    shape = Shape([(0, 0, True)], DEFAULT_TEST_COLOR)  # Needs Up
    start_r, start_c = -1, -1
    for r in range(default_grid.rows):
        for c in range(default_grid.cols):
            if not default_grid.is_death(r, c) and (r + c) % 2 == 0:  # Find Down cell
                start_r, start_c = r, c
                break
        if start_r != -1:
            break
    if start_r == -1:
        pytest.skip("Could not find a valid starting Down cell.")
    assert not GridLogic.can_place(default_grid, shape, start_r, start_c)

    shape_down = Shape([(0, 0, False)], DEFAULT_TEST_COLOR)  # Needs Down
    up_r, up_c = -1, -1
    for r in range(default_grid.rows):
        for c in range(default_grid.cols):
            if not default_grid.is_death(r, c) and (r + c) % 2 != 0:  # Find Up cell
                up_r, up_c = r, c
                break
        if up_r != -1:
            break
    if up_r == -1:
        pytest.skip("Could not find a valid starting Up cell.")
    assert not GridLogic.can_place(default_grid, shape_down, up_r, up_c)


def test_can_place_out_of_bounds(default_grid: GridData):
    """Test placement fails if shape goes out of bounds."""
    shape = Shape([(0, 0, False), (0, 1, True)], DEFAULT_TEST_COLOR)
    assert not GridLogic.can_place(default_grid, shape, 0, default_grid.cols - 1)
    shape_tall = Shape([(0, 0, False), (1, 0, False)], DEFAULT_TEST_COLOR)
    assert not GridLogic.can_place(default_grid, shape_tall, default_grid.rows - 1, 0)


# --- Line Clearing Tests ---


def test_check_and_clear_lines_simple(default_grid: GridData):
    """Test clearing a single horizontal line."""
    target_line = None
    for line in default_grid._lines:
        # Find a reasonably long horizontal line for a good test
        if len(line) > 4 and all(c[0] == line[0][0] for c in line):
            target_line = line
            break
    if not target_line:
        pytest.skip("Could not find a suitable horizontal line.")
    target_line_set = set(target_line)
    occupy_coords(default_grid, target_line_set)
    last_coord = target_line[-1]
    lines_cleared, coords_cleared, cleared_line_sets = GridLogic.check_and_clear_lines(
        default_grid, {last_coord}
    )
    assert lines_cleared == 1, f"Expected 1 line clear, got {lines_cleared}"
    assert coords_cleared == target_line_set, "Cleared coordinates mismatch"
    assert cleared_line_sets == {frozenset(target_line)}, "Cleared line set mismatch"
    for r, c in target_line_set:
        assert not default_grid._occupied_np[r, c], f"Cell ({r},{c}) was not cleared"
        assert default_grid._color_id_np[r, c] == -1, (
            f"Color ID for ({r},{c}) not reset"
        )


def test_check_and_clear_lines_no_clear(default_grid: GridData):
    """Test that no lines are cleared if none are complete."""
    target_line = None
    for line in default_grid._lines:
        # Find a reasonably long line
        if len(line) > 4:
            target_line = line
            break
    if not target_line:
        pytest.skip("Could not find a suitable line.")
    # Occupy all but the last coordinate
    coords_to_occupy = set(target_line[:-1])
    occupy_coords(default_grid, coords_to_occupy)
    # Check clear using the last occupied coordinate
    last_occupied_coord = target_line[-2]  # The one before the empty one
    lines_cleared, coords_cleared, cleared_line_sets = GridLogic.check_and_clear_lines(
        default_grid, {last_occupied_coord}
    )
    assert lines_cleared == 0, f"Expected 0 lines cleared, got {lines_cleared}"
    assert not coords_cleared, "Coords should not be cleared"
    assert not cleared_line_sets, "Cleared line sets should be empty"
    # Verify grid cells remain occupied
    for r, c in coords_to_occupy:
        assert default_grid._occupied_np[r, c], (
            f"Cell ({r},{c}) should still be occupied"
        )


# --- Specific Boundary Line Clearing Scenarios ---

# Define the boundary lines explicitly based on default EnvConfig
# IMPORTANT: Use the natural traversal order expected from line_cache v4
BOUNDARY_LINES = {
    "top_left_diag": (
        (4, 0),
        (3, 0),
        (3, 1),
        (2, 1),
        (2, 2),
        (1, 2),
        (1, 3),
        (0, 3),
        (0, 4),
    ),
    "top_horiz": tuple((0, c) for c in range(3, 12)),
    "top_right_diag": (
        (0, 10),
        (0, 11),
        (1, 11),
        (1, 12),
        (2, 12),
        (2, 13),
        (3, 13),
        (3, 14),
        (4, 14),
    ),
    "bottom_right_diag": (
        (3, 14),
        (4, 14),
        (4, 13),
        (5, 13),
        (5, 12),
        (6, 12),
        (6, 11),
        (7, 11),
        (7, 10),
    ),
    "bottom_horiz": tuple((7, c) for c in range(3, 12)),
    "bottom_left_diag": (
        (3, 0),
        (4, 0),
        (4, 1),
        (5, 1),
        (5, 2),
        (6, 2),
        (6, 3),
        (7, 3),
        (7, 4),
    ),
}


@pytest.mark.parametrize("line_name, line_coords", BOUNDARY_LINES.items())
def test_boundary_line_clears_only_when_full(
    line_name: str, line_coords: tuple[tuple[int, int], ...], default_grid: GridData
):
    """
    Tests that boundary lines clear only when the final middle piece(s) are placed,
    simulating placing pieces from the outside inwards.
    """
    grid_data = default_grid
    grid_data.reset()  # Start with a clean grid for each line test
    n = len(line_coords)
    line_set = set(line_coords)
    line_fs = frozenset(line_coords)
    log.info(f"Testing line '{line_name}' (len={n}): {line_coords}")

    # Verify line exists in cache first (essential prerequisite)
    first_coord = line_coords[0]
    assert first_coord in grid_data._coord_to_lines_map, (
        f"Coord {first_coord} not in map for line '{line_name}'"
    )
    found_mapping = False
    if first_coord in grid_data._coord_to_lines_map:
        for mapped_fs in grid_data._coord_to_lines_map[first_coord]:
            if mapped_fs == line_fs:
                found_mapping = True
                break
    assert found_mapping, (
        f"Line {line_fs} not mapped to {first_coord} for line '{line_name}'"
    )

    # --- Simulate Inward Placement ---
    placed_coords = set()
    final_clear_occurred = False
    for i in range(n // 2 + (n % 2)):  # Iterate inwards (e.g., 0, 1, 2, 3, 4 for n=9)
        coord1 = line_coords[i]
        coord2 = line_coords[n - 1 - i]
        is_last_pair_or_middle = i == (n // 2 + (n % 2) - 1)
        log.debug(
            f"  Step {i}: Considering pair {coord1} / {coord2}. Is last: {is_last_pair_or_middle}"
        )

        # --- Place first cell of the pair ---
        if coord1 not in placed_coords:
            log.debug(f"    Placing {coord1}...")
            grid_data._occupied_np[coord1[0], coord1[1]] = True
            grid_data._color_id_np[coord1[0], coord1[1]] = 0
            placed_coords.add(coord1)
            lines_cleared_1, coords_cleared_1, cleared_sets_1 = (
                GridLogic.check_and_clear_lines(grid_data, {coord1})
            )

            should_clear_now = len(placed_coords) == n
            if should_clear_now:
                log.debug(f"    Checking FINAL clear after placing {coord1}")
                assert lines_cleared_1 == 1, (
                    f"Line '{line_name}' should clear after placing final piece {coord1}, but did not."
                )
                assert coords_cleared_1 == line_set, (
                    f"Cleared coords mismatch for '{line_name}' after final piece {coord1}."
                )
                assert cleared_sets_1 == {line_fs}, (
                    f"Cleared line set mismatch for '{line_name}' after final piece {coord1}."
                )
                final_clear_occurred = True
            else:
                log.debug(f"    Checking NO clear after placing {coord1}")
                assert lines_cleared_1 == 0, (
                    f"Line '{line_name}' cleared prematurely after placing {coord1} (step {i}, total placed: {len(placed_coords)}/{n})"
                )
                assert not coords_cleared_1, (
                    f"Coords cleared prematurely for '{line_name}' after {coord1}"
                )
                assert grid_data._occupied_np[coord1[0], coord1[1]], (
                    f"{coord1} should still be occupied after non-clearing step"
                )

        # --- Place second cell of the pair (if different from first) ---
        if coord1 != coord2 and coord2 not in placed_coords:
            log.debug(f"    Placing {coord2}...")
            grid_data._occupied_np[coord2[0], coord2[1]] = True
            grid_data._color_id_np[coord2[0], coord2[1]] = 0
            placed_coords.add(coord2)
            lines_cleared_2, coords_cleared_2, cleared_sets_2 = (
                GridLogic.check_and_clear_lines(grid_data, {coord2})
            )

            should_clear_now = len(placed_coords) == n
            if should_clear_now:
                log.debug(f"    Checking FINAL clear after placing {coord2}")
                assert lines_cleared_2 == 1, (
                    f"Line '{line_name}' should clear after placing final piece {coord2}, but did not."
                )
                assert coords_cleared_2 == line_set, (
                    f"Cleared coords mismatch for '{line_name}' after final piece {coord2}."
                )
                assert cleared_sets_2 == {line_fs}, (
                    f"Cleared line set mismatch for '{line_name}' after final piece {coord2}."
                )
                final_clear_occurred = True
            else:
                log.debug(f"    Checking NO clear after placing {coord2}")
                assert lines_cleared_2 == 0, (
                    f"Line '{line_name}' cleared prematurely after placing {coord2} (step {i}, total placed: {len(placed_coords)}/{n})"
                )
                assert not coords_cleared_2, (
                    f"Coords cleared prematurely for '{line_name}' after {coord2}"
                )
                assert grid_data._occupied_np[coord2[0], coord2[1]], (
                    f"{coord2} should still be occupied after non-clearing step"
                )

    # --- Final Verification ---
    assert final_clear_occurred, (
        f"The final clear event did not happen for line '{line_name}' after placing all {n} pieces."
    )
    # Check that all cells in the line are indeed clear *after* the loop finishes
    for r_clr, c_clr in line_set:
        assert not grid_data._occupied_np[r_clr, c_clr], (
            f"Cell ({r_clr},{c_clr}) was not cleared for line '{line_name}' after test completion"
        )
