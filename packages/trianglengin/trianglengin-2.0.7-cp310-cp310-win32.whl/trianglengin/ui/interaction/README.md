
# UI Interaction Module (`trianglengin.ui.interaction`)

**Requires:** `pygame`

## Purpose

This submodule handles user input (keyboard and mouse) for the interactive modes ("play", "debug") provided by the `trianglengin.ui` package. It bridges the gap between raw Pygame events and actions within the game simulation (`GameState` from the core engine).

-   **Event Processing:** [`event_processor.py`](event_processor.py) handles common Pygame events like quitting (QUIT, ESC) and window resizing. It acts as a generator, yielding other events for mode-specific processing.
-   **Input Handler:** The [`InputHandler`](input_handler.py) class is the main entry point for this submodule.
    -   It receives Pygame events (via the `event_processor`).
    -   It **manages interaction-specific state** internally (e.g., `selected_shape_idx`, `hover_grid_coord`, `debug_highlight_coord`).
    -   It determines the current interaction mode ("play" or "debug") and delegates event handling and hover updates to specific handler functions ([`play_mode_handler.py`](play_mode_handler.py), [`debug_mode_handler.py`](debug_mode_handler.py)).
    -   It provides the necessary interaction state to the `trianglengin.ui.visualization.Visualizer` for rendering feedback (hover previews, selection highlights).
-   **Mode-Specific Handlers:** `play_mode_handler.py` and `debug_mode_handler.py` contain the logic specific to each mode, operating on the `InputHandler`'s state and the core `GameState`.
    -   `play`: Handles selecting shapes, checking placement validity, and triggering `GameState.step` on valid clicks. Updates hover state in the `InputHandler`.
    -   `debug`: Handles toggling the state of individual triangles directly using `GameState.debug_toggle_cell`. Updates hover state in the `InputHandler`.
-   **Decoupling:** It separates input handling logic from the core game simulation (`trianglengin`) and rendering (`trianglengin.ui.visualization`), although it needs references to both to function within the UI application.

## Exposed Interfaces

-   **Classes:**
    -   `InputHandler`:
        -   `__init__(game_state: GameState, visualizer: Visualizer, mode: str, env_config: EnvConfig)`
        -   `handle_input() -> bool`: Processes events for one frame, returns `False` if quitting.
        -   `get_render_interaction_state() -> dict`: Returns interaction state needed by `Visualizer.render`.
-   **Functions:**
    -   `process_pygame_events(visualizer: Visualizer) -> Generator[pygame.event.Event, Any, bool]`: Processes common events, yields others.
    -   `handle_play_click(event: pygame.event.Event, handler: InputHandler)`: Handles clicks in play mode.
    -   `update_play_hover(handler: InputHandler)`: Updates hover state in play mode.
    -   `handle_debug_click(event: pygame.event.Event, handler: InputHandler)`: Handles clicks in debug mode.
    -   `update_debug_hover(handler: InputHandler)`: Updates hover state in debug mode.

## Dependencies

-   **`trianglengin` (core):** `GameState`, `EnvConfig`, `Shape`.
-   **`trianglengin.ui.visualization`**: `Visualizer`, `coord_mapper`.
-   **`pygame`**: Relies heavily on Pygame for event handling (`pygame.event`, `pygame.mouse`) and constants (`MOUSEBUTTONDOWN`, `KEYDOWN`, etc.).
-   **Standard Libraries:** `typing`, `logging`.

---

**Note:** Please keep this README updated when adding new interaction modes, changing input handling logic, or modifying the interfaces between interaction, environment, and visualization.
