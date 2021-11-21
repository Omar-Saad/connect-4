from variables import *


def checkForStreak(state, piece, streak):
    count = 0
    for i in range(6):
        for j in range(7):
            if state[i][j] == piece:
                count += verticalStreak(i, j, state, streak)
                count += horizontalStreak(i, j, state, streak)
                count += diagonal_check(i, j, state, streak)
    return count


def verticalStreak(row, column, state, streak):
    consecutiveCount = 0
    for i in range(row, ROWS):
        if state[i][column] == state[row][column]:
            consecutiveCount += 1
        else:
            break
    if consecutiveCount >= streak:
        return 1
    else:
        return 0


def horizontalStreak(row, column, state, streak):
    consecutiveCount = 0
    for j in range(column, COL):
        if state[row][j] == state[row][column]:
            consecutiveCount += 1
        else:
            break
    if consecutiveCount >= streak:
        return 1
    else:
        return 0


def diagonal_check(row, column, state, streak):
    total = 0
    count = 0
    j = column
    for i in range(row, ROWS):
        if j > 6:
            break
        elif state[i][j] == state[row][column]:
            count += 1
        else:
            break
        j += 1
    if count >= streak:
        total += 1
    count = 0
    j = column
    for i in range(row, -1, -1):
        if j > 6:
            break
        elif state[i][j] == state[row][column]:
            count += 1
        else:
            break
        j += 1
    if count >= streak:
        total += 1
    return total


def evaluate(state):
    my_fours = checkForStreak(state, PLAYER_2, 4)
    my_threes = checkForStreak(state, PLAYER_2, 3)
    my_twos = checkForStreak(state, PLAYER_2, 2)

    comp_fours = checkForStreak(state, PLAYER_1, 4)
    comp_threes = checkForStreak(state, PLAYER_1, 3)
    comp_twos = checkForStreak(state, PLAYER_1, 2)

    return (my_fours * 20 + my_threes * 8 + my_twos * 3) - (comp_fours * 20 + comp_threes * 8 + comp_twos * 3)
