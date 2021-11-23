from variables import *


def check_for_streak(state, piece, streak):
    count = 0
    for i in range(6):
        for j in range(7):
            if state[i][j] == piece:
                count += vertical_streak(i, j, state, streak)
                count += horizontal_streak(i, j, state, streak)
                count += diagonal_check(i, j, state, streak)
    return count


def vertical_streak(row, column, state, streak):
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


def horizontal_streak(row, column, state, streak):
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
    my_fours = check_for_streak(state, AI_PLAYER, 4) % 7
    my_threes = check_for_streak(state, AI_PLAYER, 3)
    my_twos = check_for_streak(state, AI_PLAYER, 2)

    comp_fours = check_for_streak(state, HUMAN_PLAYER, 4) % 7
    comp_threes = check_for_streak(state, HUMAN_PLAYER, 3)
    comp_twos = check_for_streak(state, HUMAN_PLAYER, 2)

    score = 0

    if my_fours >= 1:
        score += 250 * my_fours
    elif my_threes >= 1:
        score += 125
    elif my_twos >= 1:
        score += 60

    if comp_fours >= 1:
        score -= 230 * comp_fours
    elif comp_threes >= 1:
        score -= 100
    elif comp_twos >= 1:
        score -= 40

    # if my_fours>=1:
    #     return 1000
    # elif comp_fours>=1:
    #     return -1000
    # elif comp_threes>=1:
    #     return -800
    #
    return score
    # return (my_fours * 10 + my_threes * 5 + my_twos * 2) - (comp_fours * 10 + comp_threes * 5 + comp_twos * 2)
