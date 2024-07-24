import chess
import chess.polyglot
import math
import time

mg_value = (82, 337, 365, 477, 1025,  0)
eg_value = (94, 281, 297, 512,  936,  0)

mg_pawn_table = (
      0,   0,   0,   0,   0,   0,  0,   0,
     98, 134,  61,  95,  68, 126, 34, -11,
     -6,   7,  26,  31,  65,  56, 25, -20,
    -14,  13,   6,  21,  23,  12, 17, -23,
    -27,  -2,  -5,  12,  17,   6, 10, -25,
    -26,  -4,  -4, -10,   3,   3, 33, -12,
    -35,  -1, -20, -23, -15,  24, 38, -22,
      0,   0,   0,   0,   0,   0,  0,   0,
)

eg_pawn_table = (
      0,   0,   0,   0,   0,   0,   0,   0,
    178, 173, 158, 134, 147, 132, 165, 187,
     94, 100,  85,  67,  56,  53,  82,  84,
     32,  24,  13,   5,  -2,   4,  17,  17,
     13,   9,  -3,  -7,  -7,  -8,   3,  -1,
      4,   7,  -6,   1,   0,  -5,  -1,  -8,
     13,   8,   8,  10,  13,   0,   2,  -7,
      0,   0,   0,   0,   0,   0,   0,   0,
)

mg_knight_table = (
    -167, -89, -34, -49,  61, -97, -15, -107,
     -73, -41,  72,  36,  23,  62,   7,  -17,
     -47,  60,  37,  65,  84, 129,  73,   44,
      -9,  17,  19,  53,  37,  69,  18,   22,
     -13,   4,  16,  13,  28,  19,  21,   -8,
     -23,  -9,  12,  10,  19,  17,  25,  -16,
     -29, -53, -12,  -3,  -1,  18, -14,  -19,
    -105, -21, -58, -33, -17, -28, -19,  -23,
)

eg_knight_table = (
    -58, -38, -13, -28, -31, -27, -63, -99,
    -25,  -8, -25,  -2,  -9, -25, -24, -52,
    -24, -20,  10,   9,  -1,  -9, -19, -41,
    -17,   3,  22,  22,  22,  11,   8, -18,
    -18,  -6,  16,  25,  16,  17,   4, -18,
    -23,  -3,  -1,  15,  10,  -3, -20, -22,
    -42, -20, -10,  -5,  -2, -20, -23, -44,
    -29, -51, -23, -15, -22, -18, -50, -64,
)

mg_bishop_table = (
    -29,   4, -82, -37, -25, -42,   7,  -8,
    -26,  16, -18, -13,  30,  59,  18, -47,
    -16,  37,  43,  40,  35,  50,  37,  -2,
     -4,   5,  19,  50,  37,  37,   7,  -2,
     -6,  13,  13,  26,  34,  12,  10,   4,
      0,  15,  15,  15,  14,  27,  18,  10,
      4,  15,  16,   0,   7,  21,  33,   1,
    -33,  -3, -14, -21, -13, -12, -39, -21,
)

eg_bishop_table = (
    -14, -21, -11,  -8, -7,  -9, -17, -24,
     -8,  -4,   7, -12, -3, -13,  -4, -14,
      2,  -8,   0,  -1, -2,   6,   0,   4,
     -3,   9,  12,   9, 14,  10,   3,   2,
     -6,   3,  13,  19,  7,  10,  -3,  -9,
    -12,  -3,   8,  10, 13,   3,  -7, -15,
    -14, -18,  -7,  -1,  4,  -9, -15, -27,
    -23,  -9, -23,  -5, -9, -16,  -5, -17,
)

mg_rook_table = (
     32,  42,  32,  51, 63,  9,  31,  43,
     27,  32,  58,  62, 80, 67,  26,  44,
     -5,  19,  26,  36, 17, 45,  61,  16,
    -24, -11,   7,  26, 24, 35,  -8, -20,
    -36, -26, -12,  -1,  9, -7,   6, -23,
    -45, -25, -16, -17,  3,  0,  -5, -33,
    -44, -16, -20,  -9, -1, 11,  -6, -71,
    -19, -13,   1,  17, 16,  7, -37, -26,
)

