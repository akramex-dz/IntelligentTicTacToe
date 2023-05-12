from functools import partial

from tic_tac_toe.logic.models import GameState, Mark, Move


def find_best_move(game_state: GameState) -> Move | None:
    maximizer: Mark = game_state.current_mark
    bound_minimax = partial(minimax, maximizer=maximizer)
    return max(game_state.possible_moves, key=bound_minimax)


def minimax(
    move: Move, maximizer: Mark, choose_highest_score: bool = False
) -> int:
    if move.afterState.game_over:
        return move.afterState.evaluate_score(maximizer)
    return (max if choose_highest_score else min)(
        minimax(next_move, maximizer, not choose_highest_score)
        for next_move in move.afterState.possible_moves
    )
