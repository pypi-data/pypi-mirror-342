# File: tests/core/environment/README.md
# Environment Tests (`tests/core/environment`)

## Purpose

This directory contains tests specifically for the game environment's core functionality, primarily focusing on the **Python `GameState` wrapper** which interacts with the underlying C++ engine.

-   **[`test_game_state.py`](test_game_state.py):** This is the main test suite. It verifies the behavior of the `trianglengin.game_interface.GameState` Python class. Tests cover:
    -   Initialization and reset.
    -   Valid and invalid `step` calls.
    -   Score calculation (placement, line clearing, penalties).
    -   Game over conditions (`is_over`, `get_game_over_reason`).
    -   Retrieval of state information (`get_grid_data_np`, `get_shapes`).
    -   Valid action calculation (`valid_actions`).
    -   State copying (`copy`).
    -   Debug functionality (`debug_toggle_cell`).

## Approach

Since the core game logic (grid operations, shape handling, line clearing, action validation) is implemented in C++, these tests primarily focus on ensuring the Python wrapper correctly interfaces with the C++ module (`trianglengin_cpp`). They validate that:

1.  Python methods call the corresponding C++ functions.
2.  Data is correctly transferred between Python and C++ (e.g., configurations, grid state, shapes, actions, rewards).
3.  The wrapper handles edge cases and errors appropriately (e.g., invalid actions).
4.  The overall game flow (steps, resets, game over) behaves as expected from the Python perspective.

Direct testing of individual C++ functions or classes would typically be done using a C++ testing framework (like Google Test), which is outside the scope of these Python tests.

## Dependencies

-   **`pytest`**: Test runner and fixtures.
-   **`numpy`**: Used for checking grid data arrays.
-   **`trianglengin.game_interface`**: The `GameState` wrapper and `Shape` class being tested.
-   **`trianglengin.config`**: `EnvConfig` used for setup.

---

**Note:** Keep this README updated if the testing strategy changes or significant new test files related to the environment wrapper are added.