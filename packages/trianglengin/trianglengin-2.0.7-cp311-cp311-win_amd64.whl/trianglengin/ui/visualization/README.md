
# UI Visualization Module (`trianglengin.ui.visualization`)

**Requires:** `pygame`

## Purpose and Architecture

This module is responsible for rendering the game state visually using the Pygame library, specifically for the **interactive modes** (play/debug) provided by the `trianglengin.ui` package.

-   **Core Components ([`core/README.md`](core/README.md)):**
    -   `Visualizer`: Orchestrates the rendering process for interactive modes.
    -   `layout`: Calculates the screen positions and sizes for different UI areas.
    -   `fonts`: Loads necessary font files.
    -   `colors`: Defines a centralized palette of RGB color tuples.
    -   `coord_mapper`: Provides functions to map screen coordinates to grid coordinates and preview indices.
-   **Drawing Components ([`drawing/README.md`](drawing/README.md)):**
    -   Contains specific functions for drawing different elements onto Pygame surfaces (grid, shapes, previews, HUD, highlights).

**Note:** This module depends on the core `trianglengin` engine for game state data (`GameState`, `EnvConfig`, `Shape`).

## Exposed Interfaces

-   **Core Classes & Functions:**
    -   `Visualizer`: Main renderer for interactive modes.
    -   `load_fonts`: Loads Pygame fonts.
    -   `colors`: Module containing color constants (e.g., `colors.WHITE`).
    -   `get_grid_coords_from_screen`: Maps screen to grid coordinates.
    -   `get_preview_index_from_screen`: Maps screen to preview index.
-   **Drawing Functions:** (Exposed via `trianglengin.ui.visualization.drawing`)
-   **Config:** (Configs are *not* re-exported from this module)

## Dependencies

-   **`trianglengin` (core):** `GameState`, `EnvConfig`, `Shape`.
-   **`trianglengin.ui.config`**: `DisplayConfig`.
-   **`trianglengin.utils`**: `geometry`.
-   **`pygame`**: The core library used for all drawing, surface manipulation, and font rendering.
-   **Standard Libraries:** `typing`, `logging`, `math`.

---

**Note:** Please keep this README updated when changing rendering logic, adding new visual elements, modifying layout calculations, or altering the interfaces exposed.
