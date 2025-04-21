
# Environment Grid Submodule (`trianglengin.core.environment.grid`)

## Purpose and Architecture

This submodule manages the game's grid structure and related logic. It defines the triangular cells, their properties, relationships, and operations like placement validation and line clearing.

-   **Cell Representation:** The actual state (occupied, death, color) is managed within `GridData` using NumPy arrays. The orientation (`is_up`) is implicit from the coordinates `(r + c) % 2 != 0`.
-   **Grid Data Structure:** The [`GridData`](grid_data.py) class holds the grid state using efficient `numpy` arrays (`_occupied_np`, `_death_np`, `_color_id_np`). It initializes death zones based on the `PLAYABLE_RANGE_PER_ROW` setting in `EnvConfig`. It retrieves precomputed potential lines and a coordinate-to-line mapping from the [`line_cache`](line_cache.py) module during initialization.
-   **Line Cache:** The [`line_cache`](line_cache.py) module precomputes **maximal** continuous lines (as coordinate tuples) of playable cells in the three directions (Horizontal, Diagonal TL-BR, Diagonal BL-TR). A maximal line is the longest possible continuous segment of playable cells in a given direction. It also creates a map from coordinates to the maximal lines they belong to (`_coord_to_lines_map`). This computation is done once per grid configuration (based on dimensions, playable ranges) and cached for efficiency. The `is_live` check within this module uses `PLAYABLE_RANGE_PER_ROW`.
-   **Grid Logic:** The [`logic.py`](logic.py) module (exposed as `GridLogic`) contains functions operating on `GridData`. This includes:
    -   Checking if a shape can be placed (`can_place`), including matching triangle orientations and checking against death zones.
    -   Checking for and clearing completed lines (`check_and_clear_lines`) using the precomputed coordinate map for efficiency. It checks if *all* cells within a candidate maximal line (with a minimum length, typically 2) are occupied before marking it for clearing.
-   **Grid Features:** Note: Any functions related to calculating scalar metrics (heights, holes, bumpiness) are expected to be handled outside this core engine library, likely in a separate features module or project.

## Exposed Interfaces

-   **Classes:**
    -   `GridData`: Holds the grid state using NumPy arrays and cached line information.
        -   `__init__(config: EnvConfig)`
        -   `reset()`
        -   `valid(r: int, c: int) -> bool`
        -   `is_death(r: int, c: int) -> bool`
        -   `is_occupied(r: int, c: int) -> bool`
        -   `get_color_id(r: int, c: int) -> Optional[int]`
        -   `__deepcopy__(memo)`
-   **Modules/Namespaces:**
    -   `logic` (often imported as `GridLogic`):
        -   `can_place(grid_data: GridData, shape: Shape, r: int, c: int) -> bool`
        -   `check_and_clear_lines(grid_data: GridData, newly_occupied_coords: Set[Tuple[int, int]]) -> Tuple[int, Set[Tuple[int, int]], Set[frozenset[Tuple[int, int]]]]` **(Returns: lines_cleared_count, unique_coords_cleared_set, set_of_cleared_lines_coord_sets)**
    -   `line_cache`:
        -   `get_precomputed_lines_and_map(config: EnvConfig) -> Tuple[List[Line], CoordMap]`

## Dependencies

-   **[`trianglengin.config`](../../../config/README.md)**:
    -   `EnvConfig`: Used by `GridData` initialization and logic functions (specifically `PLAYABLE_RANGE_PER_ROW`).
-   **[`trianglengin.structs`](../../../structs/README.md)**:
    -   Uses `Shape`, `NO_COLOR_ID`.
-   **`numpy`**:
    -   Used extensively in `GridData`.
-   **Standard Libraries:** `typing`, `logging`, `numpy`, `copy`.

---

**Note:** Please keep this README updated when changing the grid structure, cell properties, placement rules, or line clearing logic. Accurate documentation is crucial for maintainability.