eg_rook_table = (
    13, 10, 18, 15, 12,  12,   8,   5,
    11, 13, 13, 11, -3,   3,   8,   3,
     7,  7,  7,  5,  4,  -3,  -5,  -3,
     4,  3, 13,  1,  2,   1,  -1,   2,
     3,  5,  8,  4, -5,  -6,  -8, -11,
    -4,  0, -5, -1, -7, -12,  -8, -16,
    -6, -6,  0,  2, -9,  -9, -11,  -3,
    -9,  2,  3, -1, -5, -13,   4, -20,
)

mg_queen_table = (
    -28,   0,  29,  12,  59,  44,  43,  45,
    -24, -39,  -5,   1, -16,  57,  28,  54,
    -13, -17,   7,   8,  29,  56,  47,  57,
    -27, -27, -16, -16,  -1,  17,  -2,   1,
     -9, -26,  -9, -10,  -2,  -4,   3,  -3,
    -14,   2, -11,  -2,  -5,   2,  14,   5,
    -35,  -8,  11,   2,   8,  15,  -3,   1,
     -1, -18,  -9,  10, -15, -25, -31, -50,
)

eg_queen_table = (
     -9,  22,  22,  27,  27,  19,  10,  20,
    -17,  20,  32,  41,  58,  25,  30,   0,
    -20,   6,   9,  49,  47,  35,  19,   9,
      3,  22,  24,  45,  57,  40,  57,  36,
    -18,  28,  19,  47,  31,  34,  39,  23,
    -16, -27,  15,   6,   9,  17,  10,   5,
    -22, -23, -30, -16, -16, -23, -36, -32,
    -33, -28, -22, -43,  -5, -32, -20, -41,
)

mg_king_table = (
    -65,  23,  16, -15, -56, -34,   2,  13,
     29,  -1, -20,  -7,  -8,  -4, -38, -29,
     -9,  24,   2, -16, -20,   6,  22, -22,
    -17, -20, -12, -27, -30, -25, -14, -36,
    -49,  -1, -27, -39, -46, -44, -33, -51,
    -14, -14, -22, -46, -44, -30, -15, -27,
      1,   7,  -8, -64, -43, -16,   9,   8,
    -15,  36,  12, -54,   8, -28,  24,  14,
)

eg_king_table = (
    -74, -35, -18, -18, -11,  15,   4, -17,
    -12,  17,  14,  17,  17,  38,  23,  11,
     10,  17,  23,  15,  20,  45,  44,  13,
     -8,  22,  24,  27,  26,  33,  26,   3,
    -18,  -4,  21,  24,  27,  23,   9, -11,
    -19,  -3,  11,  21,  23,  16,   7,  -9,
    -27, -11,   4,  13,  14,   4,  -5, -17,
    -53, -34, -21, -11, -28, -14, -24, -43
)

gamephaseInc = (0, 1, 1, 2, 4, 0)

mg_table = (
    mg_pawn_table,
    mg_knight_table,
    mg_bishop_table,
    mg_rook_table,
    mg_queen_table,
    mg_king_table,
)

eg_table = (
    eg_pawn_table,
    eg_knight_table,
    eg_bishop_table,
    eg_rook_table,
    eg_queen_table,
    eg_king_table,
)

piece_to_index = {
    chess.PAWN : 0,
    chess.KNIGHT : 1,
    chess.BISHOP : 2,
    chess.ROOK : 3,
    chess.QUEEN : 4,
    chess.KING : 5
}

color_to_index = {
    chess.WHITE : 0,
    chess.BLACK : 1
}

tempo = 10

