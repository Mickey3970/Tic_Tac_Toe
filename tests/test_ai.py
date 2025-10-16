from ttt.game import Board
from ttt import config
from ttt.ai import choose_move


def test_impossible_blocks_immediate_threat():
    b = Board()
    # X is human, O is AI. Create a board where X threatens to win next move.
    # X has two in a row, empty third cell.
    b.make_move(0, 0, config.PLAYER_X)
    b.make_move(0, 1, config.PLAYER_X)
    # O must block at (0,2)
    move = choose_move(b, config.PLAYER_O, difficulty="impossible")
    assert move == (0, 2)


