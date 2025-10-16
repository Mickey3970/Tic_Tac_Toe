"""ai.py
AI logic for choosing Tic-Tac-Toe moves.

Implements minimax with alpha-beta pruning. Terminal scores are mapped as:
- X win: +1, O win: -1 (from X's perspective)
- draw: 0

The pruning discards branches that cannot possibly influence the final decision
given current best alternatives, greatly speeding up search.
"""

from __future__ import annotations

import math
import random
from typing import List, Optional, Tuple

from . import config, utils
from .game import Board, Move


def choose_move(board: Board, player: str, difficulty: str) -> Move:
    """Return a move for the given difficulty level.

    - easy: mostly random with occasional 1-ply lookahead
    - medium: depth-limited minimax and small randomness
    - impossible: full minimax with alpha-beta pruning
    """
    difficulty = difficulty.lower()
    legal = board.legal_moves()
    if not legal:
        raise ValueError("No legal moves available")

    # Easy: 80% random, 20% 1-ply greedy
    if difficulty == "easy":
        if random.random() < 0.8:
            return random.choice(legal)
        # Greedy: pick winning move if exists else random
        for move in utils.center_corners_sides_order(board):
            r, c = move
            b2 = board.copy()
            b2.make_move(r, c, player)
            winner, _ = b2.check_winner()
            if winner == player:
                return move
        return random.choice(legal)

    # Medium: depth-limited search with slight randomness
    if difficulty == "medium":
        if random.random() < 0.3:
            return random.choice(legal)
        _, best = minimax(board, player, depth=3, alpha=-math.inf, beta=math.inf)
        return best if best is not None else random.choice(legal)

    # Impossible: optimal play using full minimax
    # First, short-circuit for immediate win or immediate block to reduce depth
    # and guarantee correct tactical play.
    opponent = config.PLAYER_O if player == config.PLAYER_X else config.PLAYER_X
    # Play winning move if available
    for move in utils.center_corners_sides_order(board):
        r, c = move
        b2 = board.copy()
        b2.make_move(r, c, player)
        w, _ = b2.check_winner()
        if w == player:
            return move
    # Otherwise block opponent's immediate win
    for move in utils.center_corners_sides_order(board):
        r, c = move
        b2 = board.copy()
        b2.make_move(r, c, opponent)
        w, _ = b2.check_winner()
        if w == opponent:
            return move

    score, best = minimax(board, player, depth=None, alpha=-math.inf, beta=math.inf)
    return best if best is not None else random.choice(legal)


def minimax(
    board: Board,
    player: str,
    depth: Optional[int],
    alpha: float,
    beta: float,
) -> Tuple[float, Optional[Move]]:
    """Minimax with alpha-beta pruning.

    The evaluation is from X's perspective: X tries to maximize, O to minimize.
    `depth=None` explores to terminal states; otherwise limits recursion depth.
    Move ordering uses a center->corners->sides heuristic to accelerate pruning.
    """
    winner, _ = board.check_winner()
    if winner == config.PLAYER_X:
        return 1.0, None
    if winner == config.PLAYER_O:
        return -1.0, None
    if board.is_full():
        return 0.0, None

    if depth == 0:
        # For a small board like 3x3, non-terminal depth cutoffs can return 0.
        # A more advanced heuristic could be plugged in here for larger boards.
        return 0.0, None

    is_maximizing = player == config.PLAYER_X
    next_player = config.PLAYER_O if player == config.PLAYER_X else config.PLAYER_X

    best_move: Optional[Move] = None
    if is_maximizing:
        best_score = -math.inf
        for r, c in utils.center_corners_sides_order(board):
            b2 = board.copy()
            b2.make_move(r, c, player)
            score, _ = minimax(b2, next_player, None if depth is None else depth - 1, alpha, beta)
            if score > best_score:
                best_score = score
                best_move = (r, c)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break  # prune
        return best_score, best_move
    else:
        best_score = math.inf
        for r, c in utils.center_corners_sides_order(board):
            b2 = board.copy()
            b2.make_move(r, c, player)
            score, _ = minimax(b2, next_player, None if depth is None else depth - 1, alpha, beta)
            if score < best_score:
                best_score = score
                best_move = (r, c)
            beta = min(beta, best_score)
            if beta <= alpha:
                break  # prune
        return best_score, best_move


