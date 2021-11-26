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
    base_font = pygame.font.Font(None, 32)

    label_k = base_font.render("K", False, (255, 255, 0))
    screen.blit(label_k, (COL * SQUARE_SIZE + 20, 100))

    # Add default value for K
    k = 4
    user_text = '' + str(k)
    # create rectangle
    input_rect = pygame.Rect(COL * SQUARE_SIZE + 20, 130, 120, 32)

    # color_active stores color(lightskyblue3) which
    # gets active when input box is clicked by user
    color_active = pygame.Color('lightskyblue3')

    # color_passive store color(chartreuse4) which is
    # color of input box.
    color_passive = pygame.Color('chartreuse4')
    input_box_color = color_passive
    active = False



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

                if event.pos[0] < COL * SQUARE_SIZE - SQUARE_SIZE // 2:
                    if turn == HUMAN_TURN:
                        pygame.draw.circle(screen, RED,
                                           (position, SQUARE_SIZE // 2),
                                           (SQUARE_SIZE // 2) - 5)

            if event.type == pygame.MOUSEBUTTONDOWN:

                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                if event.pos[0] < COL * SQUARE_SIZE - SQUARE_SIZE // 2:
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
                print("k = " + str(k))
                col, score = minimax(board, k, True, AI)

                if is_valid_location(board, col).any():
                    row = get_next_row(board, col)
                    print(col, score)
                    drop(board, row, col, AI)
                # >>>>>>> main
                turn += 1
                turn = turn % 2

            if event.type == pygame.KEYDOWN:

                # Check for backspace
                if event.key == pygame.K_BACKSPACE:

                    # get text input from 0 to -1 i.e. end.
                    user_text = user_text[:-1]

                # Unicode standard is used for string
                # formation
                else:
                    user_text += event.unicode

            if active:
                input_box_color = color_active
            else:
                input_box_color = color_passive

            pygame.draw.rect(screen, input_box_color, input_rect)
            text_surface = base_font.render(user_text, True, (255, 255, 255))

            # render at position stated in arguments
            screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

            # set width of textfield so that text cannot get
            # outside of user's text input
            input_rect.w = max(100, text_surface.get_width() + 10)

            # display.flip() will update only a portion of the
            # screen to updated, not full area
            pygame.display.flip()

            if user_text.isdigit():
                k = int(user_text)

            label_human_score = base_font.render("Human : " + str(check_board(board, HUMAN)), True, (0, 0, 0),
                                                 (255, 255, 0))
            screen.blit(label_human_score, (COL * SQUARE_SIZE + 20, 180))
            label_ai_score = base_font.render("Ai : " + str(check_board(board, AI)), True, (0, 0, 0), (255, 255, 0))
            screen.blit(label_ai_score, (COL * SQUARE_SIZE + 20, 220))


            if not len(get_valid_location(board)):
                game_over = True
                score_1 = check_board(board, HUMAN)
                score_2 = check_board(board, AI)
                print(score_1, score_2)

                pygame.time.wait(3000)

            pygame.display.update()
