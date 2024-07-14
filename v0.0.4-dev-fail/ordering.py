import chess
from mvvlva import mvvlvaTable
from conversions import piece_to_index
from see import see

def orderwithquiets(board, moves, move_in_tt, killers, ply, counters, parent_move, history):
    tt = []
    good_captures = []
    quiets = []
    bad_captures = []

    for move in moves:
        if move == move_in_tt:
            tt.append(move)
        elif board.piece_at(move.to_square) is not None:
            see_value = see(board, move)
            if see_value >= 0:
                good_captures.append(move)
            else:
                bad_captures.append(move)
        else:
            quiets.append(move)

    good_captures = sorted(good_captures, key = lambda move: mvvlvaTable[piece_to_index[board.piece_at(move.from_square).piece_type]][piece_to_index[board.piece_at(move.from_square).piece_type]])   
    bad_captures = sorted(bad_captures, key = lambda move: mvvlvaTable[piece_to_index[board.piece_at(move.from_square).piece_type]][piece_to_index[board.piece_at(move.from_square).piece_type]])   
    quiets = sorted(quiets, key = lambda move: 
                    10_000_000 if move == killers[ply] else
                    1_000_000 if move == counters[parent_move.from_square][parent_move.to_square] else
                    history[move.from_square][move.to_square], reverse=True)
    return tt + good_captures + quiets + bad_captures

def ordercaptures(board, moves, move_in_tt):
    tt = []
    good_captures = []
    bad_captures = []
    for move in moves:
        if move == move_in_tt:
            tt.append(move)
        else:
            see_value = see(board, move)
            if see_value >= 0:
                good_captures.append(move)
            else:
                bad_captures.append(move)

    good_captures = sorted(good_captures, key = lambda move: mvvlvaTable[piece_to_index[board.piece_at(move.from_square).piece_type]][piece_to_index[board.piece_at(move.from_square).piece_type]])   
    bad_captures = sorted(bad_captures, key = lambda move: mvvlvaTable[piece_to_index[board.piece_at(move.from_square).piece_type]][piece_to_index[board.piece_at(move.from_square).piece_type]])   

    return tt + good_captures + bad_captures