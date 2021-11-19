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
    turn = 0
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
                if turn == 0:
                    pygame.draw.circle(screen, RED,
                                       (position, SQUARE_SIZE // 2),
                                       (SQUARE_SIZE // 2) - 5)
                elif turn == 1:
                    pygame.draw.circle(screen, YELLOW,
                                       (position, SQUARE_SIZE // 2),
                                       (SQUARE_SIZE // 2) - 5)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_x = event.pos[0]
                col = pos_x // SQUARE_SIZE
                if turn == 0:
                    if is_valid_location(board, col):
                        row = get_next(board, col)
                        drop(board, row, col, PLAYER_1)

                else:
                    if is_valid_location(board, col):
                        row = get_next(board, col)
                        drop(board, row, col, PLAYER_2)
                print_board(board)
                turn += 1
                turn = turn % 2
            if not (board == 0).any():
                game_over = True
                score_1 = check_board(board, PLAYER_1)
                score_2 = check_board(board, PLAYER_2)

                pygame.time.wait(3000)

            pygame.display.update()
