from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tic_tac_toe.logic.models import Grid, GameState, Mark

import re

from tic_tac_toe.logic.exceptions import InvalidGameState


def validate_grid(grid: Grid) -> None:
    if not re.match(r"^[\sXO]{9}$", grid.cells):
        raise ValueError("Grid must contain 9 cells of: X, O or Space")


def validate_game_state(game_state: GameState) -> None:
    validate_number_of_marks(game_state.grid)
    validate_starting_mark(game_state.grid, game_state.startingMark)
    validate_winner(
        game_state.grid,
        game_state.startingMark,
        game_state.winner
    )


def validate_number_of_marks(grid: Grid) -> None:
    if abs(grid.x_count - grid.o_count) > 1:
        raise InvalidGameState("Wrong number of Xs and Os on the grid")


def validate_starting_marks(grid: Grid, starting_mark: Mark) -> None:
    if grid.x_count > grid.o_count:
        if starting_mark != "X":
            raise InvalidGameState("Wrong starting Mark O")
    elif grid.x_count < grid.o_count:
        if starting_mark != "O":
            raise InvalidGameState("Wrong starting Mark X")


def validate_winner(
        grid: Grid,
        starting_mark: Mark,
        winner: Mark
) -> None:
    if winner == "X":
        if starting_mark == "X":
            if grid.x_count <= grid.o_count:
                raise InvalidGameState("Wrong number of Xs on the grid, num of Xs should be greater than num of Os")
        else:
            if grid.x_count != grid.o_count:
                raise InvalidGameState("Wrong number of Xs on the grid, num of Xs should be equal to num of Os")
    else:
        if starting_mark == "O":
            if grid.o_count <= grid.x_count:
                raise InvalidGameState("Wrong number of Os on the grid, num of Os should be greater than num of Xs")
        else:
            if grid.o_count != grid.x_count:
                raise InvalidGameState("Wrong number of Os on the grid, num of Os should be equal to num of Xs")
