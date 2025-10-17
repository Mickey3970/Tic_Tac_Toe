# Tic-Tac-Toe (pygame, MVC-like)

A minimalist Tic-Tac-Toe desktop game built with pygame, structured with a clean, testable, MVC-like architecture. Includes an AI using minimax with alpha-beta pruning, difficulty levels, replay, keyboard and mouse input, and a small HUD.

## Features

- Human vs Human (HvsH) and Human vs AI (HvsAI)
- AI difficulties: easy, medium, impossible (optimal)
- Minimax with alpha-beta pruning and move ordering (center → corners → sides)
- Replay finished game step-by-step
- Change difficulty in-game (button or press `D`)
- Keyboard support: arrows to move selection, Enter/Space to place; `R` to restart; `Esc`/`Q` to quit
- Minimalist UI with hover highlight and win-line animation
- Unit tests for logic and AI behavior

## Requirements

- Python 3.10+
- pygame, pytest

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the game

```bash
python main.py --mode HvsAI --difficulty impossible
```

CLI options:

- `--mode` one of: `HvsH`, `HvsAI` (default: `HvsAI`)
- `--difficulty` one of: `easy`, `medium`, `impossible` (default: `impossible`)

You can change difficulty during the game via the on-screen button or press `D`.

## Controls

- Mouse: click a cell to place; click Restart; click Replay; click Difficulty
- Keyboard:
  - Arrow keys: move selection
  - Enter/Space: place mark in selected cell
  - `R`: restart
  - `D`: cycle difficulty
  - `Esc` or `Q`: quit

## Replay

After a game ends (win or draw), click the Replay button to watch the moves unfold at a fixed tempo. Replay is non-blocking and uses stored move history.

## Tests

Run tests:

```bash
python -m pytest -q
```

Tests cover game winner detection and a critical AI behavior (impossible AI blocks an immediate threat).

## Project structure

```
Tic_Tac_Toe/
  main.py                # CLI entry point
  requirements.txt
  ttt/
    __init__.py          # package export convenience
    config.py            # constants: layout, colors, gameplay
    utils.py             # helpers (move ordering, RNG seed)
    game.py              # pure game logic (testable, no pygame)
    ai.py                # AI: minimax + alpha-beta; difficulty routing
    controller.py        # game loop orchestration, turn order, replay
    ui.py                # pygame rendering & input, HUD, animations
  tests/
    __init__.py
    test_game.py         # winner detection
    test_ai.py           # impossible AI blocks threat
```

## Architecture overview

- `ttt.game.Board` stores the game state and exposes pure logic (reset, make_move, legal_moves, check_winner, is_full, copy). It’s framework-agnostic and unit-testable.
- `ttt.ai` implements minimax with alpha-beta pruning. Terminal scores: X win = +1, O win = -1, draw = 0 (X’s perspective). Move ordering accelerates pruning. Difficulty levels adjust randomness and depth; impossible is optimal. Immediate win/block short-circuits ensure correct tactics.
- `ttt.controller.GameController` coordinates the loop: gets inputs from the UI, applies moves, calls AI when needed, maintains move history, and runs replay.
- `ttt.ui.GameUI` draws everything with pygame, handles mouse/keyboard, shows HUD, buttons (Restart, Replay, Difficulty), hover highlight, and win-line animation.

## Notes

- Fonts use `pygame.font.SysFont` with system-available families; no external assets.
- The code aims for clarity and maintainability with small, documented functions.


