# This imports everything that you need
from gen_pawn_war import *

class YourPawnWarBot(PawnWarBot):
    def make_move(self, chess_board: chess.Board) -> chess.Move:
        # Implement your strategy here! See example_bots.py for some ideas.

        # By default, the bot just makes the first legal move that it finds
        # you should delete the code below and replace it with your own idea
        legal_moves = legal_pawn_war_moves(chess_board)
        first_legal_move = legal_moves[0]
        return first_legal_move