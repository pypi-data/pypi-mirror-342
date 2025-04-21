

# Core Configuration Module (`trianglengin.config`)

## Purpose

This module defines the core configuration settings for the `trianglengin` game engine, independent of any UI components.

-   **[`env_config.py`](env_config.py):** Defines the `EnvConfig` Pydantic model. This class holds parameters crucial to the game simulation itself, such as:
    -   Grid dimensions (`ROWS`, `COLS`).
    -   Playable area definition (`PLAYABLE_RANGE_PER_ROW`).
    -   Number of shape preview slots (`NUM_SHAPE_SLOTS`).
    -   Reward/penalty values used by the C++ engine (`REWARD_PER_PLACED_TRIANGLE`, `REWARD_PER_CLEARED_TRIANGLE`, `REWARD_PER_STEP_ALIVE`, `PENALTY_GAME_OVER`).

## Usage

An instance of `EnvConfig` is typically created and passed to the `trianglengin.game_interface.GameState` wrapper during initialization. The wrapper then passes these settings to the underlying C++ engine.

```python
from trianglengin import GameState, EnvConfig

# Use default configuration
default_config = EnvConfig()
game = GameState(config=default_config)

# Use custom configuration
custom_config = EnvConfig(ROWS=10, COLS=10, PLAYABLE_RANGE_PER_ROW=[(0,10)]*10)
custom_game = GameState(config=custom_config)
```

## Dependencies

-   **`pydantic`**: Used for data validation and settings management.
-   **Standard Libraries:** `typing`.

---

**Note:** Configuration related to display or interactive UI elements (like screen size, FPS, fonts) is handled separately in the optional `trianglengin.ui.config` module.
