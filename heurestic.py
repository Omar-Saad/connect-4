
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


def evaluate(state, piece, HUMAN_SCORE, AI_SCORE):
    opp_piece = HUMAN_PLAYER
    opp_score = HUMAN_SCORE
    my_score = AI_SCORE
    if piece == HUMAN_PLAYER:
        opp_piece = AI_PLAYER
        opp_score = AI_SCORE
        my_score = HUMAN_SCORE

    my_fours = check_for_streak(state, piece, 4) - my_score
    my_threes = check_for_streak(state, piece, 3)
    my_twos = check_for_streak(state, piece, 2)

    # #
    opp_fours = check_for_streak(state, opp_piece, 4) - opp_score
    opp_threes = check_for_streak(state, opp_piece, 3)
    opp_twos = check_for_streak(state, opp_piece, 2)

    score = (my_fours * 10000 + my_threes * 100 + my_twos) - (opp_fours * 10000 + opp_threes * 100 + opp_twos)

    # Check if utility =0 than play in the middle
    if score == 0:
        for row in range(ROWS):
            if state[row, COL // 2] == 0:
                score += 10
                break

    # score = 0
    #
    # if my_fours >= 1:
    #     score += inf
    # elif my_threes >= 1:
    #     score += my_threes * 100
    # elif my_twos >= 1:
    #     score += my_twos * 20

    # if opp_fours >= 1:
    #     score -= inf
    # elif opp_threes >= 1:
    #     score -= opp_threes * 100
    # elif opp_twos >= 1:
    #     score -= opp_twos * 20

    # score = score - 4 * Ai_score * 140 + 4* human_score * 140

    # if my_fours>=1:
    #     return 1000
    # elif opp_fours>=1:
    #     return -1000
    # elif opp_threes>=1:
    #     return -800
    #
    # return score
    return score
