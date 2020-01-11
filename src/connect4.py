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
        self._last_move_connect4d = False
        self.winner = None

    def is_over(self):
        return self._last_move_connect4d or all(
            (len(column) == self.height) for column in self._columns
        )

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
            return (
                f"column needs to be between 0 and {self.width}, column is {column}: "
            )
        if not len(self._columns[column]) < (self.height - 1):
            return f"This piece can't be added to this column {column} since it is already full: "

    def play_move(self, piece, column):
        self.put_piece_in_column(piece=piece, column=column)
        if self._connect4(column=column, row=len(self._columns[column]) - 1):
            self._last_move_connect4d = True
            self.winner = piece

    def get_column_size(self, column):
        return len(self._columns[column])

    def get_piece_at_position(self, row, column):
        # is this redundant given this check is in is_valid_move?
        assert column in range(self.width) and row in range(
            self.height
        ), f"row and column needs to between (0, 0) and ({self.width}, {self.height}) but we have ({column}, {row})"
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


PIECE_TO_REPRESENTATION = {Piece.BLUE: "O", Piece.RED: "*", Piece.EMPTY: " "}


def draw_on_screen(
    game: Game, screen, current_player: Piece, error_msg: str = "", game_over=False
):
    screen.addstr(
        0, 0, f"CONNECT4!",
    )
    for column in range(game.width):
        for row in range(game.height):
            piece = game.get_piece_at_position(row=row, column=column)
            if PIECE_TO_REPRESENTATION[piece]:
                screen.addch(
                    game.height - row + 1, column * 2, PIECE_TO_REPRESENTATION[piece],
                )

    screen.addstr(
        game.height + 2,
        0,
        f"PROMPT: {PIECE_TO_REPRESENTATION[current_player]}'s move: select a column between 1 and {game.width}:".ljust(
            150
        ),
    )
    if error_msg:
        screen.addstr(
            game.height + 3,
            0,
            f"ERROR: Try again. You need to input an integer between 1 and {game.width}: ".ljust(
                100
            ),
        )
    if game_over:
        screen.addstr(
            game.height + 4,
            0,
            f"Game Over. {PIECE_TO_REPRESENTATION[current_player]} won!".ljust(100),
        )
        screen.addstr(
            game.height + 5,
            0,
            f"Type - 'q' to quit or any other key to restart".ljust(100),
        )
    screen.addstr(
        game.height + 6,
        0,
        f"type here: ",
    )
    screen.refresh()


def main(screen):
    while True:
        game = Game(width=6, height=7)
        screen.refresh()
        turns = cycle([Piece.BLUE, Piece.RED])
        while True:
            current_player = next(turns)
            draw_on_screen(game=game, screen=screen, current_player=current_player)

            # retry mechanism, move to a function?
            while True:
                try:
                    column = int(screen.getkey()) - 1
                except Exception:
                    draw_on_screen(
                        game=game,
                        screen=screen,
                        current_player=current_player,
                        error_msg=f"ERROR: Try again. You need to input an integer between 1 and {game.width}: ".ljust(
                            100
                        ),
                    )
                    continue
                invalid_message = game.is_valid_move(column=column)
                if invalid_message:
                    draw_on_screen(
                        game=game,
                        screen=screen,
                        current_player=current_player,
                        error_msg=f"ERROR: {invalid_message}".ljust(100),
                    )
                else:
                    break

            game.play_move(piece=current_player, column=column)
            if game.is_over():
                draw_on_screen(game=game, screen=screen, current_player=current_player, game_over=True)
                break
        inp = screen.getkey()
        if inp == "q":
            break
        else:
            continue
        break


if __name__ == "__main__":
    curses.wrapper(main)
