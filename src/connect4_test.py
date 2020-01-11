import pytest

from connect4 import Game, Piece


@pytest.mark.parametrize(
    ("description, height, width, piece, column"), [("basic", 2, 2, Piece.BLUE, 1),]
)
def test_game(description, height, width, piece, column):
    game = Game(height=height, width=width)
    game.put_piece_in_column(piece=piece, column=column)
    assert game._columns == [[], [piece]]


@pytest.mark.parametrize(
    ("description, height, width, piece, column"), [("basic", 2, 2, Piece.BLUE, 1),]
)
def test_game_too_full(description, height, width, piece, column):
    game = Game(height=height, width=width)
    game._columns = [[], [Piece.BLUE, Piece.RED]]
    with pytest.raises(Exception) as e:
        game.put_piece_in_column(piece=piece, column=column)
        assert (
            e.msg
            == f"This piece can't be added to this column {column} since it is already full"
        )


@pytest.mark.parametrize(
    ("description, height, width, piece, column"),
    [("basic", 2, 2, Piece.BLUE, 2), ("basic", 2, 2, Piece.BLUE, 3),],
)
def test_game_column_beyond_range(description, height, width, piece, column):
    game = Game(height=height, width=width)
    game._columns = [[], []]
    with pytest.raises(Exception) as e:
        game.put_piece_in_column(piece=piece, column=column)
        assert (
            e.msg
            == f"column needs to be between 0 and {game._width}, column is {column}"
        )


@pytest.mark.parametrize(
    ("description, row, column, piece"),
    [
        ("basic", 0, 0, Piece.EMPTY),
        ("basic", 0, 0, Piece.EMPTY),
        ("basic", 0, 1, Piece.BLUE),
        ("basic", 0, 2, Piece.RED),
        ("basic", 1, 2, Piece.BLUE),
        ("basic", 2, 2, Piece.EMPTY),
    ],
)
def test_game_piece_at_position(description, row, column, piece):
    game = Game(height=3, width=3)
    game._columns = [
        [],
        [Piece.BLUE],
        [Piece.RED, Piece.BLUE],
    ]
    assert game.get_piece_at_position(row=row, column=column) == piece


@pytest.mark.parametrize(
    ("description, column, size"), [("basic", 0, 0), ("basic", 1, 1), ("basic", 2, 2),]
)
def test_game_column_size(description, column, size):
    game = Game(height=3, width=3)
    game._columns = [
        [],
        [Piece.BLUE],
        [Piece.RED, Piece.BLUE],
    ]
    assert game.get_column_size(column=column) == size


@pytest.mark.parametrize(
    ("description, columns, row, column, connect4"),
    [
        (
            "basic",
            [[Piece.BLUE], [Piece.BLUE], [Piece.BLUE], [Piece.BLUE],],
            0,
            0,
            True,
        ),
        (
            "basic",
            [[Piece.BLUE, Piece.BLUE, Piece.BLUE, Piece.BLUE], [], [], [],],
            0,
            0,
            True,
        ),
        (
            "basic",
            [[Piece.BLUE, Piece.BLUE, Piece.BLUE, Piece.RED], [], [], [],],
            0,
            0,
            False,
        ),
    ],
)
def test_connect4(description, columns, row, column, connect4):
    game = Game(height=4, width=4)
    game._columns = columns
    assert game._connect4(column=0, row=0) is connect4
