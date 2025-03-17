import pygame
import random

pygame.init()

# Cài đặt cửa sổ
WIDTH, HEIGHT = 300, 450 
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 5
CROSS_WIDTH = 5
SPACE = SQUARE_SIZE // 4 

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(WHITE)

font = pygame.font.Font(None, 36)

BUTTON_WIDTH, BUTTON_HEIGHT = 120, 40
PLAY_WITH_BOT_BUTTON = pygame.Rect(20, HEIGHT - 100, BUTTON_WIDTH, BUTTON_HEIGHT)  
TWO_PLAYER_BUTTON = pygame.Rect(160, HEIGHT - 100, BUTTON_WIDTH, BUTTON_HEIGHT)


#Function

#line bàn cờ
def draw_lines():
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, BLACK, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, BLACK, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, WIDTH), LINE_WIDTH)

#X O
def draw_xo():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == "X":
                pygame.draw.line(screen, RED, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 ((col + 1) * SQUARE_SIZE - SPACE, (row + 1) * SQUARE_SIZE - SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, RED, ((col + 1) * SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SPACE, (row + 1) * SQUARE_SIZE - SPACE), CROSS_WIDTH)
            elif board[row][col] == "O":
                pygame.draw.circle(screen, BLACK, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), CIRCLE_RADIUS, CIRCLE_WIDTH)

#winning line
def draw_winning_line():
    if winning_line:
        pygame.draw.line(screen, RED, winning_line[0], winning_line[1], 10)  # Vẽ đường gạch thắng

