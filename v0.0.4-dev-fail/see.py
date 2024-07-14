import chess
from conversions import piece_to_score, indextouci

def getallattackers(board, square):
    legals = board.legal_moves
    attackers = []
    from_squares = []
    for move in legals:
        if move.to_square == square: # We don't count en passants just because
            attackers.append(board.piece_at(move.to_square))
            from_squares.append(move.from_square)
    return attackers, from_squares

def lva(board, square):
    attackers, from_squares = getallattackers(board, square)
    sorted_attackers = sorted(attackers, key = lambda p: piece_to_score[p.piece_type]) if len(attackers) != 0 else None
    lvp = False if sorted_attackers is None else sorted_attackers[0]
    from_square = False if len(from_squares) == 0 else from_squares[0]
    return lvp, from_square


def see(seeBoard, square, debug = False):
    value = 0
    lvp, from_square = lva(seeBoard, square)
    if lvp:
      piece_just_captured = seeBoard.piece_at(square)
      if debug:
        print(piece_just_captured)
      if lvp.piece_type == chess.PAWN and (square - 7 < 1 or square + 7 > 62):
        # Capture with promotion, always promote to queen
        seeBoard.push(chess.Move.from_uci(indextouci(from_square) + indextouci(square) + "q"))
        value = max(0, piece_to_score[chess.QUEEN] - piece_to_score[chess.PAWN] + piece_to_score[piece_just_captured.piece_type] -see(seeBoard, square))

      else:
        seeBoard.push(chess.Move.from_uci(indextouci(from_square) + indextouci(square)))
        value = max(0, piece_to_score[piece_just_captured.piece_type] -see(seeBoard, square))

      seeBoard.pop()
      lvp, from_square = lva(seeBoard, square)
    return value


def seecapture(seeBoard, move, debug = False):
    value = 0
    piece = seeBoard.piece_at(move.from_square)
    piece_just_captured = seeBoard.piece_at(move.to_square)
    if debug:
        print(piece_just_captured)  
    if piece.piece_type == chess.PAWN and (move.to_square - 7 < 1 or move.to_square + 7 > 62):
        # Capture with promotion, always promote to queen
        seeBoard.push(chess.Move.from_uci(indextouci(move.from_square) + indextouci(move.to_square) + "q"))
        value = piece_to_score[chess.QUEEN] - piece_to_score[chess.PAWN] + piece_to_score[piece_just_captured.piece_type] -see(seeBoard, move.to_square, debug = debug)

    else:
        seeBoard.push(chess.Move.from_uci(indextouci(move.from_square) + indextouci(move.to_square)))
        value = piece_to_score[piece_just_captured.piece_type] -see(seeBoard, move.to_square, debug = debug)

    seeBoard.pop()
    return value