

# UI Module (`trianglengin.ui`)

## Purpose

This module provides components for interacting with and visualizing the `trianglengin` game engine using Pygame and Typer. It is included as part of the main package installation.

## Components

-   **[`config.py`](config.py):** Defines `DisplayConfig` for UI-specific settings (screen size, FPS, fonts, colors).
-   **[`visualization/`](visualization/README.md):** Contains the `Visualizer` class and drawing functions responsible for rendering the game state using Pygame.
-   **[`interaction/`](interaction/README.md):** Contains the `InputHandler` class and helper functions to process keyboard/mouse input for interactive modes.
-   **[`app.py`](app.py):** The `Application` class integrates the `GameState` (from the core engine), `Visualizer`, and `InputHandler` to run the interactive application loop.
-   **[`cli.py`](cli.py):** Defines the command-line interface using Typer, providing the `trianglengin play` and `trianglengin debug` commands.

## Usage

After installing the `trianglengin` package (`pip install trianglengin`), you can run the interactive commands:

```bash
trianglengin play
trianglengin debug --seed 123
```

## Dependencies

-   **`trianglengin` (core):** Uses `GameState`, `EnvConfig`, `Shape`.
-   **`pygame`**: Required dependency for graphics, event handling, fonts.
-   **`typer`**: Required dependency for the command-line interface.
-   **Standard Libraries:** `typing`, `logging`, `sys`, `random`.

---

**Note:** While included, these UI components are designed to be initialized only when running the specific CLI commands (`play`, `debug`) and should not interfere with using the core `trianglengin` library for simulations.
