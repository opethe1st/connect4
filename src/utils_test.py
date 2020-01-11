from connect4 import Game, Piece
from utils import _generate_sequence, connect_in_direction


def test_generate_sequence():
    sequence = _generate_sequence(start=(0, 0), direction=(1, 1), maximum=(3, 3))
    assert list(sequence) == [(1, 1), (2, 2)]

    sequence = _generate_sequence(start=(0, 0), direction=(1, 0), maximum=(3, 3))
    assert list(sequence) == [(1, 0), (2, 0)]


def test_connect_in_direction():
    game = Game(height=4, width=4)
    game._columns = [
        [],
        [Piece.BLUE],
        [Piece.BLUE, Piece.BLUE, Piece.BLUE, Piece.BLUE],
        [],
    ]
    assert connect_in_direction(game=game, start=(0, 2), direction=(1, 0))

    game = Game(height=4, width=4)
    game._columns = [
        [Piece.BLUE],
        [Piece.BLUE, Piece.BLUE],
        [Piece.BLUE, Piece.BLUE, Piece.BLUE],
        [Piece.BLUE, Piece.BLUE, Piece.BLUE, Piece.BLUE],
    ]
    assert connect_in_direction(game=game, start=(2, 2), direction=(1, 1))

    game = Game(height=4, width=4)
    game._columns = [
        [Piece.BLUE, Piece.BLUE, Piece.BLUE, Piece.BLUE],
        [Piece.BLUE, Piece.BLUE, Piece.BLUE],
        [Piece.BLUE, Piece.BLUE],
        [Piece.BLUE],
    ]
    assert connect_in_direction(game=game, start=(0, 3), direction=(1, -1))