def eval(board):
    mg = [0, 0]
    eg = [0, 0]
    gamePhase = 0
    side2move = 0 if board.turn == chess.WHITE else 1
    otherside2move = side2move ^ 1

    for square in range(64):
        pc = board.piece_at(square)
        if pc != None:
            pc_type = piece_to_index[pc.piece_type]
            color = color_to_index[pc.color]
            square = square ^ 56 if color == 0 else square
            mg[color] += mg_table[pc_type][square] + eg_value[pc_type]
            eg[color] += eg_table[pc_type][square] + mg_value[pc_type]
            gamePhase += gamephaseInc[pc_type]

    mgScore = mg[side2move] - mg[otherside2move]
    egScore = eg[side2move] - eg[otherside2move]
    mgPhase = gamePhase

    if mgPhase > 24:
        mgPhase = 24

    egPhase = 24 - mgPhase
    return tempo + (mgScore * mgPhase + egScore * egPhase) / 24

infinity = 100000
mate_score = 30000
draw_score = 0

null_move_r = 3
rfp_margin = 54
rfp_depth = 9
lmr_count = 5
lmr_depth = 3
lmr_base = 0.715
lmr_mul = 0.416
deltas = [195, 398, 448, 556, 1107]
asp_delta = 38
delta_mul = 2
asp_depth = 3
fp_depth = 5
fp_margin = 250
iir_depth = 3
hbtm = 4
sbtm = 49

killers = [None for _ in range(1024)]
history =  [[0 for _ in range(64)] for _ in range(64)]
counters = [[None for _ in range(64)] for _ in range(64)]

nodes = 0
seldepth = 0
best_move = None

start_time = time.time()
hb_max_time = 12_000
sb_max_time = 2_000

hash_size_mb = 0 # PYTHON!!!!!
num_tt_element = 16000000

class bounds:
    def __init__(self):
        self.UB = 0
        self.LB = 1
        self.E = 2
        self.NONE = 3

class transposition:
    def __init__(self):
        self.hash = -1
        self.tt_move : chess.Move = chess.Move.null()
        self.score = 0
        self.depth = 0
        self.bound  = bounds().NONE

empty_tt = transposition()
transposition_table = [empty_tt for _ in range(num_tt_element)]
tt_bounds = bounds()

mvvlvaTable = (
    ( 150_000_000, 250_000_00, 350_000_000, 450_000_000, 550_000_000, 650_000_000 ),
    ( 140_000_000, 240_000_00, 340_000_000, 440_000_000, 540_000_000, 640_000_000 ),
    ( 130_000_000, 230_000_00, 330_000_000, 430_000_000, 530_000_000, 630_000_000 ),
    ( 120_000_000, 220_000_00, 320_000_000, 420_000_000, 520_000_000, 620_000_000 ),
    ( 110_000_000, 210_000_00, 310_000_000, 410_000_000, 510_000_000, 610_000_000 ),
    ( 100_000_000, 200_000_00, 300_000_000, 400_000_000, 500_000_000, 600_000_000 ),
)

