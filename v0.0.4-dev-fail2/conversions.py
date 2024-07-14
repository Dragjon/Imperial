import chess

piece_to_index = {
    chess.PAWN : 0,
    chess.KNIGHT : 1,
    chess.BISHOP : 2,
    chess.ROOK : 3,
    chess.QUEEN : 4,
    chess.KING : 5
}

piece_to_score = {
    chess.PAWN : 100,
    chess.KNIGHT : 300,
    chess.BISHOP : 300,
    chess.ROOK : 500,
    chess.QUEEN : 900,
    chess.KING : 0
}

color_to_index = {
    chess.WHITE : 0,
    chess.BLACK : 1
}

def indextouci(index):
    row = index // 8 + 1
    col = index % 8

    col_letter = chr(ord('a') + col)

    uci_square = f"{col_letter}{row}"
    
    return uci_square