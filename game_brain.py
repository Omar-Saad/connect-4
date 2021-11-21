from math import inf

from heurestic import evaluate
from variables import *


def create_board():
    board = np.zeros((ROWS, COL), dtype=np.uint8)
    return board


def drop(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROWS - 1][col] == EMPTY


def get_next(board, col):
    for row in range(ROWS):
        if board[row][col] == EMPTY:
            return row


def check_board(board, piece):
    horizontal_window = np.array([[1, 1, 1, 1]], dtype=np.uint8)
    vertical_window = np.transpose(horizontal_window)
    diagonal_window = np.eye(4, dtype=np.uint8)
    inv_diagonal_window = np.fliplr(diagonal_window)
    winning_windows = [horizontal_window, vertical_window, diagonal_window, inv_diagonal_window]
    for window in winning_windows:
        conv = scipy.signal.convolve(board == piece, window, mode="valid")
        # TODO :    count 4 in conv
        if (conv == 4).any():
            return True
    return False


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
    children = []
    for child in generate_possible_moves(board):
        temp = np.copy(board)
        drop(temp, child[0], child[1], piece)
        # print(temp)
        # print("---------------------")
        children.append(temp)

    return children


def maximize(board, k):
    if not (board == 0).any() or k == 0:
        return None, evaluate(board)

    (max_child, max_utiility) = (None, inf)

    for child in generate_children(board, PLAYER_1):
        (temp_child, utility) = maximize(child, k - 1)

        if utility > max_utiility:
            max_child, max_utiility = child, utility

    return max_child, max_utiility


def minimize(board, k):
    if not (board == 0).any() or k == 0:
        return None, evaluate(board)

    (min_child, min_utiility) = (None, inf)

    for child in generate_children(board, PLAYER_1):
        (temp_child, utility) = maximize(child, k - 1)

        if utility < min_utiility:
            min_child, min_utiility = child, utility

    return min_child, min_utiility


def minmax(board, k):
    (child, utility) = maximize(board, k)
    return child

def print_board(board):
    print(board)


board = [[0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 1, 2, 0, 0, 0, 0]]

board = np.array(board)
#
# board[1][1] = 2
# board[5][0] = 1
# board[3][2] = 1
# board[4][4] = 2
# board[3][6] = 1
# board[3][3] = 2
# board[2][2] = 2
# print(board)
print("---------------------------------------------")
print(minmax(board, 1))
# print(generate_children(board, PLAYER_1))
