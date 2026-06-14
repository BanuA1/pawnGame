import pygame
import chess
import random
import os

WIDTH = 640
HEIGHT = 700          # extra space at bottom for turn/game text
BOARD_SIZE = 640
SQ_SIZE = BOARD_SIZE // 8

LIGHT = (240, 217, 181)
DARK = (181, 136, 99)
YELLOW = (255, 255, 0)
GREEN = (40, 180, 90)
RED = (220, 60, 60)
BLACK = (30, 30, 30)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")
clock = pygame.time.Clock()

board = chess.Board()
selected_square = None
running = True
play_against_ai = False   # Press A to turn AI on/off
human_color = chess.WHITE

font = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont(None, 36)

# Optional sound. Put move.wav in the same folder if you want sound.
move_sound = None
if os.path.exists("move.wav"):
    move_sound = pygame.mixer.Sound("move.wav")

# Load chess piece images from images/ folder
pieces = {}
names = [
    "wp", "wr", "wn", "wb", "wq", "wk",
    "bp", "br", "bn", "bb", "bq", "bk"
]

for name in names:
    path = f"images/{name}.png"
    image = pygame.image.load(path)
    pieces[name] = pygame.transform.scale(image, (SQ_SIZE, SQ_SIZE))


def get_square_from_mouse(pos):
    x, y = pos
    if y >= BOARD_SIZE:
        return None

    col = x // SQ_SIZE
    row = y // SQ_SIZE

    rank = 7 - row
    file = col

    return chess.square(file, rank)


def draw_board():
    for row in range(8):
        for col in range(8):
            color = LIGHT if (row + col) % 2 == 0 else DARK
            pygame.draw.rect(
                screen,
                color,
                (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            )


def draw_coordinates():
    # Files: a b c d e f g h
    for col in range(8):
        letter = chr(ord("a") + col)
        text = font.render(letter, True, BLACK)
        screen.blit(text, (col * SQ_SIZE + 5, BOARD_SIZE - 22))

    # Ranks: 1 2 3 4 5 6 7 8
    for row in range(8):
        rank = str(8 - row)
        text = font.render(rank, True, BLACK)
        screen.blit(text, (5, row * SQ_SIZE + 5))


def draw_pieces():
    for square in chess.SQUARES:
        piece = board.piece_at(square)

        if piece is not None:
            col = chess.square_file(square)
            row = 7 - chess.square_rank(square)

            color = "w" if piece.color == chess.WHITE else "b"

            piece_map = {
                chess.PAWN: "p",
                chess.ROOK: "r",
                chess.KNIGHT: "n",
                chess.BISHOP: "b",
                chess.QUEEN: "q",
                chess.KING: "k"
            }

            key = color + piece_map[piece.piece_type]
            screen.blit(pieces[key], (col * SQ_SIZE, row * SQ_SIZE))


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


def highlight_legal_moves():
    if selected_square is None:
        return

    for move in board.legal_moves:
        if move.from_square == selected_square:
            to_square = move.to_square
            col = chess.square_file(to_square)
            row = 7 - chess.square_rank(to_square)
            center = (col * SQ_SIZE + SQ_SIZE // 2, row * SQ_SIZE + SQ_SIZE // 2)

            # Red ring if capture, green dot if normal move
            if board.piece_at(to_square) is not None:
                pygame.draw.circle(screen, RED, center, 18, 4)
            else:
                pygame.draw.circle(screen, GREEN, center, 10)


def draw_status():
    pygame.draw.rect(screen, GRAY, (0, BOARD_SIZE, WIDTH, HEIGHT - BOARD_SIZE))

    if board.is_checkmate():
        winner = "Black" if board.turn == chess.WHITE else "White"
        message = f"Checkmate! {winner} wins. Press R to reset."
    elif board.is_stalemate():
        message = "Stalemate! Press R to reset."
    elif board.is_insufficient_material():
        message = "Draw: insufficient material. Press R to reset."
    elif board.is_check():
        turn = "White" if board.turn == chess.WHITE else "Black"
        message = f"{turn} is in check!"
    else:
        turn = "White" if board.turn == chess.WHITE else "Black"
        message = f"{turn} to move"

    ai_text = "AI: ON" if play_against_ai else "AI: OFF"
    help_text = "Esc: quit   R: reset   A: toggle AI"

    status_surface = big_font.render(message, True, BLACK)
    ai_surface = font.render(ai_text, True, BLACK)
    help_surface = font.render(help_text, True, BLACK)

    screen.blit(status_surface, (15, BOARD_SIZE + 8))
    screen.blit(ai_surface, (15, BOARD_SIZE + 38))
    screen.blit(help_surface, (120, BOARD_SIZE + 38))


def make_move(move):
    global selected_square

    # Auto-promote pawn to queen if it reaches last rank
    piece = board.piece_at(move.from_square)
    if piece is not None and piece.piece_type == chess.PAWN:
        to_rank = chess.square_rank(move.to_square)
        if to_rank == 0 or to_rank == 7:
            move = chess.Move(move.from_square, move.to_square, promotion=chess.QUEEN)

    if move in board.legal_moves:
        board.push(move)

        # Computer move
        if not board.is_game_over():
            ai_move = random.choice(list(board.legal_moves))
            board.push(ai_move)
            print("Computer played:", ai_move)

        selected_square = None

        if move_sound is not None:
            move_sound.play()

        return True

    selected_square = None
    return False


def ai_move():
    if board.is_game_over():
        return

    move = random.choice(list(board.legal_moves))
    board.push(move)

    if move_sound is not None:
        move_sound.play()


def reset_game():
    global board, selected_square
    board = chess.Board()
    selected_square = None


while running:
    screen.fill(BLACK)

    draw_board()
    draw_coordinates()
    highlight_selected()
    highlight_legal_moves()
    draw_pieces()
    draw_status()
    pygame.display.flip()

    # If AI is on, AI plays black after your white move
    if play_against_ai and board.turn != human_color and not board.is_game_over():
        pygame.time.wait(300)
        ai_move()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_r:
                reset_game()
            elif event.key == pygame.K_a:
                play_against_ai = not play_against_ai

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if board.is_game_over():
                continue

            # If AI is on, only let human move white pieces
            if play_against_ai and board.turn != human_color:
                continue

            clicked_square = get_square_from_mouse(event.pos)
            if clicked_square is None:
                continue

            if selected_square is None:
                piece = board.piece_at(clicked_square)

                if piece is not None and piece.color == board.turn:
                    selected_square = clicked_square

            else:
                move = chess.Move(selected_square, clicked_square)
                make_move(move)

    clock.tick(60)

pygame.quit()
