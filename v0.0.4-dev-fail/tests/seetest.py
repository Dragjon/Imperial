import chess
import sys
import os
from colorama import Fore, Style, init

# Add the parent directory of 'see.py' to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from see import seecapture
from conversions import indextouci

# Initialize colorama
init(autoreset=True)

def parse_seepos_line(line):
    parts = line.strip().split('|')
    if len(parts) < 3:
        raise ValueError(f"Line format incorrect: {line}")
    fen = parts[0].strip()
    uci_move = parts[1].strip()
    expected_score = int(parts[2].strip())
    comment = parts[3].strip() if len(parts) > 3 else ""
    return fen, uci_move, expected_score, comment

def load_positions(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    return [parse_seepos_line(line) for line in lines]

def test_see_positions(filename):
    positions = load_positions(filename)
    
    # Print header with color
    header = "{:<3} {:<50} {:<8} {:<14} {:<14} {:<10} {:<}".format("No.", "FEN", "Move", "Expected SEE", "Calculated SEE", "Result", "Comment")
    print(Fore.CYAN + header)
    print(Fore.CYAN + "=" * 110)
    
    i = 0
    for _, (fen, uci_move, expected_score, comment) in enumerate(positions, start=1):
        board = chess.Board(fen=fen)
        move = chess.Move.from_uci(uci_move)
        if board.piece_at(move.to_square) is None:
            continue
        i += 1
        calculated_score = seecapture(board, move)
        result = "Test passed." if calculated_score == expected_score else "Test failed."
        result_color = Fore.GREEN if result == "Test passed." else Fore.RED
        print("{:<3} {:<50} {:<8} {:<14} {:<14} {:<10} {:<}".format(
            i, fen, uci_move, expected_score, calculated_score, result_color + result, comment
        ))

if __name__ == "__main__":
    test_see_positions(os.path.abspath(os.path.join(os.path.dirname(__file__), 'seepos.txt')))
