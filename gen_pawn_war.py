
import chess


class LabeledBoard(chess.Board):
    def __str__(self):
        rows = []

        for rank in range(7, -1, -1):
            pieces = []

            for file in range(8):
                square = chess.square(file, rank)
                piece = self.piece_at(square)
                pieces.append(piece.symbol() if piece else ".")

            rows.append(f"{rank + 1}  " + " ".join(pieces))

        rows.append("")
        rows.append("   a b c d e f g h")
        return "\n".join(rows)


def make_pawn_war_board():
    board = LabeledBoard(None)

    for column in range(8):
        board.set_piece_at(chess.square(column, 1), chess.Piece(chess.PAWN, chess.WHITE))
        board.set_piece_at(chess.square(column, 6), chess.Piece(chess.PAWN, chess.BLACK))

    board.turn = chess.WHITE
    board.clear_stack()
    return board


def pawn_reached_end(board):
    for square in chess.SquareSet(chess.BB_RANK_8):
        if board.piece_at(square) == chess.Piece(chess.PAWN, chess.WHITE):
            return chess.WHITE

    for square in chess.SquareSet(chess.BB_RANK_1):
        if board.piece_at(square) == chess.Piece(chess.PAWN, chess.BLACK):
            return chess.BLACK

    return None


def try_move(board, move_text):
    try:
        move = chess.Move.from_uci(move_text)
    except ValueError:
        return False, "Invalid move format. Use moves like e2e4 or d7d5."

    if move not in board.legal_moves:
        return False, "Illegal move."

    board.push(move)

    winner = pawn_reached_end(board)
    if winner == chess.WHITE:
        return True, "White wins!"
    elif winner == chess.BLACK:
        return True, "Black wins!"

    return True, "Move played."


board = make_pawn_war_board()

while True:
    print(board)
    print("Turn:", "White" if board.turn == chess.WHITE else "Black")
    print("Legal moves:", [move.uci() for move in board.legal_moves])

    move_text = input("Move: ")
    ok, message = try_move(board, move_text)
    print(message)
    print()

    if "wins" in message:
        break