#check win 
def check_winner():
    global winning_line
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] != " ":
            winning_line = [(0, row * SQUARE_SIZE + SQUARE_SIZE // 2), (WIDTH, row * SQUARE_SIZE + SQUARE_SIZE // 2)]
            return board[row][0]

    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] != " ":
            winning_line = [(col * SQUARE_SIZE + SQUARE_SIZE // 2, 0), (col * SQUARE_SIZE + SQUARE_SIZE // 2, WIDTH)]
            return board[0][col]

    if board[0][0] == board[1][1] == board[2][2] != " ":
        winning_line = [(0, 0), (WIDTH, WIDTH)]
        return board[0][0]

    if board[0][2] == board[1][1] == board[2][0] != " ":
        winning_line = [(WIDTH, 0), (0, WIDTH)]
        return board[0][2]

    return None

def is_full():
    return all(board[row][col] != " " for row in range(BOARD_ROWS) for col in range(BOARD_COLS))

def restart_game():
    global board, player, winner, winning_line
    board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    player = starting_player
    winner = None
    winning_line = None
    screen.fill(WHITE)
    draw_lines()

def display_winner(text):
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT - 50))  # Hiển thị thông báo phía trên nút
    pygame.display.update()
    pygame.time.wait(2000)  # Hiển thị thông báo trong 2 giây
    restart_game()  # Tự động khởi động lại trò chơi sau khi hiển thị thông báo

def draw_buttons():
    # Vẽ nút "Play with Bot"
    pygame.draw.rect(screen, GREEN if game_mode == "bot" else GRAY, PLAY_WITH_BOT_BUTTON, border_radius=10)
    text_bot = font.render("BOT", True, WHITE)
    # Căn giữa chữ trong nút
    text_x = PLAY_WITH_BOT_BUTTON.x + (PLAY_WITH_BOT_BUTTON.width - text_bot.get_width()) // 2
    text_y = PLAY_WITH_BOT_BUTTON.y + (PLAY_WITH_BOT_BUTTON.height - text_bot.get_height()) // 2
    screen.blit(text_bot, (text_x, text_y))

    # Vẽ nút "2 Player"
    pygame.draw.rect(screen, GREEN if game_mode == "2player" else GRAY, TWO_PLAYER_BUTTON, border_radius=10)
    text_2p = font.render("2 PLAYER", True, WHITE)
    # Căn giữa chữ trong nút
    text_x = TWO_PLAYER_BUTTON.x + (TWO_PLAYER_BUTTON.width - text_2p.get_width()) // 2
    text_y = TWO_PLAYER_BUTTON.y + (TWO_PLAYER_BUTTON.height - text_2p.get_height()) // 2
    screen.blit(text_2p, (text_x, text_y))

def find_winning_move(player):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == " ":
                board[row][col] = player
                if check_win(player):
                    board[row][col] = " "
                    return (row, col)
                board[row][col] = " "
    return None

def check_win(player):
    for row in range(BOARD_ROWS):
        if all(board[row][col] == player for col in range(BOARD_COLS)):
            return True
    for col in range(BOARD_COLS):
        if all(board[row][col] == player for row in range(BOARD_ROWS)):
            return True
    if all(board[i][i] == player for i in range(BOARD_ROWS)) or all(board[i][BOARD_ROWS - 1 - i] == player for i in range(BOARD_ROWS)):
        return True
    return False
"""
ĐI TRƯỚC:
    Luôn đi nước đầu tiên vào trung tâm (nếu có thể).

    Nếu trung tâm đã bị đối thủ chọn trước, hãy đi vào một góc.

    Nếu đối thủ đi vào góc đối diện, hãy kiểm soát hàng hoặc cột.

    Luôn chặn đối thủ khi họ sắp thắng.

    Nếu đối thủ có hai dấu liên tiếp với ô trống còn lại trên hàng/cột/đường chéo => chặn.
_________________________________
ĐI SAU:
    Nếu đối thủ đi trung tâm trước, hãy chọn một góc.

    Nếu đối thủ đi vào góc, hãy đi trung tâm ngay lập tức.

"""

def bot_move():
    available_moves = [(row, col) for row in range(BOARD_ROWS) for col in range(BOARD_COLS) if board[row][col] == " "]
    if not available_moves:
        return False
    
    # 1. Kiểm tra xem có thể thắng ngay không
    move = find_winning_move("X")
    if move:
        board[move[0]][move[1]] = "X"
        return True
    
    # 2. Chặn đối thủ nếu họ sắp thắng
    move = find_winning_move("O")
    if move:
        board[move[0]][move[1]] = "X"
        return True
    
    # 3. Ưu tiên đi vào trung tâm nếu trống
    if board[1][1] == " ":
        board[1][1] = "X"
        return True
    
    # 4. Ưu tiên chọn một trong bốn góc
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    random.shuffle(corners)
    for row, col in corners:
        if board[row][col] == " ":
            board[row][col] = "X"
            return True
    
    # 5. Nếu không có góc, chọn cạnh bất kỳ
    edges = [(0, 1), (1, 0), (1, 2), (2, 1)]
    random.shuffle(edges)
    for row, col in edges:
        if board[row][col] == " ":
            board[row][col] = "X"
            return True
    
    return False  # Không có nước đi nào khả dụng

# Khởi tạo trò chơi
draw_lines()
board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
player = "X"
winner = None
winning_line = None
game_mode = "2player"  # Mặc định là chế độ 2 người chơi
starting_player = "O"  # Người chơi luôn đánh trước khi chơi với bot
running = True

while running:
    screen.fill(WHITE)
    draw_lines()
    draw_xo()
    draw_winning_line()  # Vẽ đường gạch thắng
    draw_buttons()

    if winner:
        display_winner(f"Player {winner} wins!" if winner != "Tie" else "It's a tie!")
        # Sau khi hiển thị thông báo, trò chơi sẽ tự động khởi động lại

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()

            # Kiểm tra nếu nhấn vào nút chế độ chơi
            if PLAY_WITH_BOT_BUTTON.collidepoint(x, y):
                game_mode = "bot"
                starting_player = "O"  # Người chơi luôn đánh trước khi chơi với bot
                restart_game()
            elif TWO_PLAYER_BUTTON.collidepoint(x, y):
                game_mode = "2player"
                starting_player = "X"  # Reset về X đánh trước khi chơi 2 người
                restart_game()

            # Kiểm tra nếu nhấn vào bảng trò chơi
            elif y < WIDTH:
                row = y // SQUARE_SIZE
                col = x // SQUARE_SIZE
                if board[row][col] == " ":
                    if game_mode == "bot":
                        # Người chơi đánh "O"
                        board[row][col] = "O"
                        winner = check_winner()
                        if winner:
                            screen.fill(WHITE)
                            draw_lines()
                            draw_xo()
                            draw_winning_line()
                            display_winner(f"Player {winner} wins!" if winner != "Tie" else "It's a tie!")
                        elif is_full():
                            screen.fill(WHITE)
                            draw_lines()
                            draw_xo()
                            display_winner("It's a tie!")
                        else:
                            # Cập nhật màn hình ngay sau khi người chơi đánh "O"
                            screen.fill(WHITE)
                            draw_lines()
                            draw_xo()
                            draw_winning_line()
                            draw_buttons()
                            pygame.display.update()

                            # Thêm độ trễ trước khi bot đánh "X"
                            pygame.time.wait(700)

                            # Bot đánh "X"
                            if bot_move():
                                winner = check_winner()
                                if winner:
                                    screen.fill(WHITE)
                                    draw_lines()
                                    draw_xo()
                                    draw_winning_line()
                                    display_winner(f"Player {winner} wins!" if winner != "Tie" else "It's a tie!")
                                elif is_full():
                                    screen.fill(WHITE)
                                    draw_lines()
                                    draw_xo()
                                    display_winner("It's a tie!")
                    else:
                        # Chế độ 2 người chơi
                        board[row][col] = player
                        winner = check_winner()
                        if winner:
                            screen.fill(WHITE)
                            draw_lines()
                            draw_xo()
                            draw_winning_line()
                            display_winner(f"Player {winner} wins!" if winner != "Tie" else "It's a tie!")
                        elif is_full():
                            screen.fill(WHITE)
                            draw_lines()
                            draw_xo()
                            display_winner("It's a tie!")
                        player = "O" if player == "X" else "X"

pygame.quit()
