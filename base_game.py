# Basic functions of othello
BLACK = 1
WHITE = 2
# Constants for directions
UP = (-1, 0)
UP_RIGHT = (-1, 1)
RIGHT = (0, 1)
DOWN_RIGHT = (1, 1)
DOWN = (1, 0)
DOWN_LEFT = (1, -1)
LEFT = (0, -1)
UP_LEFT = (-1, -1)

board_size = 8
board_choices = None
alphabet_list = None


def base_game_init(boardsize):
    global board_size, alphabet_list, board_choices
    board_size = boardsize
    alphabet_list = [chr(x) for x in range(ord('a'), ord('z') + 1)]
    board_choices = [["%c%d " % (alphabet_list[i], j) for i in range(board_size)] for j in range(board_size)]


def evaluator(board, color):
    cur_score = 0
    for row in board:
        for cell in row:
            if cell == color:
                cur_score += 1
    return cur_score


def finish_game(board):
    print('No more moves is available. Game is finished')
    black_count = 0
    white_count = 0
    for row in board:
        for cell in row:
            if cell == BLACK:
                black_count += 1
            elif cell == WHITE:
                white_count += 1


    if black_count > white_count:
        print("Black player wins\n "+str(black_count)+" points")
    elif white_count > black_count:
        print("White player wins \n "+str(white_count)+" points")
    else:
        print("Draw")


def print_choices(board, valid_moves):
    move_coords = [valid_move["coordinate"] for valid_move in valid_moves]
    for i, rows in enumerate(board):
        for j, cell in enumerate(rows):
            if (i, j) in move_coords:
                print(board_choices[i][j], end='')
            elif cell == WHITE:
                print('WW ', end='')
            elif cell == BLACK:
                print('BB ', end='')
            elif cell == 0:
                print('-- ', end='')
            else:
                print(cell, end='')
        print()


def get_choice(valid_moves, color):
    move_coords = [valid_move["coordinate"] for valid_move in valid_moves]

    choice = input()
    j = ord(choice[0]) - ord('a')
    i = ord(choice[1]) - ord('0')
    print(i, j)
    if (i, j) in move_coords:
        return valid_moves[move_coords.index((i, j))]
    else:
        print("That is not a valid move")
        return get_choice(valid_moves, color)


def enemy_color(color):
    if color == WHITE:
        return BLACK
    else:
        return WHITE


def get_valid_moves(board, color):
    res_moves = []
    for iRow, row in enumerate(board):
        for iCol, cell in enumerate(row):
            if cell != 0:
                continue
            move = check_valid_move(board, color, (iRow, iCol))
            if move is not None:
                res_moves.append(move)
    return res_moves


def make_move(board, valid_move, color):
    def flip_direction(i, j, dir_tuple, player_color):
        diffI, diffJ = dir_tuple
        # Place starting piece
        board[i][j] = player_color
        i, j = move_over(i, j, diffI, diffJ)
        # Filp  until finding the same colored piece
        while is_in_range(i, j):
            if board[i][j] == player_color:
                break
            board[i][j] = player_color
            i, j = move_over(i, j, diffI, diffJ)

    directions = valid_move['direction']
    (tmpI, tmpJ) = valid_move['coordinate']
    for direction in directions:
        flip_direction(tmpI, tmpJ, direction, color)


# check if cell is a valid move or not
# returns None if coordinate is not a valid move
# else returns
# result = [
#   coordinate: (int, int) valid move
#   amount: int  amount of enemy piece taken if move was made
#   direction: [] list of directions of enemy piece taken if move was made
# ]
def check_valid_move(board, color, coordinate):
    result = {"coordinate": coordinate, "amount": 0, "direction": []}

    # Returns 0 if move is invalid
    # else returns the amount of enemy piece taken if move is valid
    def check_line(i, j, direction):
        diffI, diffJ = direction
        i, j = move_over(i, j, diffI, diffJ)
        # If neighbor is in range and is enemy piece
        if is_in_range(i, j) and board[i][j] == enemy_color(color):
            i, j = move_over(i, j, diffI, diffJ)  # move 1 step
            count = 1
            same_color_found = False
            # find same colored piece
            while is_in_range(i, j):
                if board[i][j] == color:
                    same_color_found = True
                    break
                elif board[i][j] != enemy_color(color):
                    break
                i, j = move_over(i, j, diffI, diffJ)
                count += 1
            # done looping
            if same_color_found:
                # If there was a same colored piece, return the count
                return count
            else:
                # If there was no same colored piece, move is invalid
                return 0
        else:
            # If neighbor is not enemy piece, move is invalid
            return 0

    iStart, jStart = coordinate
    check_line_results = [
        check_line(iStart, jStart, UP),
        check_line(iStart, jStart, UP_RIGHT),
        check_line(iStart, jStart, RIGHT),
        check_line(iStart, jStart, DOWN_RIGHT),
        check_line(iStart, jStart, DOWN),
        check_line(iStart, jStart, DOWN_LEFT),
        check_line(iStart, jStart, LEFT),
        check_line(iStart, jStart, UP_LEFT)
    ]
    # Check move for every directions
    if check_line_results[0] > 0:
        result["amount"] += check_line_results[0]
        result["direction"].append(UP)
    if check_line_results[1] > 0:
        result["amount"] += check_line_results[1]
        result["direction"].append(UP_RIGHT)
    if check_line_results[2] > 0:
        result["amount"] += check_line_results[2]
        result["direction"].append(RIGHT)
    if check_line_results[3] > 0:
        result["amount"] += check_line_results[3]
        result["direction"].append(DOWN_RIGHT)
    if check_line_results[4] > 0:
        result["amount"] += check_line_results[4]
        result["direction"].append(DOWN)
    if check_line_results[5] > 0:
        result["amount"] += check_line_results[5]
        result["direction"].append(DOWN_LEFT)
    if check_line_results[6] > 0:
        result["amount"] += check_line_results[6]
        result["direction"].append(LEFT)
    if check_line_results[7] > 0:
        result["amount"] += check_line_results[7]
        result["direction"].append(UP_LEFT)

    if result["amount"] == 0:
        return None
    return result


def is_in_range(i, j):
    return board_size > i >= 0 and board_size > j >= 0


def move_over(mv_i, mv_j, diffI, diffJ):
    mv_i += diffI
    mv_j += diffJ
    return mv_i, mv_j


def print_board_helper(board, color):
    valid_moves = get_valid_moves(board, color)
    moves = [valid_move["coordinate"] for valid_move in valid_moves]
    print_choices(board, moves)
