import chess
import chess.polyglot
from ordering import ordercaptures, orderwithquiets
from eval import eval
from conversions import piece_to_index
import math
import time

infinity = 100000
mate_score = 30000
draw_score = 0

null_move_r = 3
rfp_margin = 55
rfp_depth = 8
lmr_count = 5
lmr_depth = 2
lmr_base = 0.75
lmr_mul = 0.4
deltas = (180, 400, 450, 550, 1100)
asp_delta = 40

killers = [None for _ in range(1024)]
history =  [[0 for _ in range(64)] for _ in range(64)]
counters = [[None for _ in range(64)] for _ in range(64)]

nodes = 0
seldepth = 0
best_move = None

hbtm = 10
sbtm = 40
start_time = time.time()
hb_max_time = 12_000
sb_max_time = 2_000

hash_size_mb = 32
tt_size = hash_size_mb * 250000
tt_move = [None for _ in range(tt_size)]

def qsearch(ply, alpha, beta):
    global board, nodes, seldepth

    elapsed = (time.time() - start_time) * 1000
    if global_depth > 1 and elapsed > hb_max_time:
        raise TimeoutError()
    stand_pat = eval(board)
    max = stand_pat

    if stand_pat >= beta:
        return beta
    
    if alpha < stand_pat:
        alpha = stand_pat

    legals = board.legal_moves
    captures = []

    if ply > seldepth:
        seldepth = ply

    for move in legals:
        if board.is_capture(move):
            captures.append(move)

    board_hash = chess.polyglot.zobrist_hash(board) % tt_size
    move_in_tt = tt_move[board_hash]
    captures = ordercaptures(board, captures, move_in_tt)
    for move in captures:
        # Nasty en-passants
        index = piece_to_index[board.piece_at(move.to_square).piece_type] if board.piece_at(move.to_square) != None else 0
        if stand_pat + deltas[index] < alpha:
            return alpha

        nodes += 1
        board.push(move)
        score = -qsearch(ply + 1, -beta, -alpha)
        board.pop()

        if score > max:
            tt_move[board_hash] = move
            max = score
            if score > alpha:
                alpha = score
                if score >= beta:
                    return beta
    
    return max

def alphabeta(depth, ply, alpha, beta, parent_move):
    global board, nodes, seldepth, best_move

    elapsed = (time.time() - start_time) * 1000
    if global_depth > 1 and elapsed > hb_max_time:
        raise TimeoutError()
    if board.is_checkmate():
        return -mate_score + ply
    if ply != 0 and board.can_claim_draw() or board.is_insufficient_material() or board.is_stalemate():
        return draw_score
    if depth <= 0:
        return qsearch(ply, alpha, beta)
    
    node_is_check = board.is_check()
    is_root = ply == 0
    pv_node = beta - alpha != 1
    max = -infinity
    legals = board.legal_moves
    if ply > seldepth:
        seldepth = ply

    seval = eval(board)
    if depth <= rfp_depth and seval - rfp_margin * depth >= beta and not node_is_check:
        return seval
    
    if seval > beta and not node_is_check:
        board.push(chess.Move.null())
        null_score = -alphabeta(depth - null_move_r - 1, ply + 1, -beta, -beta + 1, chess.Move.null())
        board.pop()
        if null_score >= beta:
            return null_score

    board_hash = chess.polyglot.zobrist_hash(board) % tt_size
    move_in_tt = tt_move[board_hash]

    legals = orderwithquiets(board, board.legal_moves, move_in_tt, killers, ply, counters, parent_move, history)
    move_count = 0

    for move in legals:
        move_count += 1
        nodes += 1
        lmr = int(lmr_base + math.log(depth) * math.log(move_count) * lmr_mul) if move_count > lmr_count and depth >= lmr_depth and not board.is_capture(move) and not node_is_check and not pv_node else 0

        board.push(move)

        board_is_check = board.is_check()

        check_extension = 1 if board_is_check else 0

        score = 0

        if move_count == 1 and pv_node:
            score = -alphabeta(depth + check_extension - 1, ply + 1, -beta, -alpha, move)
        else:
            score = -alphabeta(depth + check_extension - lmr - 1, ply + 1, -alpha - 1, -alpha, move)

            if score > alpha and beta > score:
                score = -alphabeta(depth + check_extension - 1, ply + 1, -beta, -alpha, move)

        board.pop()

        if score > max:
            max = score
            tt_move[board_hash] = move
            if is_root:
                best_move = move
            if score > alpha:
                alpha = score
                if score >= beta:
                    if board.piece_at(move.to_square) is None:
                        killers[ply] = move
                        history[move.from_square][move.to_square] = min(history[move.from_square][move.to_square] + depth * depth, 999_999)

                        if bool(parent_move):
                            counters[parent_move.from_square][parent_move.to_square] = move
                    break

    return max

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

            if depth > 3:
                delta = asp_delta
                alpha = score - delta
                beta = score + delta

            new_score = 0
            killers = [None for _ in range(1024)]

            while True:
                new_score = alphabeta(depth, 0, alpha, beta, chess.Move.null())
                if new_score <= alpha:
                    beta = (alpha + beta) / 2
                    alpha = new_score - delta

                elif new_score >= beta:
                    beta = new_score + delta

                else:
                    break

                delta *= 2

            score = new_score
            elapsed = time.time() - start_search_time
            print(f"info depth {depth} seldepth {seldepth} score cp {int(score)} nodes {nodes} nps {int(nodes / (elapsed + 0.0000001))} time {int(elapsed * 1000)} pv {best_move}")
            if elapsed * 1000 > sb_max_time:
                print(f"bestmove {best_move}")
                break
    except TimeoutError:
        print(f"bestmove {best_move}")


def parse_parameters(line):
    DEFAULT_WTIME = 1000000
    DEFAULT_BTIME = 1000000
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
    global board, hbtm, sbtm, hb_max_time, sb_max_time, start_time, tt_size, tt_move, hash_size_mb
    remaining_time = 1000000

    while True:
        line = input()
        if line == "uci":
            print("id name Imperious v0.0.4")
            print("id author Dragjon")
            print(f"option name Hash type spin default 32 min 1 max 256")
            print("uciok")
        elif line.startswith("setoption name Hash"):
            _, hash_value = line.split("setoption name Hash value ", 1)
            print(f"info string Hash is set to {hash_value}MB")
            hash_value = int(hash_value)
            hash_size_mb = hash_value
            tt_size = hash_size_mb * 250000
            tt_move = [None for _ in range(tt_size)]
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