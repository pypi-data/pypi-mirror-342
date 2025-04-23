# Core engine exports
from .config import EnvConfig
from .game_interface import (
    GameState,
    Shape,
)
from .utils import ActionType, geometry

__all__ = [
    # Core Interface & Config
    "GameState",
    "Shape",
    "EnvConfig",
    # Utilities & Types
    "utils",
    "geometry",
    "ActionType",
]

# Attempt to import the C++ module to make its version accessible (optional)
try:
    from . import trianglengin_cpp as _cpp_module

    __version__ = _cpp_module.__version__
except ImportError:
    # If C++ module not found (e.g., during docs build without compilation)
    # Try getting version from package metadata if installed
    try:
        from importlib.metadata import version

        __version__ = version("trianglengin")
    except ImportError:
        __version__ = "unknown"  # Fallback
    except Exception:
        __version__ = "unknown (C++ module not found, package metadata failed)"
