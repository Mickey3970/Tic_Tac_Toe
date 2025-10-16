"""
ttt package

This package contains a small, cleanly structured Tic-Tac-Toe game built with
an MVC-like separation:
- game: pure game logic (no pygame)
- ai: minimax-based AI
- controller: turn orchestration and game loop
- ui: pygame-based rendering and input handling
- config: central constants
- utils: helpers
"""

from . import game, ai, controller, ui, config, utils  # re-export for convenience

__all__ = [
    "game",
    "ai",
    "controller",
    "ui",
    "config",
    "utils",
]


