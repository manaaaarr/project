# from othello_constants import *  # Also available from othello_board
from base_game import *
import ai
import othello_board

base_game_init(board_size)

depth =1

ai.init(depth)

# Print board state
board = [[0 for i in range(board_size)] for j in range(board_size)]
# Set middle pieces to black and white
mid = board_size//2
board[mid-1][mid-1] = BLACK
board[mid-1][mid] = WHITE
board[mid][mid-1] = WHITE
board[mid][mid] = BLACK


cur_color = WHITE
g_move_num = 0
agent = {WHITE: "Player", BLACK: "Minimax"}  # Naive, Player, Minimax
othello_board.init(board)

while True:
    g_move_num += 0
    g_valid_moves = get_valid_moves(board, cur_color)
    # Check if game is finished
    if len(g_valid_moves) == 0:
        if len(get_valid_moves(board, enemy_color(cur_color))) == 0:
            finish_game(board)
            break
        else:
            print('Currnet player have no more moves available')
            cur_color = enemy_color(cur_color)
            continue

    # Get choice
    if agent[cur_color] == "Naive":
        print("white AI Move")
        ai.start(g_move_num)
        valid_move = ai.naive(g_valid_moves)
    elif agent[cur_color] == "Minimax":
        print("black AI Move")
        ai.start(g_move_num)
        print("color: ", cur_color)
        valid_move = ai.minimax(board, cur_color)
    else:
        print("Player Move")
        othello_board.refresh_board(board, g_valid_moves, cur_color)
        # valid_move = get_choice(g_valid_moves, cur_color)
        othello_board.start_listening(g_valid_moves, cur_color)
        valid_move = othello_board.get_choice()
    make_move(board, valid_move, cur_color)
    cur_color = enemy_color(cur_color)

