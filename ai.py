import copy
from base_game import enemy_color, get_valid_moves, make_move, evaluator

depth =1
move_num = None
show_steps = False


def init(depth_oth):
    global depth
    depth = depth_oth




def start(movenum):
    global move_num
    move_num = movenum


# Returns the first available
def naive(valid_moves):
    return valid_moves[0]


def minimax(board, cur_minimax_color):
    max_depth = depth + move_num

    def _minimax(cur_board, cur_color, cur_depth, isMax, alpha, beta, parent_has_no_moves=False):

        if max_depth == cur_depth:
            score = evaluator(cur_board, cur_minimax_color)
            return score, None

        valid_moves = get_valid_moves(cur_board, cur_color)
        if len(valid_moves) == 0:
            if parent_has_no_moves:
                score = evaluator(cur_board, cur_minimax_color)
            else:
                score, move = _minimax(
                    copy.deepcopy(cur_board), enemy_color(cur_color), cur_depth + 1, not isMax,
                    alpha, beta, True)
            return score, None

        if isMax:
            #     ai_gui.add_minimax_board(cur_board, alpha, cur_depth - g_move_num, isMax, False)
            alpha_move = valid_moves[0]
            for i, move in enumerate(valid_moves):
                board_copy = copy.deepcopy(cur_board)
                make_move(board_copy, move, cur_color)

                cur_score, cur_move = _minimax(board_copy, enemy_color(cur_color), cur_depth + 1, False, alpha, beta)
                # print_minimax_move(cur_move)
                if cur_score > alpha:
                    alpha = cur_score
                    alpha_move = move
                if beta <= alpha:
                    if len(valid_moves) - 1 > i:
                        board_copy2 = copy.deepcopy(cur_board)
                        make_move(board_copy2, valid_moves[i + 1], cur_color)
                    break

            return alpha, alpha_move
        else:
            beta_move = valid_moves[0]
            for i, move in enumerate(valid_moves):
                board_copy = copy.deepcopy(cur_board)
                make_move(board_copy, move, cur_color)

                cur_score, cur_move = _minimax(board_copy, enemy_color(cur_color), cur_depth + 1, True, alpha, beta)
                # print_minimax_move(cur_move)
                if beta > cur_score:
                    beta = cur_score
                    beta_move = move
                if beta <= alpha:
                    # Go to next node
                    if  len(valid_moves) - 1 > i:
                        board_copy2 = copy.deepcopy(cur_board)
                        make_move(board_copy2, valid_moves[i + 1], cur_color)

                    break

            return beta, beta_move



    best_score, best_move = _minimax(copy.deepcopy(board), cur_minimax_color, move_num, True, float("-inf"),
                                     float("inf"))

    return best_move




