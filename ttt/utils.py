"""utils.py
Small helper utilities used across the project.
"""

from __future__ import annotations

import random
from typing import List, Tuple

from . import config


def set_random_seed(seed: int | None) -> None:
    """Optionally seed the random generator for reproducible AI behaviors."""
    if seed is not None:
        random.seed(seed)


def center_corners_sides_order(board) -> List[Tuple[int, int]]:
    """Return move ordering: center -> corners -> sides for pruning efficiency.

    This heuristic improves alpha-beta pruning by exploring more promising moves
    early, which often increases the number of pruned branches.
    """
    n = config.BOARD_SIZE
    center = (n // 2, n // 2)
    corners = [(0, 0), (0, n - 1), (n - 1, 0), (n - 1, n - 1)]

    # Sides are remaining edge cells excluding corners
    sides: List[Tuple[int, int]] = []
    for i in range(1, n - 1):
        sides.append((0, i))
        sides.append((n - 1, i))
        sides.append((i, 0))
        sides.append((i, n - 1))

    ordered: List[Tuple[int, int]] = []
    legal = set(board.legal_moves())

    if center in legal:
        ordered.append(center)

    for c in corners:
        if c in legal:
            ordered.append(c)

    for s in sides:
        if s in legal:
            ordered.append(s)

    # Append any legal move not covered above (e.g., for non-3x3 future boards)
    for move in board.legal_moves():
        if move not in ordered:
            ordered.append(move)

    return ordered


