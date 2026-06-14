import pygame
import chess
import os

WIDTH = 640
HEIGHT = 640
SQ_SIZE = WIDTH // 8

LIGHT = (240, 217, 181)
DARK = (181, 136, 99)
YELLOW = (255, 255, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

board = chess.Board()
selected_square = None
running = True

# -----------------------------
# LOAD CHESS PIECE IMAGES HERE
# -----------------------------
pieces = {}

names = [
    "wp", "wr", "wn", "wb", "wq", "wk",
    "bp", "br", "bn", "bb", "bq", "bk"
]

for name in names:
    image_path = os.path.join("images", name + ".png")
    image = pygame.image.load(image_path)
    pieces[name] = pygame.transform.scale(image, (SQ_SIZE, SQ_SIZE))


def legal_pawn_advance_moves(board):
    return [move for move in board.legal_moves]


def draw_board():
    for row in range(8):
        for col in range(8):
            color = LIGHT if (row + col) % 2 == 0 else DARK
            pygame.draw.rect(
                screen,
                color,
                (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            )


def draw_pieces():
    piece_map = {
        chess.PAWN: "p",
        chess.ROOK: "r",
        chess.KNIGHT: "n",
        chess.BISHOP: "b",
        chess.QUEEN: "q",
        chess.KING: "k"
    }

    for square in chess.SQUARES:
        piece = board.piece_at(square)

        if piece is not None:
            col = chess.square_file(square)
            row = 7 - chess.square_rank(square)

            color = "w" if piece.color == chess.WHITE else "b"
            key = color + piece_map[piece.piece_type]

            screen.blit(
                pieces[key],
                (col * SQ_SIZE, row * SQ_SIZE)
            )


def highlight_selected():
    if selected_square is not None:
        col = chess.square_file(selected_square)
        row = 7 - chess.square_rank(selected_square)

        pygame.draw.rect(
            screen,
            YELLOW,
            (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE),
            5
        )


def get_square_from_mouse(pos):
    x, y = pos

    col = x // SQ_SIZE
    row = y // SQ_SIZE

    rank = 7 - row
    file = col

    return chess.square(file, rank)


while running:
    screen.fill((0, 0, 0))

    draw_board()
    highlight_selected()
    draw_pieces()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            clicked_square = get_square_from_mouse(event.pos)

            if selected_square is None:
                piece = board.piece_at(clicked_square)

                if piece is not None and piece.color == board.turn:
                    selected_square = clicked_square

            else:
                move = chess.Move(selected_square, clicked_square)
                print("Trying to move:", move)

                if move in legal_pawn_advance_moves(board):
                    board.push(move)
                    print(board)
                else:
                    print("Illegal move!")

                selected_square = None

pygame.quit()
