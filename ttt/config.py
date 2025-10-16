"""config.py
Centralized configuration and constants for the Tic-Tac-Toe project.

This module intentionally keeps only data/constants and no pygame imports so it
is lightweight and easy to import from anywhere.
"""

# Board and window configuration
BOARD_SIZE = 3  # scalable; other sizes like 4+ will still render
SCREEN_WIDTH = 520
SCREEN_HEIGHT = 640  # leave room for a small HUD

# Layout and drawing settings
MARGIN = 30  # outer margin around the board
GRID_LINE_WIDTH = 6
SYMBOL_STROKE_WIDTH = 10
HOVER_THICKNESS = 4
WIN_LINE_THICKNESS = 10

# Animation timings (in milliseconds)
HOVER_FADE_MS = 120
WIN_LINE_ANIM_MS = 450
REPLAY_STEP_MS = 450  # time between moves when replaying

# Colors (minimalist palette)
COLOR_BACKGROUND = (245, 246, 250)  # light grayish
COLOR_GRID = (200, 205, 210)        # soft grid
COLOR_X = (55, 66, 250)             # calm blue
COLOR_O = (230, 70, 70)             # soft red
COLOR_ACCENT = (90, 100, 110)       # for HUD text/buttons
COLOR_HOVER = (180, 190, 200)       # subtle hover highlight
COLOR_RESTART_BG = (230, 233, 238)

# Fonts (use system fonts via pygame.font.SysFont)
FONT_NAME = "Segoe UI"
FONT_SIZE_HUD = 20
FONT_SIZE_BUTTON = 18

# Gameplay constants
PLAYER_X = "X"
PLAYER_O = "O"
EMPTY = None

# Supported modes and difficulties
MODES = {
    "HvsH": "Human vs Human",
    "HvsAI": "Human vs AI",
}

DIFFICULTIES = ["easy", "medium", "impossible"]


