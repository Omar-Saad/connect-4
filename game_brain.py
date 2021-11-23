import math
from math import inf

from heurestic import evaluate
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


def generate_children(board, piece):
    """generate 7 children at most"""
    children = []
    for col in range(0, COL):
        if is_valid_location(board, col):
            row = get_next_row(board, col)
            temp = np.copy(board)
            drop(temp, row, col, piece)
            children.append(temp)

    return children


def maximize(board, k, HUMAN_SCORE, AI_SCORE):
    if not (board == 0).any() or k == 0:
        return None, evaluate(board, AI_PLAYER, HUMAN_SCORE, AI_SCORE)
    k -= 1
    (max_child, max_utility) = (None, -inf)

    for child in generate_children(board, AI_PLAYER):
        (temp_child, utility) = minimize(child, k, HUMAN_SCORE, AI_SCORE)

        if utility > max_utility:
            max_child, max_utility = child, utility

    return max_child, max_utility


def minimize(board, k, HUMAN_SCORE, AI_SCORE):
    if not (board == 0).any() or k == 0:
        return None, evaluate(board, HUMAN_PLAYER, HUMAN_SCORE, AI_SCORE)
    k -= 1
    (min_child, min_utility) = (None, inf)

    for child in generate_children(board, HUMAN_PLAYER):
        (temp_child, utility) = maximize(child, k, HUMAN_SCORE, AI_SCORE)

        if utility < min_utility:
            min_child, min_utility = child, utility

    return min_child, min_utility


def minmax(board, k):
    (child, utility) = maximize(board, k, check_board(board, HUMAN_PLAYER), check_board(board, AI_PLAYER))
    print(child)
    print("util = " + str(utility))
    return child


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


def minimax(node, depth, piece):
    # TODO: return column of the node
    if depth == 0 or is_terminal(node):
        return evaluate(node)
    if piece == AI_PLAYER:
        value = -math.inf
        for child in generate_children(node, piece):
            value = max(value, minimax(child, depth - 1, HUMAN_PLAYER))
        return value
    else:
        value = math.inf
        for child in generate_children(node, piece):
            value = min(value, minimax(child, depth - 1, AI_PLAYER))
        return value

def print_board(board):
    print(np.flip(board, 0))
# board = [[0, 0, 0, 0, 0, 0, 0],
#          [0, 0, 0, 0, 0, 0, 0],
#          [0, 0, 0, 0, 0, 0, 0],
#          [0, 0, 0, 0, 0, 0, 0],
#          [0, 0, 0, 0, 0, 0, 0],
#          [0, 1, 2, 0, 0, 0, 0]]
# #
# board = np.array(board)
# #
# # board[1][1] = 2
# # board[5][0] = 1
# # board[3][2] = 1
# # board[4][4] = 2
# # board[3][6] = 1
# # board[3][3] = 2
# # board[2][2] = 2
# print(board)
# # print("---------------------------------------------")
# # generate_children(board,PLAYER_1)
# print(minmax(board, 2))
# print(generate_children(board, PLAYER_1))