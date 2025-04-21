

# UI Visualization Core Submodule (`trianglengin.ui.visualization.core`)

**Requires:** `pygame`

## Purpose and Architecture

This submodule contains the central classes and foundational elements for the **interactive** visualization system within the `trianglengin.ui` package. It orchestrates rendering for play/debug modes, manages layout and coordinate systems, and defines core visual properties like colors and fonts.

-   **Render Orchestration:**
    -   [`Visualizer`](visualizer.py): The main class for rendering in **interactive modes** ("play", "debug"). It maintains the Pygame screen, calculates layout using `layout.py`, manages cached preview area rectangles, and calls appropriate drawing functions from [`trianglengin.ui.visualization.drawing`](../drawing/README.md). **It receives interaction state (hover position, selected index) via its `render` method to display visual feedback.**
-   **Layout Management:**
    -   [`layout.py`](layout.py): Contains functions (`calculate_interactive_layout`, `calculate_training_layout`) to determine the size and position of the main UI areas based on the screen dimensions, mode, and `DisplayConfig`.
-   **Coordinate System:**
    -   [`coord_mapper.py`](coord_mapper.py): Provides essential mapping functions:
        -   `_calculate_render_params`: Internal helper to get scaling and offset for grid rendering.
        -   `get_grid_coords_from_screen`: Converts mouse/screen coordinates into logical grid (row, column) coordinates.
        -   `get_preview_index_from_screen`: Converts mouse/screen coordinates into the index of the shape preview slot being pointed at.
-   **Visual Properties:**
    -   [`colors.py`](colors.py): Defines a centralized palette of named color constants (RGB tuples).
    -   [`fonts.py`](fonts.py): Contains the `load_fonts` function to load and manage Pygame font objects.

## Exposed Interfaces

-   **Classes:**
    -   `Visualizer` (Import directly from `visualizer.py`, not exported here)
-   **Functions:**
    -   `calculate_interactive_layout(...) -> Dict[str, pygame.Rect]`
    -   `calculate_training_layout(...) -> Dict[str, pygame.Rect]` (Kept for potential future use)
    -   `load_fonts() -> Dict[str, Optional[pygame.font.Font]]`
    -   `get_grid_coords_from_screen(...) -> Optional[Tuple[int, int]]`
    -   `get_preview_index_from_screen(...) -> Optional[int]`
-   **Modules:**
    -   `colors`: Provides color constants (e.g., `colors.RED`).
    -   `layout`: Provides layout calculation functions.
    -   `coord_mapper`: Provides coordinate mapping functions.
    -   `fonts`: Provides font loading functions.

## Dependencies

-   **`trianglengin` (core):** `GameState`, `EnvConfig`, `Shape`.
-   **`trianglengin.ui.config`**: `DisplayConfig`.
-   **`trianglengin.utils`**: `geometry`.
-   **`trianglengin.ui.visualization.drawing`**: Drawing functions are called by `Visualizer`.
-   **`pygame`**: Used for surfaces, rectangles, fonts, display management.
-   **Standard Libraries:** `typing`, `logging`, `math`.

---

**Note:** Please keep this README updated when changing the core rendering logic, layout calculations, coordinate mapping, or the interfaces of the renderers.
