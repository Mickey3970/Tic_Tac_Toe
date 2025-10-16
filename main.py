"""
How to run:
  1) Install requirements: pip install -r requirements.txt
  2) Run the game:
       python main.py --mode HvsAI --difficulty impossible
     Or:
       python main.py --mode HvsH

This file is the entry point and CLI for selecting the game mode and AI
difficulty. It imports the package modules using `from ttt import ...` as
requested.
"""

import argparse

from ttt import config
from ttt.controller import GameController


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for mode and difficulty."""
    parser = argparse.ArgumentParser(description="Tic-Tac-Toe with pygame and minimax AI")
    parser.add_argument(
        "--mode",
        choices=list(config.MODES.keys()),
        default="HvsAI",
        help="Choose game mode",
    )
    parser.add_argument(
        "--difficulty",
        choices=config.DIFFICULTIES,
        default="impossible",
        help="AI difficulty (only used in HvsAI)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    controller = GameController(mode=args.mode, difficulty=args.difficulty)
    controller.run()


if __name__ == "__main__":
    main()