def qsearch(board, ply, alpha, beta):
    global nodes, seldepth, transposition_table

    elapsed = (time.time() - start_time) * 1000
    if global_depth > 1 and elapsed > hb_max_time:
        raise TimeoutError()
    legals = board.legal_moves
    stand_pat = eval(board)
    max_score = stand_pat

    if stand_pat >= beta:
        return beta
    
    if alpha < stand_pat:
        alpha = stand_pat

    captures = []

    if ply > seldepth:
        seldepth = ply

    for move in legals:
        if board.is_capture(move):
            captures.append(move)
            
    board_hash = chess.polyglot.zobrist_hash(board)
    tt_hash_index =  board_hash % num_tt_element
    curr_transposition = transposition_table[tt_hash_index]
    tt_hit = curr_transposition.hash == board_hash
    move_in_tt = curr_transposition.tt_move
    bound_in_tt = curr_transposition.bound
    score_in_tt = curr_transposition.score

    if tt_hit:
        if bound_in_tt == tt_bounds.LB and score_in_tt >= beta:
            return score_in_tt
        if bound_in_tt == tt_bounds.UB and score_in_tt <= alpha:
            return score_in_tt
        if bound_in_tt == tt_bounds.E:
            return score_in_tt

    captures = sorted(captures, key=lambda move: 
                    1_000_000_000 if tt_hit and move_in_tt == move else 
                    mvvlvaTable[piece_to_index[board.piece_at(move.from_square).piece_type]][piece_to_index[board.piece_at(move.from_square).piece_type]], reverse=True)

    old_alpha = alpha
    curr_best_move = None
    for move in captures:
        # Nasty en-passants
        index = piece_to_index[board.piece_at(move.to_square).piece_type] if board.piece_at(move.to_square) != None else 0
        if stand_pat + deltas[index] < alpha:
            return alpha

        nodes += 1
        board.push(move)
        score = -qsearch(board, ply + 1, -beta, -alpha)
        board.pop()

        if score > max_score:
            curr_best_move = move
            max_score = score
            if score > alpha:
                alpha = score
            if alpha >= beta:
                break
    
    new_tt = transposition()
    new_tt.hash = board_hash
    new_tt.bound = tt_bounds.LB if max_score >= beta else tt_bounds.UB if alpha == old_alpha else tt_bounds.E
    new_tt.tt_move = curr_best_move if alpha > old_alpha else move_in_tt
    new_tt.score = max_score
    new_tt.depth = 0
    transposition_table[tt_hash_index] = new_tt

    return max_score

def alphabeta(board, depth, ply, alpha, beta, parent_move):
    global nodes, seldepth, best_move, transposition_table

    elapsed = (time.time() - start_time) * 1000
    if global_depth > 1 and elapsed > hb_max_time:
        raise TimeoutError()
    if board.is_checkmate():
        return -mate_score + ply
    if ply != 0 and board.can_claim_draw() or board.is_insufficient_material() or board.is_stalemate():
        return draw_score
    if depth <= 0:
        return qsearch(board, ply, alpha, beta)
    
    pv_node = (beta - alpha) != 1

    board_hash = chess.polyglot.zobrist_hash(board)
    tt_hash_index =  board_hash % num_tt_element
    curr_transposition = transposition_table[tt_hash_index]
    tt_hit = curr_transposition.hash == board_hash
    move_in_tt = curr_transposition.tt_move
    depth_in_tt = curr_transposition.depth
    bound_in_tt = curr_transposition.bound
    score_in_tt = curr_transposition.score

    if not pv_node and tt_hit and depth_in_tt >= depth:
        if bound_in_tt == tt_bounds.LB and score_in_tt >= beta:
            return score_in_tt
        if bound_in_tt == tt_bounds.UB and score_in_tt <= alpha:
            return score_in_tt
        if bound_in_tt == tt_bounds.E:
            return score_in_tt
    elif depth > iir_depth:
        depth -= 1

    node_is_check = board.is_check()
    is_root = ply == 0
    max_score = -infinity
    legals = board.legal_moves
    if ply > seldepth:
        seldepth = ply

    seval = eval(board)
    if not pv_node and depth <= rfp_depth and seval - rfp_margin * depth >= beta and not node_is_check:
        return seval
    
    if not pv_node and seval > beta and not node_is_check:
        board.push(chess.Move.null())
        null_score = -alphabeta(board, depth - null_move_r - 1, ply + 1, -beta, -beta + 1, chess.Move.null())
        board.pop()
        if null_score >= beta:
            return null_score

    legals = sorted(list(legals), key=lambda move: 
                    1_000_000_000 if tt_hit and move_in_tt == move else 
                    mvvlvaTable[piece_to_index[board.piece_at(move.from_square).piece_type]][piece_to_index[board.piece_at(move.from_square).piece_type]] if board.is_capture(move) else 
                    10_000_000 if move == killers[ply] else
                    1_000_000 if move == counters[parent_move.from_square][parent_move.to_square] else
                    history[move.from_square][move.to_square], reverse=True)

    old_alpha = alpha
    curr_best_move = None
    move_count = 0

    for move in legals:

        if not pv_node and not board.is_capture(move) and depth <= fp_depth and seval * fp_margin < alpha and abs(max_score) < mate_score - ply - 1:
            continue

        move_count += 1
        nodes += 1
        lmr = int(lmr_base + math.log(depth) * math.log(move_count) * lmr_mul) if move_count > lmr_count and depth >= lmr_depth and not board.is_capture(move) and not node_is_check and not pv_node else 0

        board.push(move)

        board_is_check = board.is_check()

        check_extension = 1 if board_is_check else 0

        score = 0

        if move_count == 1:
            score = -alphabeta(board, depth + check_extension - 1, ply + 1, -beta, -alpha, move)
        else:
            score = -alphabeta(board, depth + check_extension - lmr - 1, ply + 1, -alpha - 1, -alpha, move)

            if lmr > 0 and score > alpha:
                score = -alphabeta(board, depth + check_extension - 1, ply + 1, -alpha - 1, -alpha, move)

            if score > alpha and beta > score:
                score = -alphabeta(board, depth + check_extension - 1, ply + 1, -beta, -alpha, move)

        board.pop()

        if score > max_score:
            max_score = score
            curr_best_move = move
            if is_root:
                best_move = move
            if score > alpha:
                alpha = score
            if score >= beta:
                if not board.is_capture(move):
                    killers[ply] = move
                    history[move.from_square][move.to_square] = min(history[move.from_square][move.to_square] + depth * depth, 999_999)

                    if bool(parent_move):
                        counters[parent_move.from_square][parent_move.to_square] = move
                break

    new_tt = transposition()
    new_tt.hash = board_hash
    new_tt.bound = tt_bounds.LB if max_score >= beta else tt_bounds.UB if alpha == old_alpha else tt_bounds.E
    new_tt.tt_move = curr_best_move if alpha > old_alpha else move_in_tt
    new_tt.score = max_score
    new_tt.depth = depth
    transposition_table[tt_hash_index] = new_tt

    return max_score

