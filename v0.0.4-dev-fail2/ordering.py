import chess
from mvvlva import mvvlvaTable
from conversions import piece_to_index

def orderwithquiets(board, moves, move_in_tt, killers, ply, counters, parent_move, history):
    return sorted(list(moves), key=lambda move: 
                    1_000_000_000 if move == move_in_tt else 
                    mvvlvaTable[piece_to_index[board.piece_at(move.from_square).piece_type]][piece_to_index[board.piece_at(move.from_square).piece_type]] if board.is_capture(move) else 
                    10_000_000 if move == killers[ply] else
                    1_000_000 if move == counters[parent_move.from_square][parent_move.to_square] else
                    history[move.from_square][move.to_square], reverse=True)

def ordercaptures(board, moves, move_in_tt):
    return sorted(moves, key = lambda move: 1_000_000_000 if move == move_in_tt else mvvlvaTable[piece_to_index[board.piece_at(move.from_square).piece_type]][piece_to_index[board.piece_at(move.from_square).piece_type]])   