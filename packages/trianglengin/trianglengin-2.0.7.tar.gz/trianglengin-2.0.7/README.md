
[![CI Status](https://github.com/lguibr/trianglengin/actions/workflows/ci_cd.yml/badge.svg)](https://github.com/lguibr/trianglengin/actions/workflows/ci_cd.yml)
[![codecov](https://codecov.io/gh/lguibr/trianglengin/graph/badge.svg?token=YOUR_CODECOV_TOKEN_HERE&flag=trianglengin)](https://codecov.io/gh/lguibr/trianglengin)
[![PyPI version](https://badge.fury.io/py/trianglengin.svg)](https://badge.fury.io/py/trianglengin)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

# Triangle Engine (`trianglengin`) v2.0.3
<img src="bitmap.png" alt="trianglengin logo" width="300"/>

**Version 2 introduces a high-performance C++ core for the game logic.**

This library provides the core components for a triangle puzzle game, suitable for reinforcement learning agents or other applications requiring a fast game engine. Interactive play/debug modes are included.

It encapsulates:

1.  **Core Game Logic (C++):** High-performance implementation of environment rules, state representation, actions, placement validation, and line clearing. ([`src/trianglengin/cpp/README.md`](src/trianglengin/cpp/README.md))
2.  **Python Interface:** A Python `GameState` wrapper providing a user-friendly API to interact with the C++ core. ([`src/trianglengin/game_interface.py`](src/trianglengin/game_interface.py))
3.  **Configuration (Python/Pydantic):** Models for environment settings (`EnvConfig`). ([`src/trianglengin/config/README.md`](src/trianglengin/config/README.md))
4.  **Utilities (Python):** General helpers, geometry functions, shared types. ([`src/trianglengin/utils/README.md`](src/trianglengin/utils/README.md))
5.  **UI Components (Python/Pygame/Typer):** Basic visualization, interaction handling, and CLI for interactive modes. ([`src/trianglengin/ui/README.md`](src/trianglengin/ui/README.md))

---



## 🎮 The Ultimate Triangle Puzzle Guide 🧩

Get ready to become a Triangle Master! This guide explains everything you need to know to play the game, step-by-step, with lots of details!

### 1. Introduction: Your Mission! 🎯

Your goal is to place colorful shapes onto a special triangular grid. By filling up lines of triangles, you make them disappear and score points! Keep placing shapes and clearing lines for as long as possible to get the highest score before the grid fills up and you run out of moves. Sounds simple? Let's dive into the details!

### 2. The Playing Field: The Grid 🗺️

- **Triangle Cells:** The game board is a grid made of many small triangles. Some point UP (🔺) and some point DOWN (🔻). They alternate like a checkerboard pattern based on their row and column index (specifically, `(row + col) % 2 != 0` means UP).
- **Shape:** The grid itself is rectangular overall, but the playable area within it is typically shaped like a triangle or hexagon, wider in the middle and narrower at the top and bottom.
- **Playable Area:** You can only place shapes within the designated playable area.
- **Death Zones 💀:** Around the edges of the playable area (often at the start and end of rows), some triangles are marked as "Death Zones". You **cannot** place any part of a shape onto these triangles. They are off-limits! Think of them as the boundaries within the rectangular grid.

### 3. Your Tools: The Shapes 🟦🟥🟩

- **Shape Formation:** Each shape is a collection of connected small triangles (🔺 and 🔻). They come in different colors and arrangements. Some might be a single triangle, others might be long lines, L-shapes, or more complex patterns.
- **Relative Positions:** The triangles within a shape have fixed positions _relative to each other_. When you move the shape, all its triangles move together as one block.
- **Preview Area:** You will always have **three** shapes available to choose from at any time. These are shown in a special "preview area" on the side of the screen.

### 4. Making Your Move: Placing Shapes 🖱️➡️▦

This is the core action! Here's exactly how to place a shape:

- **Step 4a: Select a Shape:** Look at the three shapes in the preview area. Click on the one you want to place. It should highlight 💡 to show it's selected.
- **Step 4b: Aim on the Grid:** Move your mouse cursor over the main grid. You'll see a faint "ghost" image of your selected shape following your mouse. This preview helps you aim.
- **Step 4c: The Placement Rules (MUST Follow!)**
  - 📏 **Rule 1: Fit Inside Playable Area:** ALL triangles of your chosen shape must land within the playable grid area. No part of the shape can land in a Death Zone 💀.
  - 🧱 **Rule 2: No Overlap:** ALL triangles of your chosen shape must land on currently _empty_ spaces on the grid. You cannot place a shape on top of triangles that are already filled with color from previous shapes.
  - 📐 **Rule 3: Orientation Match!** This is crucial!
    - If a part of your shape is an UP triangle (🔺), it MUST land on an UP space (🔺) on the grid.
    - If a part of your shape is a DOWN triangle (🔻), it MUST land on a DOWN space (🔻) on the grid.
    - 🔺➡️🔺 (OK!)
    - 🔻➡️🔻 (OK!)
    - 🔺➡️🔻 (INVALID! ❌)
    - 🔻➡️🔺 (INVALID! ❌)
  - **Visual Feedback:** The game helps you!
    - 👍 **Valid Spot:** If the position under your mouse follows ALL three rules, the ghost preview will usually look solid and possibly greenish. This means you _can_ place the shape here.
    - 👎 **Invalid Spot:** If the position breaks _any_ of the rules (out of bounds, overlaps, wrong orientation), the ghost preview will usually look faded and possibly reddish. This means you _cannot_ place the shape here.
- **Step 4d: Confirm Placement:** Once you find a **valid** spot (👍), click the left mouse button again. _Click!_ The shape is now placed permanently on the grid! ✨

### 5. Scoring Points: How You Win! 🏆

You score points in two main ways:

- **Placing Triangles:** You get a small number of points for _every single small triangle_ that makes up the shape you just placed. (e.g., placing a 3-triangle shape might give you 3 \* tiny_score points).
- **Clearing Lines:** This is where the BIG points come from! You get a much larger number of points for _every single small triangle_ that disappears when you clear a line (or multiple lines at once!). See the next section for details!

### 6. Line Clearing Magic! ✨ (The Key to High Scores!)

This is the most exciting part! When you place a shape, the game immediately checks if you've completed any lines. This section explains how the game _finds_ and _clears_ these lines.

- **What Lines Can Be Cleared?** There are **three** types of lines the game looks for:

  - **Horizontal Lines ↔️:** A straight, unbroken line of filled triangles going across a single row.
  - **Diagonal Lines (Top-Left to Bottom-Right) ↘️:** An unbroken diagonal line of filled triangles stepping down and to the right.
  - **Diagonal Lines (Bottom-Left to Top-Right) ↗️:** An unbroken diagonal line of filled triangles stepping up and to the right.

- **How Lines are Found: Pre-calculation of Maximal Lines**

  - **The Idea:** Instead of checking every possible line combination all the time, the game pre-calculates all *maximal* continuous lines of playable triangles when it starts. A **maximal line** is the longest possible straight segment of *playable* triangles (not in a Death Zone) in one of the three directions (Horizontal, Diagonal ↘️, Diagonal ↗️).
  - **Tracing:** For every playable triangle on the grid, the game traces outwards in each of the three directions to find the full extent of the continuous playable line passing through that triangle in that direction.
  - **Storing Maximal Lines:** Only the complete maximal lines found are stored. For example, if tracing finds a playable sequence `A-B-C-D`, only the line `(A,B,C,D)` is stored, not the sub-segments like `(A,B,C)` or `(B,C,D)`. These maximal lines represent the *potential* lines that can be cleared.
  - **Coordinate Map:** The game also builds a map linking each playable triangle coordinate `(r, c)` to the set of maximal lines it belongs to. This allows for quick lookup.

- **Defining the Paths (Neighbor Logic):** How does the game know which triangle is "next" when tracing? It depends on the current triangle's orientation (🔺 or 🔻) and the direction being traced:

  - **Horizontal ↔️:**
    - Left Neighbor: `(r, c-1)` (Always in the same row)
    - Right Neighbor: `(r, c+1)` (Always in the same row)
  - **Diagonal ↘️ (TL-BR):**
    - If current is 🔺 (Up): Next is `(r+1, c)` (Down triangle directly below)
    - If current is 🔻 (Down): Next is `(r, c+1)` (Up triangle to the right)
  - **Diagonal ↗️ (BL-TR):**
    - If current is 🔻 (Down): Next is `(r-1, c)` (Up triangle directly above)
    - If current is 🔺 (Up): Next is `(r, c+1)` (Down triangle to the right)

- **Visualizing the Paths:**

  - **Horizontal ↔️:**
    ```
    ... [🔻][🔺][🔻][🔺][🔻][🔺] ...  (Moves left/right in the same row)
    ```
  - **Diagonal ↘️ (TL-BR):** (Connects via shared horizontal edges)
    ```
    ...[🔺]...
    ...[🔻][🔺] ...
    ...     [🔻][🔺] ...
    ...         [🔻] ...
    (Path alternates row/col increments depending on orientation)
    ```
  - **Diagonal ↗️ (BL-TR):** (Connects via shared horizontal edges)
    ```
    ...           [🔺]  ...
    ...      [🔺][🔻]   ...
    ... [🔺][🔻]        ...
    ... [🔻]            ...
    (Path alternates row/col increments depending on orientation)
    ```

- **The "Full Line" Rule:** After you place a piece, the game looks at the coordinates `(r, c)` of the triangles you just placed. Using the pre-calculated map, it finds all the *maximal* lines that contain _any_ of those coordinates. For each of those maximal lines (that have at least 2 triangles), it checks: "Is _every single triangle coordinate_ in this maximal line now occupied?" If yes, that line is complete! (Note: Single isolated triangles don't count as clearable lines).

- **The _Poof_! 💨:**
  - If placing your shape completes one or MORE maximal lines (of any type, length >= 2) simultaneously, all the triangles in ALL completed lines vanish instantly!
  - The spaces become empty again.
  - You score points for _every single triangle_ that vanished. Clearing multiple lines at once is the best way to rack up points! 🥳

### 7. Getting New Shapes: The Refill 🪄

- **The Trigger:** The game only gives you new shapes when a specific condition is met.
- **The Condition:** New shapes appear **only when all three of your preview slots become empty at the exact same time.**
- **How it Happens:** This usually occurs right after you place your _last_ available shape (the third one).
- **The Refill:** As soon as the third slot becomes empty, _BAM!_ 🪄 Three brand new, randomly generated shapes instantly appear in the preview slots.
- **Important:** If you place a shape and only one or two slots are empty, you **do not** get new shapes yet. You must use up all three before the refill happens.

### 8. The End of the Road: Game Over 😭

So, how does the game end?

- **The Condition:** The game is over when you **cannot legally place _any_ of the three shapes currently available in your preview slots anywhere on the grid.**
- **The Check:** After every move (placing a shape and any resulting line clears), and after any potential shape refill, the game checks: "Is there at least one valid spot on the grid for Shape 1? OR for Shape 2? OR for Shape 3?"
- **No More Moves:** If the answer is "NO" for all three shapes (meaning none of them can be placed anywhere according to the Placement Rules), then the game immediately ends.
- **Strategy:** This means you need to be careful! Don't fill up the grid in a way that leaves no room for the types of shapes you might get later. Always try to keep options open! 🤔

That's it! Now you know all the rules. Go forth and conquer the Triangle Puzzle! 🏆

---

## Purpose

The primary goal is to provide a self-contained, installable library for the core logic and basic interactive UI of the triangle puzzle game. This allows different RL agent implementations or other applications to build upon a consistent and well-defined game backend, avoiding code duplication.


## Installation

**Prerequisites:**
*   A C++ compiler supporting C++17 (e.g., GCC, Clang, MSVC).
*   CMake (version 3.14 or higher).
*   Python (>= 3.10) and Pip.

```bash
# For standard use (once published or built):
pip install trianglengin>=2.0.3

# Building from source (requires compiler and CMake):
git clone https://github.com/lguibr/trianglengin.git
cd trianglengin
pip install .
```
*(Note: `pygame` and `typer` will be installed as core dependencies).*

## Running Interactive Modes

After installing, you can run the interactive modes directly:

- **Play Mode:**
  ```bash
  trianglengin play [--seed 42] [--log-level INFO]
  ```
- **Debug Mode:**
  ```bash
  trianglengin debug [--seed 42] [--log-level DEBUG]
  ```

---

## Local Development & Testing

These instructions are for developers contributing to `trianglengin`.

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/lguibr/trianglengin.git
    cd trianglengin
    ```

2.  **Prerequisites:** Ensure you have a C++17 compiler and CMake installed.

3.  **Create and Activate Virtual Environment:** (venv or conda)
    ```bash
    # Example using venv
    python -m venv venv
    source venv/bin/activate # or .\venv\Scripts\activate on Windows
    ```
    **IMPORTANT:** Ensure your virtual environment is activated.

4.  **Install Build Dependencies:** (Needed even for core dev)
    ```bash
    pip install pybind11>=2.10 cmake wheel
    ```

5.  **Clean Previous Builds (Optional but Recommended):**
    ```bash
    rm -rf build/ src/trianglengin.egg-info/ dist/ src/trianglengin/trianglengin_cpp.*.so src/trianglengin/trianglengin_cpp*.cpp
    ```

6.  **Install in Editable Mode with Dev Dependencies:**
    *   **Make sure your virtual environment is active!**
    *   Run from the project root directory:
        ```bash
        # Installs core, UI, and dev tools
        pip install -e '.[dev]'
        ```
        This command compiles the C++ extension and installs the Python package so changes are reflected immediately. It also installs development tools.

7.  **Running Checks:**
    *   **Make sure your virtual environment is active!**
    *   **Tests & Coverage:**
        ```bash
        pytest tests/ --cov=src/trianglengin --cov-report=xml
        ```
        (Coverage measures core Python code, excluding UI).
        To just run tests: `pytest`
    *   **Linting:** `ruff check .`
    *   **Formatting:** `ruff format .`
    *   **Type Checking:** `mypy src/trianglengin/ tests/`

8.  **Troubleshooting Build/Import Errors:**
    *   Ensure compiler and CMake are installed and in PATH.
    *   Make sure the virtual environment is active *before* running `pip install -e`.
    *   Clean previous builds (Step 5).
    *   Check `pyproject.toml` and `setup.py` for correct configuration.
    *   Verify Pybind11 version compatibility.

---

## Project Structure (v2 - UI Included)

```
trianglengin/
├── .github/workflows/      # GitHub Actions CI/CD
│   └── ci_cd.yml
├── src/                    # Source root
│   └── trianglengin/       # Python package source
│       ├── __init__.py     # Exposes core public API (GameState, EnvConfig, Shape)
│       ├── game_interface.py # Python GameState wrapper class
│       ├── py.typed        # PEP 561 marker
│       ├── cpp/            # C++ Core Implementation ([src/trianglengin/cpp/README.md])
│       │   ├── CMakeLists.txt
│       │   ├── bindings.cpp
│       │   ├── config.h
│       │   ├── structs.h
│       │   ├── grid_data.h / .cpp
│       │   ├── grid_logic.h / .cpp
│       │   ├── shape_logic.h / .cpp
│       │   └── game_state.h / .cpp
│       ├── core/           # Core Python components (now minimal/empty)
│       │   └── __init__.py
│       ├── utils/          # General Python utilities ([src/trianglengin/utils/README.md])
│       │   └── ... (geometry.py, types.py)
│       ├── config/         # Core configuration models ([src/trianglengin/config/README.md])
│       │   ├── __init__.py
│       │   └── env_config.py   # EnvConfig (Pydantic)
│       └── ui/             # UI Components ([src/trianglengin/ui/README.md])
│           ├── __init__.py # Exposes UI API (Application, cli_app, DisplayConfig)
│           ├── app.py      # Interactive mode application runner
│           ├── cli.py      # CLI definition (play/debug)
│           ├── config.py   # DisplayConfig (Pydantic)
│           ├── interaction/    # User input handling ([src/trianglengin/ui/interaction/README.md])
│           │   ├── __init__.py
│           │   ├── event_processor.py
│           │   ├── input_handler.py
│           │   ├── play_mode_handler.py
│           │   └── debug_mode_handler.py
│           └── visualization/  # Pygame rendering ([src/trianglengin/ui/visualization/README.md])
│               ├── __init__.py
│               ├── core/       # Core vis components ([src/trianglengin/ui/visualization/core/README.md])
│               │   ├── __init__.py
│               │   ├── colors.py
│               │   ├── coord_mapper.py
│               │   ├── fonts.py
│               │   ├── layout.py # NEW
│               │   └── visualizer.py
│               └── drawing/    # Drawing functions ([src/trianglengin/ui/visualization/drawing/README.md])
│                   ├── __init__.py
│                   ├── grid.py
│                   ├── highlight.py
│                   ├── hud.py
│                   ├── previews.py
│                   ├── shapes.py
│                   └── utils.py
├── tests/                  # Unit/Integration tests (Python) ([tests/README.md])
│   ├── __init__.py
│   ├── conftest.py
│   └── core/environment/
│       └── test_game_state.py # Tests the Python GameState wrapper
├── .gitignore
├── pyproject.toml          # Build config, dependencies
├── setup.py                # C++ Extension build script
├── README.md               # This file
├── LICENSE
└── MANIFEST.in
```

## Core Components (v2)

- **`trianglengin.cpp` (C++ Core)**: Implements the high-performance game logic (state, grid, shapes, rules). Not directly imported in Python.
- **`trianglengin.game_interface.GameState` (Python Wrapper)**: The primary Python class for interacting with the game engine. It holds a reference to the C++ game state object and provides methods like `step`, `reset`, `is_over`, `valid_actions`, `get_shapes`, `get_grid_data_np`, **`get_outcome`**.
- **`trianglengin.config.EnvConfig`**: Python Pydantic model for core environment configuration. Passed to C++ core during initialization.
- **`trianglengin.utils`**: General Python utility functions and types. ([`src/trianglengin/utils/README.md`](src/trianglengin/utils/README.md))

## UI Components (`trianglengin.ui`)

- **`trianglengin.ui.config.DisplayConfig`**: Pydantic model for UI display settings.
- **`trianglengin.ui.visualization`**: Python/Pygame rendering components. Uses data obtained from the `GameState` wrapper. ([`src/trianglengin/ui/visualization/README.md`](src/trianglengin/ui/visualization/README.md))
- **`trianglengin.ui.interaction`**: Python/Pygame input handling for interactive modes. Interacts with the `GameState` wrapper. ([`src/trianglengin/ui/interaction/README.md`](src/trianglengin/ui/interaction/README.md))
- **`trianglengin.ui.app.Application`**: Integrates UI components for interactive modes.
- **`trianglengin.ui.cli`**: Command-line interface (`trianglengin play`/`debug`).

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on the [GitHub repository](https://github.com/lguibr/trianglengin). Ensure that changes maintain code quality (pass tests, linting, type checking) and keep READMEs updated. Building requires a C++17 compiler and CMake.
