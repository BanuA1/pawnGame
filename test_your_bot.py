'''
Use this script to test how your bot performs.

Uppercase P = white pawns
Lowercase p = black pawns
'''
from example_bots import *
from your_bot import YourPawnWarBot


your_bot = YourPawnWarBot()
enemy_bot = CapturePawnWarBot()

board = make_pawn_war_board()

# choose the first player randomly
first_player = random.choice([your_bot, enemy_bot])
if first_player == your_bot:
    print("Your bot is playing as white and goes first!")
    second_player = enemy_bot
else:
    print("Your bot is playing as black and goes second!")
    second_player = your_bot

current_player = first_player
result = pawn_war_result(board)
# keep playing the game until there's a result (win for white, win for black, or tie)
while result is None:
    if current_player == your_bot:
        bot_name = "Your bot"
    else:
        bot_name = "Enemy bot"

    print(f"{bot_name}'s turn:")
    print(board)
    # make a move on the copy of the board so that the bot can't accidentally mess with the real board
    move = current_player.make_move(board.copy())
    print(f"{bot_name} made move: {move}")
    board.push(move)
    result = pawn_war_result(board)

print(board)
print(result)
if your_bot == first_player:
    print("(As a reminder, your bot was playing as white.)")
else:
    print("(As a reminder, your bot was playing as black.)")
