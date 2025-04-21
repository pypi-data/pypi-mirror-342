# File: trianglengin/core/environment/grid/logic.py
import logging
from typing import TYPE_CHECKING, Final

from trianglengin.core.structs.constants import NO_COLOR_ID

if TYPE_CHECKING:
    from trianglengin.core.environment.grid.grid_data import GridData
    from trianglengin.core.structs.shape import Shape


log = logging.getLogger(__name__)

# Minimum length a line must have to be eligible for clearing
MIN_LINE_LENGTH_TO_CLEAR: Final = 2


def can_place(grid_data: "GridData", shape: "Shape", r: int, c: int) -> bool:
    """
    Checks if a shape can be placed at the specified (r, c) top-left position.

    Args:
        grid_data: The current grid state.
        shape: The shape to place.
        r: Target row for the shape's origin (relative 0,0).
        c: Target column for the shape's origin (relative 0,0).

    Returns:
        True if the placement is valid, False otherwise.
    """
    if not shape or not shape.triangles:
        log.warning("Attempted to check placement for an empty or invalid shape.")
        return False

    for dr, dc, is_up_shape in shape.triangles:
        place_r, place_c = r + dr, c + dc

        # 1. Check bounds
        if not grid_data.valid(place_r, place_c):
            return False

        # 2. Check death zone
        if grid_data.is_death(place_r, place_c):
            return False

        # 3. Check occupancy
        if grid_data.is_occupied(place_r, place_c):
            return False

        # 4. Check orientation match
        is_up_grid = (place_r + place_c) % 2 != 0
        if is_up_shape != is_up_grid:
            return False

    return True


def check_and_clear_lines(
    grid_data: "GridData", newly_occupied_coords: set[tuple[int, int]]
) -> tuple[int, set[tuple[int, int]], set[frozenset[tuple[int, int]]]]:
    """
    Checks for completed lines involving the newly occupied coordinates and clears them.

    Uses the precomputed coordinate-to-lines map for efficiency. Only checks
    maximal lines that contain at least one of the newly occupied cells.

    Args:
        grid_data: The grid data object (will be modified if lines are cleared).
        newly_occupied_coords: A set of (r, c) tuples that were just filled.

    Returns:
        A tuple containing:
        - lines_cleared_count (int): The number of maximal lines cleared.
        - unique_coords_cleared_set (set[tuple[int, int]]): A set of unique (r, c)
          coordinates of all triangles that were cleared.
        - set_of_cleared_lines_coord_sets (set[frozenset[tuple[int, int]]]): A set
          containing the frozensets of coordinates for each cleared maximal line.
    """
    if not newly_occupied_coords:
        return 0, set(), set()

    # Find all candidate maximal lines that include any of the new coordinates
    candidate_lines_fs: set[frozenset[tuple[int, int]]] = set()
    for r_new, c_new in newly_occupied_coords:
        # Check if the coordinate exists in the precomputed map
        if (r_new, c_new) in grid_data._coord_to_lines_map:
            candidate_lines_fs.update(grid_data._coord_to_lines_map[(r_new, c_new)])

    if not candidate_lines_fs:
        return 0, set(), set()

    cleared_lines_fs: set[frozenset[tuple[int, int]]] = set()
    unique_coords_cleared: set[tuple[int, int]] = set()

    # Check each candidate line for completion
    for line_fs in candidate_lines_fs:
        line_coords = tuple(line_fs)  # Convert back for iteration/indexing if needed

        # --- Added Check: Ensure line has minimum length ---
        if len(line_coords) < MIN_LINE_LENGTH_TO_CLEAR:
            continue
        # --- End Added Check ---

        # Check if ALL coordinates in this line are now occupied
        is_line_complete = True
        for r_line, c_line in line_coords:
            # Use is_occupied which correctly handles death zones
            if not grid_data.is_occupied(r_line, c_line):
                is_line_complete = False
                break  # No need to check further coords in this line

        if is_line_complete:
            cleared_lines_fs.add(line_fs)
            unique_coords_cleared.update(line_coords)

    # If any lines were completed, clear the cells
    if unique_coords_cleared:
        log.debug(
            f"Clearing {len(cleared_lines_fs)} lines involving {len(unique_coords_cleared)} unique cells."
        )
        for r_clear, c_clear in unique_coords_cleared:
            # Check bounds just in case, though precomputed lines should be valid
            if grid_data.valid(r_clear, c_clear):
                grid_data._occupied_np[r_clear, c_clear] = False
                grid_data._color_id_np[r_clear, c_clear] = NO_COLOR_ID
            else:
                log.warning(
                    f"Attempted to clear out-of-bounds coordinate ({r_clear}, {c_clear}) from line."
                )

    return len(cleared_lines_fs), unique_coords_cleared, cleared_lines_fs
