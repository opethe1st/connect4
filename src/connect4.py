import curses
from enum import Enum
from itertools import cycle
from typing import List
from utils import connect_in_direction


class Piece(Enum):
    BLUE = 1
    RED = 2
    EMPTY = 3


class Game:
    "This is an instance of the connect4 game"

    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width
        #  this is represented internally column-wise because the pieces fall column wise
        self._columns: List[List[Piece]] = [[] for _ in range(width)]
        self._game_over = False
        self.winner = None

    def is_over(self):
        # TODO(ope): also should be game over if there are no moves left to play
        return self._game_over

    def _connect4(self, column, row):
        return any(
            [
                connect_in_direction(
                    game=self, start=(row, column), direction=(-1, -1)
                ),
                connect_in_direction(game=self, start=(row, column), direction=(-1, 1)),
                connect_in_direction(game=self, start=(row, column), direction=(-1, 0)),
                connect_in_direction(game=self, start=(row, column), direction=(0, -1)),
            ]
        )

    def is_valid_move(self, column):
        if column not in range(self.width):
            return f"column needs to be between 0 and {self.width}, column is {column}: "
        if not len(self._columns[column]) < (self.height - 1):
            return f"This piece can't be added to this column {column} since it is already full: "

    def play_move(self, piece, column):
        self.put_piece_in_column(piece=piece, column=column)
        if self._connect4(column=column, row=len(self._columns[column]) - 1):
            self._game_over = True
            self.winner = piece

    def get_column_size(self, column):
        return len(self._columns[column])

    def get_piece_at_position(self, row, column):
        # is this redundant given this check is in is_valid_move?
        assert (column, row) < (
            self.width,
            self.height,
        ), f"x and y needs to between (0, 0) and ({self.width}, {self.height}) but we have ({column}, {row})"
        if row < len(self._columns[column]):
            return self._columns[column][row]
        else:
            return Piece.EMPTY

    def put_piece_in_column(self, piece: Piece, column: int):
        # is this redundant given this check is in is_valid_move?
        assert column in range(
            self.width
        ), f"column needs to be between 0 and {self.width}, column is {column}"
        if len(self._columns[column]) < (self.height - 1):
            self._columns[column].append(piece)
        else:
            raise Exception(
                f"This piece can't be added to this column {column} since it is already full"
            )


PIECE_TO_REPRESENTATION = {Piece.BLUE: "🔵", Piece.RED: "🔴", Piece.EMPTY: None}


PIECE_TO_NAME = {
    Piece.BLUE: "Blue",
    Piece.RED: "Red",
}


def draw_on_screen(game: Game, screen):
    for y in range(game.width):
        for x in range(game.height):
            piece = game.get_piece_at_position(row=x, column=y)
            if PIECE_TO_REPRESENTATION[piece]:
                screen.addch(
                    game.height - x,
                    y * 3,
                    PIECE_TO_REPRESENTATION[piece],
                    curses.color_pair(piece.value),
                )


def main(screen):
    game = Game(width=6, height=7)

    turns = cycle([Piece.BLUE, Piece.RED])
    while True:
        current_player = next(turns)
        draw_on_screen(game=game, screen=screen)
        screen.addstr(
            game.height + 2,
            0,
            f"{PIECE_TO_NAME[current_player]}'s move: select a column between 1 and {game.width}: ",
        )
        screen.refresh()

        # retry mechanism, move to a function?
        while True:
            try:
                column = int(screen.getkey()) - 1
            except Exception:
                screen.addstr(
                    game.height + 1,
                    0,
                    f"Try again. You need to input an integer between 1 and {game.width}: ",
                )
                continue
            invalid_message = game.is_valid_move(column=column)
            if invalid_message:
                screen.addstr(
                    game.height + 1,
                    0,
                    invalid_message,
                )
            else:
                break

        game.play_move(piece=current_player, column=column)
        if game.is_over():
            screen.clear()
            draw_on_screen(game=game, screen=screen)
            screen.addstr(
                game.height + 2, 0, f"Game Over. {PIECE_TO_NAME[current_player]} won!"
            )
            screen.refresh()
            break

    screen.getch()


if __name__ == "__main__":
    curses.wrapper(main)
