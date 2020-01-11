import curses
from enum import Enum
from itertools import cycle
from typing import List


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

    def get_column_size(self, column):
        return len(self._columns[column])

    def get_piece_at_position(self, row, column):
        # I should probably add a guard condition here to make sure that we have useful errors if x and y are out of band
        assert (column, row) < (self.height, self.width), f"x and y needs to between (0, 0) and ({self.height}, {self.width})"
        if row < len(self._columns[column]):
            return self._columns[column][row]
        else:
            return Piece.EMPTY

    def put_piece_in_column(self, piece: Piece, column: int):
        assert column in range(self.width), f"column needs to be between 0 and {self.width}, column is {column}"
        # need to make sure that self._columns is not greater than column length here
        if len(self._columns[column]) < (self.height - 1):
            self._columns[column].append(piece)
        else:
            raise Exception(f"This piece can't be added to this column {column} since it is already full")


PIECE_TO_REPRESENTATION = {
    Piece.BLUE: "X",
    Piece.RED: "O",
    Piece.EMPTY: " "
}

PIECE_TO_NAME = {
    Piece.BLUE: "Blue",
    Piece.RED: "Red",
}


def draw_on_screen(game: Game, screen):
    for y in range(game.width):
        for x in range(game.height):
            piece = game.get_piece_at_position(row=x, column=y)
            # seems color doesn't work for addch. Tragic!
            screen.addch(game.height - x, y, PIECE_TO_REPRESENTATION[piece], curses.color_pair(piece.value))


def main(screen):
    curses.start_color()
    game = Game(width=6, height=7)

    turns = cycle([Piece.BLUE, Piece.RED])
    while True:
        current_player = next(turns)
        draw_on_screen(game=game, screen=screen)
        # should make this more user friendly by making it between 1 and 6.
        screen.addstr(game.height + 1, 0, f"{PIECE_TO_NAME[current_player]}'s move: select a column between 1 and {game.width}: ")
        screen.refresh()
        column = int(screen.getkey()) - 1
        # need to be able to recover from errors here. tell player to try again.
        game.put_piece_in_column(piece=current_player, column=column)


if __name__ == "__main__":
    curses.wrapper(main)
