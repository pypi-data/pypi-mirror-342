
# UI Visualization Drawing Submodule (`trianglengin.ui.visualization.drawing`)

**Requires:** `pygame`

## Purpose and Architecture

This submodule contains specialized functions responsible for drawing specific visual elements of the game onto Pygame surfaces for the **interactive modes** within the `trianglengin.ui` package. These functions are typically called by the core renderer (`Visualizer`) in [`trianglengin.ui.visualization.core`](../core/README.md).

-   **[`grid.py`](grid.py):** Functions for drawing the grid background (`draw_grid_background`), the individual triangles within it colored based on occupancy/emptiness (`draw_grid_state`), and optional debug overlays (`draw_debug_grid_overlay`).
-   **[`shapes.py`](shapes.py):** Contains `draw_shape`, a function to render a given `Shape` object at a specific location on a surface (used primarily for previews).
-   **[`previews.py`](previews.py):** Handles rendering related to shape previews:
    -   `render_previews`: Draws the dedicated preview area, including borders and the shapes within their slots, handling selection highlights.
    -   `draw_placement_preview`: Draws a semi-transparent version of a shape snapped to the grid, indicating a potential placement location (used in play mode hover).
    -   `draw_floating_preview`: Draws a semi-transparent shape directly under the mouse cursor when hovering over the grid but not snapped (used in play mode hover).
-   **[`hud.py`](hud.py):** `render_hud` draws Heads-Up Display elements like help text onto the main screen surface (simplified for interactive modes).
-   **[`highlight.py`](highlight.py):** `draw_debug_highlight` draws a distinct border around a specific triangle, used for visual feedback in debug mode.
-   **[`utils.py`](utils.py):** Helper functions, like `get_triangle_points`, used by other drawing functions.

## Exposed Interfaces

-   **Grid Drawing:**
    -   `draw_grid_background(...)`
    -   `draw_grid_state(...)`
    -   `draw_debug_grid_overlay(...)`
-   **Shape Drawing:**
    -   `draw_shape(...)`
-   **Preview Drawing:**
    -   `render_previews(...) -> Dict[int, pygame.Rect]`
    -   `draw_placement_preview(...)`
    -   `draw_floating_preview(...)`
-   **HUD Drawing:**
    -   `render_hud(...)`
-   **Highlight Drawing:**
    -   `draw_debug_highlight(...)`
-   **Utilities:**
    -   `get_triangle_points(...) -> list[tuple[float, float]]`

## Dependencies

-   **`trianglengin` (core):** `EnvConfig`, `GameState`, `Shape`.
-   **`trianglengin.ui.config`**: `DisplayConfig`.
-   **`trianglengin.ui.visualization.core`**: `colors`, `coord_mapper`.
-   **`pygame`**: The core library used for all drawing operations.
-   **Standard Libraries:** `typing`, `logging`, `math`.

---

**Note:** Please keep this README updated when adding new drawing functions, modifying existing ones, or changing their dependencies.