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


def print_board(board):
    print(np.flip(board, 0))
