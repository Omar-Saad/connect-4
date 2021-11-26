from variables import *


def create_board():
    board = np.zeros((ROWS, COL), dtype=np.uint8)
    return board


def drop(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    """checks if the selected column contains empty space or not"""
    return board[ROWS - 1][col] == EMPTY


def get_next_row(board, col):
    """Returns the row corresponding to the valid column in the board"""
    for row in range(ROWS):
        if board[row][col] == EMPTY:
            return row


def check_board(board, piece, streak=4):
    # TODO : optimization using sparse matrix
    """The function use convolution to calculate how many piece is connected in the board
    Example:
    0   0   0   0   0   0                               0   0   0   0   0   0
    1   1   1   1   1   1                               1   2   3   4   4   4
    1   1   0   1   1   1   conv  1   1   1   1     =   1   2   0   1   2   3
    1   1   1   0   1   1                               1   2   3   0   0   0
    1   0   1   1   1   1                               1   0   1   2   3   4
    """
    horizontal_window = np.array([[1, 1, 1, 1]], dtype=np.uint8)
    vertical_window = np.transpose(horizontal_window)
    diagonal_window = np.eye(4, dtype=np.uint8)
    inv_diagonal_window = np.fliplr(diagonal_window)
    winning_windows = [horizontal_window, vertical_window, diagonal_window, inv_diagonal_window]
    score = 0
    for window in winning_windows:
        conv = scipy.signal.convolve(board == piece, window, mode="valid")
        # count streak in conv matrix
        if (conv == streak).any():
            score += np.count_nonzero(conv == 4)
    return score


def print_board(board):
    print(np.flip(board, 0))


def generate_possible_moves(state):
    possible_moves = []

    for j in range(COL):
        for i in range(ROWS):
            if state[i][j] == 1 or state[i][j] == 2:
                possible_moves.append([i - 1, j])
                break
            if i == 5:
                possible_moves.append([i, j])
                break

    return possible_moves


# def maximize(board, k):
#     if not (board == 0).any() or k == 0:
#         return None, evaluate(board)
#     k -= 1
#     (max_child, max_utility) = (None, -inf)
#
#     for child in generate_children(board, AI_PLAYER):
#         (temp_child, utility) = minimize(child, k)
#
#         if utility > max_utility:
#             max_child, max_utility = child, utility
#
#     return max_child, max_utility
#
#
# def minimize(board, k):
#     if not (board == 0).any() or k == 0:
#         return None, evaluate(board)
#     k -= 1
#     (min_child, min_utility) = (None, inf)
#
#     for child in generate_children(board, HUMAN_PLAYER):
#         (temp_child, utility) = maximize(child, k)
#
#         if utility < min_utility:
#             min_child, min_utility = child, utility
#
#     return min_child, min_utility
#
#
# def minimax(board, k):
#     (child, utility) = maximize(board, k)
#     print(child)
#     print("util = " + str(utility))
#     return child
#

# SECOND minimax implementation


'''
minimax pseudocode => Wikipedia
function  minimax(node, depth, maximizingPlayer) is
    if depth = 0 or node is a terminal node then
        return the heuristic value of node
    if maximizingPlayer then
        value := −∞
        for each child of node do
            value := max(value, minimax(child, depth − 1, FALSE))
        return value
    else (* minimizing player *)
        value := +∞
        for each child of node do
            value := min(value, minimax(child, depth − 1, TRUE))
        return value
'''


def is_terminal(board):
    return not (board == 0).any()


def get_valid_location(board):
    """return valid column in board"""
    valid = []
    for col in range(COL):
        if is_valid_location(board, col):
            valid.append(col)
    return valid


# def generate_children(board, piece):
#     """generate 7 children at most"""
#     valid = get_valid_location(board)
#     children = []
#     for valid_col in valid:
#         c_board = np.copy(board)
#         row = get_next_row(board, valid_col)
#         drop(c_board, row, valid_col, piece)
#         children.append(c_board)
#     return children


def evaluate_1(board):
    score = 0
    center_array = [int(i) for i in list(board[:, COL // 2])]
    center_count = center_array.count(AI)
    score += center_count * 3
    score += check_board(board, AI) * 100
    score += check_board(board, AI, 3) * 5
    score += check_board(board, AI, 2) * 2
    score -= check_board(board, HUMAN) * 100
    score -= check_board(board, HUMAN, 3) * 50
    return score


from collections import deque

tree = deque()


def minimax(board, depth, is_alpha_beta: bool, piece, alpha=-math.inf, beta=math.inf):
    valid_location = get_valid_location(board)
    if depth == 0 or is_terminal(board):
        if is_terminal(board):
            ai_score = check_board(board, AI)
            player_score = check_board(board, PLAYER_1)
            if ai_score > player_score:
                return None, math.inf
            elif ai_score < player_score:
                return None, -math.inf
            else:
                return None, 0
        else:
            return None, evaluate_1(board)

    if piece == AI:
        score = -math.inf
        column = random.choice(valid_location)
        a = []

        for col in valid_location:
            row = get_next_row(board, col)
            board_copy = board.copy()
            drop(board_copy, row, col, AI)
            max_score = minimax(board_copy, depth - 1, is_alpha_beta, PLAYER_1, alpha, beta)[1]
            a.append(max_score)
            if max_score > score:
                score = max_score
                column = col
            # Alpha Beta
            if is_alpha_beta:
                alpha = max(alpha, score)
                if alpha >= beta:
                    break
        tree.append("max")
        tree.append([score, depth])

        tree.append(a)

        return column, score

    else:
        score = math.inf
        column = random.choice(valid_location)
        a = []

        for col in valid_location:
            row = get_next_row(board, col)
            board_copy = board.copy()
            drop(board_copy, row, col, PLAYER_1)
            min_score = minimax(board_copy, depth - 1, is_alpha_beta, AI, alpha, beta)[1]
            a.append(min_score)
            if min_score < score:
                score = min_score
                column = col
                # Alpha Beta
            if is_alpha_beta:
                beta = min(beta, score)
                if alpha >= beta:
                    break
        tree.append("min")
        tree.append([score, depth])
        tree.append(a)
        return column, score


def print_tree():
    while len(tree) > 0:
        x = tree.popleft()
        if isinstance(x, str):
            print("                    " * (tree[0][1] - 1), end="")
            print(x + " Choose : " + str(tree[0][0]))
            print("                    " * (tree[0][1] - 1), end="")
            print("depth = " + str(tree[0][1]))
            print("                    " * (tree[0][1] - 1), end="")
            tree.popleft()

        elif isinstance(x, list):
            for i in x:
                print(i, end=" ")
            print()
            print("--------------------------------")
