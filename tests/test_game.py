from ttt.game import Board
from ttt import config


def test_check_winner_rows_cols_diags():
    b = Board()

    # Row win
    b.make_move(0, 0, config.PLAYER_X)
    b.make_move(0, 1, config.PLAYER_X)
    b.make_move(0, 2, config.PLAYER_X)
    w, line = b.check_winner()
    assert w == config.PLAYER_X
    assert set(line) == {(0, 0), (0, 1), (0, 2)}

    b.reset()
    # Col win
    b.make_move(0, 1, config.PLAYER_O)
    b.make_move(1, 1, config.PLAYER_O)
    b.make_move(2, 1, config.PLAYER_O)
    w, line = b.check_winner()
    assert w == config.PLAYER_O
    assert set(line) == {(0, 1), (1, 1), (2, 1)}

    b.reset()
    # Diagonal win
    b.make_move(0, 0, config.PLAYER_X)
    b.make_move(1, 1, config.PLAYER_X)
    b.make_move(2, 2, config.PLAYER_X)
    w, line = b.check_winner()
    assert w == config.PLAYER_X
    assert set(line) == {(0, 0), (1, 1), (2, 2)}


