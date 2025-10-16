"""controller.py
Game loop orchestration and turn handling.

Responsible for sequencing turns, delegating input/rendering to `ui`, and
calling into the AI when appropriate. Contains no drawing logic itself.
"""

from __future__ import annotations

import pygame
from typing import Optional, Tuple, List

from . import ai, config, ui
from .game import Board


class GameController:
    """High-level controller for the Tic-Tac-Toe match."""

    def __init__(self, mode: str, difficulty: str) -> None:
        self.mode = mode
        self.difficulty = difficulty
        self.board = Board()
        self.current_player = config.PLAYER_X
        self.winner: Optional[str] = None
        self.winning_line = None
        self.ui = ui.GameUI(self.board, self.mode, self.difficulty)
        # Move history for replay: list of (row, col, player)
        self.history: List[Tuple[int, int, str]] = []
        self.replaying: bool = False
        self.replay_index: int = 0
        self._replay_last_ts: int = 0

    def reset(self) -> None:
        """Reset board and state to start a new game."""
        self.board.reset()
        self.current_player = config.PLAYER_X
        self.winner = None
        self.winning_line = None
        self.ui.on_reset()
        self.history.clear()
        self.replaying = False
        self.replay_index = 0

    def run(self) -> None:
        """Main loop. Delegates events to UI and performs AI/human moves."""
        clock = pygame.time.Clock()
        running = True
        while running:
            # Handle user inputs via UI helper
            action = self.ui.handle_events()
            if action.get("quit"):
                running = False
                continue
            if action.get("restart"):
                self.reset()
                continue
            if action.get("toggle_difficulty"):
                self._cycle_difficulty()
                self.ui.set_difficulty(self.difficulty)
            if action.get("replay") and (self.winner or self.board.is_full()):
                self._start_replay()

            # Human move attempt
            cell = action.get("place")
            if cell and not self.winner and not self.replaying:
                r, c = cell
                if self._is_human_turn() and self.board.make_move(r, c, self.current_player):
                    self.history.append((r, c, self.current_player))
                    self._post_move_update()

            # AI move (if applicable)
            if not self.winner and self._is_ai_turn() and not self.replaying:
                move = ai.choose_move(self.board, self.current_player, self.difficulty)
                self.board.make_move(move[0], move[1], self.current_player)
                self.history.append((move[0], move[1], self.current_player))
                self._post_move_update()

            # Handle replay state machine (non-blocking)
            if self.replaying:
                now = pygame.time.get_ticks()
                if self._replay_last_ts == 0 or now - self._replay_last_ts >= config.REPLAY_STEP_MS:
                    self._replay_last_ts = now
                    if self.replay_index < len(self.history):
                        r, c, p = self.history[self.replay_index]
                        self.board.make_move(r, c, p)
                        self.replay_index += 1
                        self.winner, self.winning_line = self.board.check_winner()
                    else:
                        # End of replay
                        self.replaying = False

            # Draw current frame
            self.ui.render(self.board, self.current_player, self.winner, self.winning_line)
            clock.tick(60)

        pygame.quit()

    def _is_human_turn(self) -> bool:
        if self.mode == "HvsH":
            return True
        if self.mode == "HvsAI":
            # human is X by default, AI is O
            return self.current_player == config.PLAYER_X
        return True

    def _is_ai_turn(self) -> bool:
        if self.mode != "HvsAI":
            return False
        return self.current_player == config.PLAYER_O

    def _post_move_update(self) -> None:
        self.winner, self.winning_line = self.board.check_winner()
        if not self.winner and not self.board.is_full():
            self.current_player = (
                config.PLAYER_O if self.current_player == config.PLAYER_X else config.PLAYER_X
            )

    def _cycle_difficulty(self) -> None:
        order = config.DIFFICULTIES
        try:
            idx = order.index(self.difficulty)
        except ValueError:
            idx = 0
        self.difficulty = order[(idx + 1) % len(order)]

    def _start_replay(self) -> None:
        # Reset board and play history moves at a fixed tempo
        self.board.reset()
        self.winner = None
        self.winning_line = None
        self.replaying = True
        self.replay_index = 0
        self._replay_last_ts = 0


