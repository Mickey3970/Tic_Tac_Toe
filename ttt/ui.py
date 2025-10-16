"""ui.py
Pygame-based rendering and input handling.

Provides a minimalist aesthetic with a central board, subtle colors, and small
HUD. Supports mouse and keyboard (arrows + Enter) input, hover highlight, and
win line animation.
"""

from __future__ import annotations

import time
from typing import Dict, Optional, Tuple

import pygame

from . import config


class GameUI:
    """Handle all drawing and user event processing."""

    def __init__(self, board, mode: str, difficulty: str) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("Tic-Tac-Toe")
        self.font_hud = pygame.font.SysFont(config.FONT_NAME, config.FONT_SIZE_HUD)
        self.font_btn = pygame.font.SysFont(config.FONT_NAME, config.FONT_SIZE_BUTTON)

        self.mode = mode
        self.difficulty = difficulty
        self.board = board
        self.selector = [0, 0]  # keyboard-controlled selection
        self.last_hover_change = 0.0
        self.win_anim_start: Optional[float] = None

        self._compute_layout()

    def _compute_layout(self) -> None:
        n = config.BOARD_SIZE
        # Compute board rect to fit within margins and maintain square
        width = config.SCREEN_WIDTH - 2 * config.MARGIN
        height = config.SCREEN_HEIGHT - 2 * config.MARGIN - 80  # reserve HUD
        size = min(width, height)
        self.board_rect = pygame.Rect(
            (config.SCREEN_WIDTH - size) // 2,
            config.MARGIN + 40,  # below HUD line
            size,
            size,
        )
        self.cell_size = self.board_rect.width // n
        # Restart button
        self.restart_rect = pygame.Rect(
            config.MARGIN,
            config.SCREEN_HEIGHT - 40,
            120,
            28,
        )
        # Replay and difficulty buttons
        self.replay_rect = pygame.Rect(
            self.restart_rect.right + 10,
            config.SCREEN_HEIGHT - 40,
            100,
            28,
        )
        self.diff_rect = pygame.Rect(
            self.replay_rect.right + 10,
            config.SCREEN_HEIGHT - 40,
            170,
            28,
        )

    def on_reset(self) -> None:
        self.selector = [0, 0]
        self.win_anim_start = None

    def handle_events(self) -> Dict[str, Optional[Tuple[int, int]]]:
        """Process pygame events and return an action dict.

        Keys in the returned dict:
        - "quit": bool
        - "restart": bool
        - "place": Optional[(row, col)] if user places a mark
        """
        action = {"quit": False, "restart": False, "place": None, "replay": False, "toggle_difficulty": False}

        mouse_pos = pygame.mouse.get_pos()
        hovering_cell = self._cell_at(mouse_pos)
        if hovering_cell != tuple(self.selector):
            self.last_hover_change = time.time()
        if hovering_cell is not None:
            self.selector = [hovering_cell[0], hovering_cell[1]]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                action["quit"] = True
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    action["quit"] = True
                elif event.key == pygame.K_r:
                    action["restart"] = True
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if self._inside_selection() and self._selection_empty():
                        action["place"] = (self.selector[0], self.selector[1])
                elif event.key == pygame.K_UP:
                    self.selector[0] = max(0, self.selector[0] - 1)
                elif event.key == pygame.K_DOWN:
                    self.selector[0] = min(config.BOARD_SIZE - 1, self.selector[0] + 1)
                elif event.key == pygame.K_LEFT:
                    self.selector[1] = max(0, self.selector[1] - 1)
                elif event.key == pygame.K_RIGHT:
                    self.selector[1] = min(config.BOARD_SIZE - 1, self.selector[1] + 1)
                elif event.key == pygame.K_d:
                    action["toggle_difficulty"] = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.restart_rect.collidepoint(mouse_pos):
                    action["restart"] = True
                elif self.replay_rect.collidepoint(mouse_pos):
                    action["replay"] = True
                elif self.diff_rect.collidepoint(mouse_pos):
                    action["toggle_difficulty"] = True
                else:
                    cell = self._cell_at(mouse_pos)
                    if cell is not None and self.board.grid[cell[0]][cell[1]] is config.EMPTY:
                        action["place"] = cell
        return action

    def render(self, board, current_player, winner, winning_line) -> None:
        self.screen.fill(config.COLOR_BACKGROUND)
        self._draw_hud(current_player)
        self._draw_board(board)
        self._draw_symbols(board)
        if winner and winning_line:
            self._draw_win_line(winning_line)
        pygame.display.flip()

    # Drawing helpers
    def _draw_hud(self, current_player: str) -> None:
        text = f"Mode: {self.mode}   Difficulty: {self.difficulty}   Turn: {current_player}"
        surf = self.font_hud.render(text, True, config.COLOR_ACCENT)
        self.screen.blit(surf, (config.MARGIN, config.MARGIN))

        # Restart button
        pygame.draw.rect(self.screen, config.COLOR_RESTART_BG, self.restart_rect, border_radius=6)
        btn_text = self.font_btn.render("Restart (R)", True, config.COLOR_ACCENT)
        self.screen.blit(btn_text, (self.restart_rect.x + 10, self.restart_rect.y + 5))
        # Replay button
        pygame.draw.rect(self.screen, config.COLOR_RESTART_BG, self.replay_rect, border_radius=6)
        r_text = self.font_btn.render("Replay", True, config.COLOR_ACCENT)
        self.screen.blit(r_text, (self.replay_rect.x + 10, self.replay_rect.y + 5))
        # Difficulty toggle button
        pygame.draw.rect(self.screen, config.COLOR_RESTART_BG, self.diff_rect, border_radius=6)
        d_text = self.font_btn.render("Difficulty (D)", True, config.COLOR_ACCENT)
        self.screen.blit(d_text, (self.diff_rect.x + 10, self.diff_rect.y + 5))

    def _draw_board(self, board) -> None:
        n = config.BOARD_SIZE
        # Grid lines
        for i in range(1, n):
            # Vertical
            x = self.board_rect.x + i * self.cell_size
            pygame.draw.line(self.screen, config.COLOR_GRID, (x, self.board_rect.top), (x, self.board_rect.bottom), config.GRID_LINE_WIDTH)
            # Horizontal
            y = self.board_rect.y + i * self.cell_size
            pygame.draw.line(self.screen, config.COLOR_GRID, (self.board_rect.left, y), (self.board_rect.right, y), config.GRID_LINE_WIDTH)

        # Hover / selection highlight
        if self._inside_selection():
            r, c = self.selector
            rect = self._cell_rect(r, c)
            pygame.draw.rect(self.screen, config.COLOR_HOVER, rect, width=config.HOVER_THICKNESS, border_radius=6)

    def _draw_symbols(self, board) -> None:
        n = config.BOARD_SIZE
        pad = self.cell_size // 5
        for r in range(n):
            for c in range(n):
                val = board.grid[r][c]
                if val == config.PLAYER_X:
                    rect = self._cell_rect(r, c)
                    x1 = (rect.left + pad, rect.top + pad)
                    x2 = (rect.right - pad, rect.bottom - pad)
                    y1 = (rect.left + pad, rect.bottom - pad)
                    y2 = (rect.right - pad, rect.top + pad)
                    pygame.draw.line(self.screen, config.COLOR_X, x1, x2, config.SYMBOL_STROKE_WIDTH)
                    pygame.draw.line(self.screen, config.COLOR_X, y1, y2, config.SYMBOL_STROKE_WIDTH)
                elif val == config.PLAYER_O:
                    rect = self._cell_rect(r, c)
                    center = (rect.centerx, rect.centery)
                    radius = (self.cell_size // 2) - pad
                    pygame.draw.circle(self.screen, config.COLOR_O, center, radius, config.SYMBOL_STROKE_WIDTH)

    def _draw_win_line(self, winning_line) -> None:
        # Animate line drawing based on time since win
        if self.win_anim_start is None:
            self.win_anim_start = time.time()
        t = (time.time() - self.win_anim_start) * 1000.0
        progress = min(1.0, t / config.WIN_LINE_ANIM_MS)

        start_cell = winning_line[0]
        end_cell = winning_line[-1]
        p1 = self._cell_rect(*start_cell).center
        p2 = self._cell_rect(*end_cell).center
        # Interpolate end point for animation
        ex = p1[0] + (p2[0] - p1[0]) * progress
        ey = p1[1] + (p2[1] - p1[1]) * progress
        pygame.draw.line(self.screen, config.COLOR_ACCENT, p1, (ex, ey), config.WIN_LINE_THICKNESS)

    # Geometry helpers
    def _cell_rect(self, row: int, col: int) -> pygame.Rect:
        return pygame.Rect(
            self.board_rect.x + col * self.cell_size + 6,
            self.board_rect.y + row * self.cell_size + 6,
            self.cell_size - 12,
            self.cell_size - 12,
        )

    def _cell_at(self, pos) -> Optional[Tuple[int, int]]:
        if not self.board_rect.collidepoint(pos):
            return None
        rel_x = pos[0] - self.board_rect.x
        rel_y = pos[1] - self.board_rect.y
        c = rel_x // self.cell_size
        r = rel_y // self.cell_size
        if 0 <= r < config.BOARD_SIZE and 0 <= c < config.BOARD_SIZE:
            return (r, c)
        return None

    def _inside_selection(self) -> bool:
        r, c = self.selector
        return 0 <= r < config.BOARD_SIZE and 0 <= c < config.BOARD_SIZE

    def _selection_empty(self) -> bool:
        r, c = self.selector
        return self.board.grid[r][c] is config.EMPTY

    # External setters
    def set_difficulty(self, difficulty: str) -> None:
        """Update the UI's difficulty label."""
        self.difficulty = difficulty


