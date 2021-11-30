import os
import time

from game_brain import *
from gui import *


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


total_average_time = 0
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    base_font = pygame.font.Font(None, 32)

    label_pruning = base_font.render("Pruning", True, (255, 255, 0))
    screen.blit(label_pruning, (COL * SQUARE_SIZE + 20, 300))
    pruning = True
    input_rect_1 = pygame.Rect(COL * SQUARE_SIZE + 20, 330, 120, 32)
    input_rect_2 = pygame.Rect(COL * SQUARE_SIZE + 20, 365, 120, 32)

    label_k = base_font.render("K", True, (255, 255, 0))
    screen.blit(label_k, (COL * SQUARE_SIZE + 20, 100))
    # Add default value for K
    k = 4
    user_text = '' + str(k)
    # create rectangle
    input_rect = pygame.Rect(COL * SQUARE_SIZE + 20, 130, 120, 32)

    # color_active stores color(light sky blue 3) which
    # gets active when input box is clicked by user
    color_active = pygame.Color('lightskyblue3')

    # color_passive store color(chartreuse4) which is
    # color of input box.
    color_passive = pygame.Color('chartreuse4')
    input_box_color = color_passive
    rect_1_color = color_active
    rect_2_color = color_passive
    active = False

    game_over = False
    board = create_board()
    # Choosing random player to start the game

    turn = random.randint(HUMAN_TURN, AI_TURN)
    score_1 = score_2 = 0
    while not game_over:
        # TODO screen to choose difficulty and puring option and start playing with constant k
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

                if input_rect_1.collidepoint(event.pos):
                    pruning = True
                    rect_1_color = color_active
                    rect_2_color = color_passive
                elif input_rect_2.collidepoint(event.pos):
                    pruning = False
                    rect_1_color = color_passive
                    rect_2_color = color_active

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
                start_time = time.time()
                col, score = minimax(board, k, pruning, AI)
                end_time = time.time()
                total_average_time += end_time - start_time
                print_tree(k)
                print("Min-Max Running Time = " + str(end_time - start_time))

                if is_valid_location(board, col).any():
                    row = get_next_row(board, col)
                    drop(board, row, col, AI)
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

            pygame.draw.rect(screen, rect_1_color, input_rect_1)
            pygame.draw.rect(screen, rect_2_color, input_rect_2)
            text_surface_1 = base_font.render("True", True, (255, 255, 255))
            text_surface_2 = base_font.render("False", True, (255, 255, 255))

            # render at position stated in arguments
            screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
            screen.blit(text_surface_1, (input_rect_1.x + 5, input_rect_1.y + 5))
            screen.blit(text_surface_2, (input_rect_2.x + 5, input_rect_2.y + 5))

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
            label_ai_score = base_font.render("AI : " + str(check_board(board, AI)), True, (0, 0, 0), (255, 255, 0))
            screen.blit(label_ai_score, (COL * SQUARE_SIZE + 20, 220))

            if not len(get_valid_location(board)):
                game_over = True
                score_1 = check_board(board, HUMAN)
                score_2 = check_board(board, AI)
                print(score_1, score_2)
                # TODO new Screen for game over or wining and play again
                pygame.time.wait(3000)

            pygame.display.update()
    pygame.quit()
    print("------------------------------------------------------------------")
    if score_1 > score_2:
        print("CONGRATULATION YOU HAVE WON")
    elif score_1 < score_2:
        print("YOU HAVE LOST")
    else:
        print("DRAW")
    print(f"Average time per play = {(total_average_time / 21)}")

    restart_game_choice = input("\nPlay Again?\nAnswer (Y,N): ")
    if restart_game_choice.upper() == "N":
        print("Thank You for your time")
    elif restart_game_choice.upper() == "Y":
        os.system("python main.py")
