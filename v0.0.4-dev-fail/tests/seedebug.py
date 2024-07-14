import chess
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from see import *

board = chess.Board(fen="4R3/2r3p1/5bk1/1p1r1p1p/p2PR1P1/P1BK1P2/1P6/8 b - -")
from conversions import *
print(indextouci(chess.Move.from_uci("h5g4").from_square))
print(seecapture(board, chess.Move.from_uci("h5g4"), debug = True))