import chess
from conversions import piece_to_index, color_to_index
from evaldefs import tempo, mg_table, eg_table, mg_value, eg_value, gamephaseInc

def eval(board):
    mg = [0, 0]
    eg = [0, 0]
    gamePhase = 0
    side2move = 0 if board.turn == chess.WHITE else 1
    otherside2move = side2move ^ 1

    for square in range(64):
        pc : chess.Piece = board.piece_at(square)
        if pc != None:
            pc_type = piece_to_index[pc.piece_type]
            color = color_to_index[pc.color]
            square = square ^ 56 if color == 0 else square
            mg[color] += mg_table[pc_type][square] + mg_value[pc_type]
            eg[color] += eg_table[pc_type][square] + eg_value[pc_type]
            gamePhase += gamephaseInc[pc_type]

    mgScore = mg[side2move] - mg[otherside2move]
    egScore = eg[side2move] - eg[otherside2move]
    mgPhase = gamePhase

    if mgPhase > 24:
        mgPhase = 24

    egPhase = 24 - mgPhase
    return tempo + (mgScore * mgPhase + egScore * egPhase) / 24