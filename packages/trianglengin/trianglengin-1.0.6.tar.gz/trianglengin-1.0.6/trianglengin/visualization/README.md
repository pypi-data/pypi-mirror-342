# File: trianglengin/visualization/README.md

# Visualization Module (`trianglengin.visualization`)

## Purpose and Architecture

This module is responsible for rendering the game state visually using the Pygame library, specifically for the **interactive modes** (play/debug) provided directly by the `trianglengin` library.

-   **Core Components ([`core/README.md`](core/README.md)):**
    -   `Visualizer`: Orchestrates the rendering process for interactive modes.
    -   `layout`: Calculates the screen positions and sizes for different UI areas.
    -   `fonts`: Loads necessary font files.
    -   `colors`: Defines a centralized palette of RGB color tuples.
    -   `coord_mapper`: Provides functions to map screen coordinates to grid coordinates and preview indices.
-   **Drawing Components ([`drawing/README.md`](drawing/README.md)):**
    -   Contains specific functions for drawing different elements onto Pygame surfaces (grid, shapes, previews, HUD, highlights).

**Note:** More advanced visualization components related to training (e.g., dashboards, plots, progress bars) would typically reside in a separate project that uses this engine.

## Exposed Interfaces

-   **Core Classes & Functions:**
    -   `Visualizer`: Main renderer for interactive modes.
    -   `calculate_interactive_layout`, `calculate_training_layout`: Calculates UI layout rectangles.
    -   `load_fonts`: Loads Pygame fonts.
    -   `colors`: Module containing color constants (e.g., `colors.WHITE`).
    -   `get_grid_coords_from_screen`: Maps screen to grid coordinates.
    -   `get_preview_index_from_screen`: Maps screen to preview index.
-   **Drawing Functions:** (Exposed via `trianglengin.visualization.drawing`)
-   **Config:**
    -   `DisplayConfig`: Configuration class (re-exported from `trianglengin.config`).
    -   `EnvConfig`: Configuration class (re-exported from `trianglengin.config`).

## Dependencies

-   **`trianglengin.core`**: `GameState`, `EnvConfig`, `GridData`, `Shape`, `Triangle`.
-   **`trianglengin.config`**: `DisplayConfig`.
-   **`trianglengin.utils`**: `geometry` (Planned).
-   **`pygame`**: The core library used for all drawing, surface manipulation, and font rendering.
-   **Standard Libraries:** `typing`, `logging`, `math`.

---

**Note:** Please keep this README updated when changing rendering logic, adding new visual elements, modifying layout calculations, or altering the interfaces exposed.