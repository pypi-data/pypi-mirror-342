# trianglengin/core/environment/grid/__init__.py
"""
Modules related to the game grid structure and logic.

Provides:
- GridData: Class representing the grid state.
- logic: Module containing grid-related logic (placement, line clearing).
- line_cache: Module for caching precomputed lines.

See GridData documentation: [grid_data.py](grid_data.py)
See Grid Logic documentation: [logic.py](logic.py)
See Line Cache documentation: [line_cache.py](line_cache.py)
"""

from . import line_cache, logic
from .grid_data import GridData

__all__ = ["GridData", "logic", "line_cache"]
