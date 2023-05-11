from __future__ import annotations
import enum
import re
from dataclasses import dataclass
from functools import cached_property
from tic_tac_toe.logic.validators import validate_game_state, validate_grid


WINNING_PATTERNS = (
    "???......",
    "...???...",
    "......???",
    "?..?..?..",
    ".?..?..?.",
    "..?..?..?",
    "?...?...?",
    "..?.?.?..",
)

# TicTacToe Domain models 
class Mark(str, enum.Enum):
    CROSS = "X"
    NAUGHT = "O"

    @property
    def other(self) -> "Mark":
        return Mark.CROSS if self is Mark.NAUGHT else Mark.NAUGHT


@dataclass(frozen=True)
class Grid:
    cells: str= " " * 9 

    def __post_init__(self) -> None:
        validate_grid(self)
    
    @cached_property
    def x_count(self) -> int:
        return self.cells.count("X")

    @cached_property
    def o_count(self) -> int:
        return self.cells.count("O")

    @cached_property
    def empty_count(self) -> int:
        return self.cells.count(" ")


# DTO to carry the data of the different game phases 
@dataclass(frozen=True)
class Move:
    mark: Mark
    cellIndex: int
    beforeState: "GameState"
    afterState: "GameState"


@dataclass(frozen=True)
class GameState:
    grid: Grid
    startingMark: Mark = Mark.CROSS

    def __post_init__(self):
        validate_game_state(self)

    @cached_property
    def current_mark(self) -> Mark:
        if self.grid.o_count == self.grid.x_count :
            return self.startingMark
        else :
            return self.startingMark.other
    
    @cached_property
    def game_not_started(self) -> bool:
        return self.grid.empty_count == 9
    
    @cached_property
    def game_over(self) -> bool :
        return self.winner is not None or self.tie
    
    @cached_property
    def tie(self) -> bool :
        return self.winner is None and self.grid.empty_count==0
    
    @cached_property
    def winner(self) -> Mark | None :
        for pattern in WINNING_PATTERNS :
            for mark in Mark :
                if re.match(pattern.replace("?", mark), self.grid.cells) :
                    return mark
        return None

    @cached_property
    def winning_cells(self) -> list[int] :
        for pattern in WINNING_PATTERNS :
            for mark in Mark :
                if re.match(pattern.replace("?", mark), self.grid.cells) :
                    return [
                        match.start()
                        for match in re.finditer(r"\?", pattern)
                    ]
        return []