global_depth = 0
def getbestmove():
    global global_depth, killers, history, counters, nodes, best_move, seldepth
    history =  [[0 for _ in range(64)] for _ in range(64)]
    counters = [[None for _ in range(64)] for _ in range(64)]
    seldepth = 0
    nodes = 0
    start_search_time = time.time()

    try:
        score = 0
        alpha = -infinity
        beta = infinity
        delta = 0

        for depth in range(1, 256):
            global_depth = depth

            if depth > asp_depth:
                delta = asp_delta
                alpha = score - delta
                beta = score + delta

            new_score = 0
            killers = [None for _ in range(1024)]

            while True:
                new_score = alphabeta(board, depth, 0, alpha, beta, chess.Move.null())
                if new_score <= alpha:
                    print(f"info depth {depth} seldepth {seldepth} score cp {int(alpha)} lowerbound nodes {nodes} nps {int(nodes / (elapsed + 0.0000001))} time {int(elapsed * 1000)} pv {best_move}")
                    beta = (alpha + beta) / 2
                    alpha = new_score - delta

                elif new_score >= beta:
                    print(f"info depth {depth} seldepth {seldepth} score cp {int(beta)} upperbound nodes {nodes} nps {int(nodes / (elapsed + 0.0000001))} time {int(elapsed * 1000)} pv {best_move}")
                    beta = new_score + delta

                else:
                    break

                delta *= delta_mul

            score = new_score
            elapsed = time.time() - start_search_time
            print(f"info depth {depth} seldepth {seldepth} score cp {int(score)} nodes {nodes} nps {int(nodes / (elapsed + 0.0000001))} time {int(elapsed * 1000)} pv {best_move}")
            if elapsed * 1000 > sb_max_time:
                print(f"bestmove {best_move}")
                break
    except TimeoutError:
        print(f"bestmove {best_move}")


