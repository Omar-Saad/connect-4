from game_brain import *


def draw_board(board):
    for col in range(COL):
        for row in range(ROWS):
            pygame.draw.rect(screen, BLUE,
                             pygame.Rect(
                                 (SQUARE_SIZE * col, SQUARE_SIZE * row + SQUARE_SIZE),
                                 (SQUARE_SIZE, SQUARE_SIZE)))
            pygame.draw.circle(screen, BLACK,
                               (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                row * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE // 2),
                               (SQUARE_SIZE // 2) - 5)
    for col in range(COL):
        for row in range(ROWS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, RED,
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                    HEIGHT - row * SQUARE_SIZE - SQUARE_SIZE // 2),
                                   (SQUARE_SIZE // 2) - 5)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, YELLOW,
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                    HEIGHT - row * SQUARE_SIZE - SQUARE_SIZE // 2),
                                   (SQUARE_SIZE // 2) - 5)
    pygame.display.update()


if __name__ == '__main__':

    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    game_over = False
    board = create_board()
    # Choosing random player to start the game
    turn = random.randint(HUMAN_TURN, AI_TURN)

    score_1 = score_2 = 0
    while not game_over:
        draw_board(board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.display.update()
                position = event.pos[0]
                pygame.draw.rect(screen, BLACK,
                                 pygame.Rect(
                                     (0, 0),
                                     (WIDTH, SQUARE_SIZE)))

                if turn == HUMAN_TURN:
                    pygame.draw.circle(screen, RED,
                                       (position, SQUARE_SIZE // 2),
                                       (SQUARE_SIZE // 2) - 5)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_x = event.pos[0]
                col = pos_x // SQUARE_SIZE

                if turn == HUMAN_TURN:
                    if is_valid_location(board, col):
                        row = get_next_row(board, col)
                        drop(board, row, col, HUMAN)
                        turn += 1
                        turn = turn % 2

            if turn == AI_TURN:
                # <<<<<<< omar
                # GET the next move from min-max (New Board)
                # board = minmax(board, 3)
                # pygame.time.wait(200)
                # 2nd method
                col, score = minimax(board, 6, True, -math.inf, math.inf, AI)
                if is_valid_location(board, col):
                    row = get_next_row(board, col)
                    print(col, score)
                    drop(board, row, col, AI)
                # >>>>>>> main
                turn += 1
                turn = turn % 2

            if not len(get_valid_location(board)):
                game_over = True
                score_1 = check_board(board, HUMAN)
                score_2 = check_board(board, AI)
                print(score_1, score_2)

                pygame.time.wait(3000)

            pygame.display.update()
