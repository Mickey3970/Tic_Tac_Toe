"""game.py
Pure game logic for Tic-Tac-Toe, independent of pygame.

Provides a `Board` class with utilities for making moves, checking wins,
copying state, and enumerating legal moves. This module is fully unit-testable.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from . import config


Move = Tuple[int, int]


@dataclass
class Board:
    """Immutable-ish board state for Tic-Tac-Toe.

    Internally stores a 2D list of values: "X", "O", or None for empty. Methods
    that modify the board return booleans for success, and the board can be
    copied with `.copy()` for search algorithms.
    """

    size: int = field(default_factory=lambda: config.BOARD_SIZE)
    grid: List[List[Optional[str]]] = field(init=False)

    def __post_init__(self) -> None:
        self.grid = [[config.EMPTY for _ in range(self.size)] for _ in range(self.size)]

    def reset(self) -> None:
        """Clear all cells to empty."""
        for r in range(self.size):
            for c in range(self.size):
                self.grid[r][c] = config.EMPTY

    def copy(self) -> "Board":
        """Return a shallow copy of the board state for search algorithms."""
        new_board = Board(self.size)
        new_board.grid = [row[:] for row in self.grid]
        return new_board

    def make_move(self, row: int, col: int, player: str) -> bool:
        """Place a player's symbol if the cell is empty.

        Returns True if move applied; False otherwise.
        """
        if not (0 <= row < self.size and 0 <= col < self.size):
            return False
        if self.grid[row][col] is not config.EMPTY:
            return False
        self.grid[row][col] = player
        return True

    def legal_moves(self) -> List[Move]:
        """Return list of available (row, col) coordinates."""
        moves: List[Move] = []
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] is config.EMPTY:
                    moves.append((r, c))
        return moves

    def is_full(self) -> bool:
        """Return True when no empty cells remain."""
        for row in self.grid:
            for cell in row:
                if cell is config.EMPTY:
                    return False
        return True

    def check_winner(self) -> Tuple[Optional[str], Optional[List[Move]]]:
        """Check for a winner.

        Returns a tuple (winner, line) where `winner` is "X", "O" or None, and
        `line` is the list of winning coordinates or None if no winner.
        Works for any N×N board size.
        """
        n = self.size

        # Check rows and columns
        for i in range(n):
            # Row i
            if self.grid[i][0] is not config.EMPTY and all(self.grid[i][j] == self.grid[i][0] for j in range(1, n)):
                return self.grid[i][0], [(i, j) for j in range(n)]
            # Column i
            if self.grid[0][i] is not config.EMPTY and all(self.grid[j][i] == self.grid[0][i] for j in range(1, n)):
                return self.grid[0][i], [(j, i) for j in range(n)]

        # Main diagonal
        if self.grid[0][0] is not config.EMPTY and all(self.grid[k][k] == self.grid[0][0] for k in range(1, n)):
            return self.grid[0][0], [(k, k) for k in range(n)]

        # Anti-diagonal
        if self.grid[0][n - 1] is not config.EMPTY and all(
            self.grid[k][n - 1 - k] == self.grid[0][n - 1] for k in range(1, n)
        ):
            return self.grid[0][n - 1], [(k, n - 1 - k) for k in range(n)]

        return None, None