def parse_parameters(line):
    DEFAULT_WTIME = float('inf')
    DEFAULT_BTIME = float('inf')
    parameters = line.split()[1:]
    wtime, btime = DEFAULT_WTIME, DEFAULT_BTIME

    for i in range(len(parameters)):
        if parameters[i] == "infinite":
            wtime = float('inf')
            btime = float('inf')
        elif parameters[i] == "wtime" and i + 1 < len(parameters):
            wtime = float(parameters[i + 1])
        elif parameters[i] == "btime" and i + 1 < len(parameters):
            btime = float(parameters[i + 1])
    return wtime, btime


def play_chess():
    global board, hbtm, sbtm, hb_max_time, sb_max_time, start_time, hash_size_mb, null_move_r, rfp_depth, rfp_margin, lmr_count, lmr_depth, lmr_base, lmr_mul, deltas, asp_delta, asp_depth, fp_depth, fp_margin, tempo
    remaining_time = 1000000

    while True:
        line = input()
        if line == "uci":
            print("id name Imperious v0.0.9")
            print("id author Dragjon")
            print(f"option name Hash type spin default {hash_size_mb} min 0 max 0") 
            print(f"option name NullMoveR type spin default {null_move_r} min 0 max 10") # 1
            print(f"option name RFPMargin type spin default {rfp_margin} min 0 max 100") # 5
            print(f"option name RFPDepth type spin default {rfp_depth} min 0 max 20") # 2
            print(f"option name LMRCount type spin default {lmr_count} min 0 max 15") # 1
            print(f"option name LMRDepth type spin default {lmr_depth} min 0 max 10") # 1
            print(f"option name LMRBaseInt type spin default {int(lmr_base*1000)} min 0 max 5000") # 100
            print(f"option name LMRMulInt type spin default {int(lmr_mul*1000)} min 0 max 5000") # 100
            print(f"option name DeltaPawn type spin default {deltas[0]} min 0 max 480") # 10
            print(f"option name DeltaKnight type spin default {deltas[1]} min 0 max 800") # 10
            print(f"option name DeltaBishop type spin default {deltas[2]} min 0 max 850") # 10
            print(f"option name DeltaRook type spin default {deltas[3]} min 0 max 950") # 10
            print(f"option name DeltaQueen type spin default {deltas[4]} min 0 max 1500") # 10
            print(f"option name ASPDepth type spin default {asp_depth} min 0 max 10") # 1
            print(f"option name ASPDelta type spin default {asp_delta} min 0 max 200") # 5
            print(f"option name FPDepth type spin default {fp_depth} min 0 max 8") # 1
            print(f"option name FPMargin type spin default {fp_margin} min 0 max 400") # 5
            print(f"option name HBTM type spin default {hbtm} min 1 max 30") # 5
            print(f"option name SBTM type spin default {sbtm} min 1 max 60") # 5
            print(f"option name Tempo type spin default {tempo} min 0 max 50") # 5
            print("uciok")
        elif line.startswith("setoption name Hash"):
            _, hash_value = line.split("setoption name Hash value ", 1)
            print(f"info string Hash is set to {hash_value}MB")
            hash_value = int(hash_value)
            hash_size_mb = hash_value
        elif line.startswith("setoption name NullMoveR"):
            _, value = line.split("setoption name NullMoveR value ", 1)
            print(f"info string NullMoveR is set to {hash_value}")
            null_move_r = int(value)
        elif line.startswith("setoption name RFPMargin"):
            _, value = line.split("setoption name RFPMargin value ", 1)
            print(f"info string RFPMargin is set to {value}")
            rfp_margin = int(value)
        elif line.startswith("setoption name RFPDepth"):
            _, value = line.split("setoption name RFPDepth value ", 1)
            print(f"info string RFPDepth is set to {value}")
            rfp_depth = int(value)
        elif line.startswith("setoption name LMRCount"):
            _, value = line.split("setoption name LMRCount value ", 1)
            print(f"info string LMRCount is set to {value}")
            lmr_count = int(value)
        elif line.startswith("setoption name LMRDepth"):
            _, value = line.split("setoption name LMRDepth value ", 1)
            print(f"info string LMRDepth is set to {value}")
            lmr_depth = int(value)
        elif line.startswith("setoption name LMRBaseInt"):
            _, value = line.split("setoption name LMRBaseInt value ", 1)
            print(f"info string LMRBaseInt is set to {value}")
            lmr_base = int(value) / 1000
        elif line.startswith("setoption name LMRMulInt"):
            _, value = line.split("setoption name LMRMulInt value ", 1)
            print(f"info string LMRMulInt is set to {value}")
            lmr_mul = int(value) / 1000
        elif line.startswith("setoption name DeltaPawn"):
            _, value = line.split("setoption name DeltaPawn value ", 1)
            print(f"info string DeltaPawn is set to {value}")
            deltas[0] = int(value)
        elif line.startswith("setoption name DeltaKnight"):
            _, value = line.split("setoption name DeltaKnight value ", 1)
            print(f"info string DeltaKnight is set to {value}")
            deltas[1] = int(value)
        elif line.startswith("setoption name DeltaBishop"):
            _, value = line.split("setoption name DeltaBishop value ", 1)
            print(f"info string DeltaBishop is set to {value}")
            deltas[2] = int(value)
        elif line.startswith("setoption name DeltaRook"):
            _, value = line.split("setoption name DeltaRook value ", 1)
            print(f"info string DeltaRook is set to {value}")
            deltas[3] = int(value)
        elif line.startswith("setoption name DeltaQueen"):
            _, value = line.split("setoption name DeltaQueen value ", 1)
            print(f"info string DeltaQueen is set to {value}")
            deltas[4] = int(value)
        elif line.startswith("setoption name ASPDepth"):
            _, value = line.split("setoption name ASPDepth value ", 1)
            print(f"info string ASPDepth is set to {value}")
            asp_depth = int(value)
        elif line.startswith("setoption name ASPDelta"):
            _, value = line.split("setoption name ASPDelta value ", 1)
            print(f"info string ASPDelta is set to {value}")
            asp_delta = int(value)
        elif line.startswith("setoption name FPDepth"):
            _, value = line.split("setoption name FPDepth value ", 1)
            print(f"info string FPDepth is set to {value}")
            fp_depth = int(value)
        elif line.startswith("setoption name FPMargin"):
            _, value = line.split("setoption name FPMargin value ", 1)
            print(f"info string FPMargin is set to {value}")
            fp_margin = int(value)
        elif line.startswith("setoption name HBTM"):
            _, value = line.split("setoption name HBTM value ", 1)
            print(f"info string HBTM is set to {value}")
            hbtm = int(value)
        elif line.startswith("setoption name SBTM"):
            _, value = line.split("setoption name SBTM value ", 1)
            print(f"info string SBTM is set to {value}")
            sbtm = int(value)
        elif line.startswith("setoption name Tempo"):
            _, value = line.split("setoption name Tempo value ", 1)
            print(f"info string Tempo is set to {value}")
            tempo = int(value)
        elif line == "isready":
            print("readyok")
        elif line.startswith("position startpos"):
            board = chess.Board()
            if "moves" in line:
                _, moves_part = line.split("moves")
                moves = moves_part.strip().split()
                for move in moves:
                    board.push_uci(move)
        elif line.startswith("position fen"):
            _, fen = line.split("fen ")
            fen = fen.split(" ")
            fen = fen[0] + " " + fen[1] + " " + fen[2] + " " + fen[3] + " " + fen[4] + " " + fen[5]
            board.set_fen(fen)
            if "moves" in line:
                _, moves_part = line.split("moves")
                moves = moves_part.strip().split()
                for move in moves:
                    board.push_uci(move)
        elif line.startswith("go"):
            wtime, btime = parse_parameters(line)
            remaining_time = wtime if board.turn == chess.WHITE else btime
            start_time = time.time()
            sb_max_time = remaining_time / sbtm
            hb_max_time = remaining_time / hbtm
            getbestmove()
        elif line == "quit":
            break

if __name__ == "__main__":
    board = chess.Board()
    play_chess()