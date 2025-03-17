# Tic Tac Toe - Pygame

## Mô tả
Tic Tac Toe, viết bằng Python, dùng Pygame. Thêm chế đọ chơi với máy:
- **Chế độ 2 người chơi**: Hai người chơi thay phiên nhau đánh "X" và "O".
- **Chế độ chơi với Bot**: Người chơi đi trước với "O", bot sẽ chơi với "X" và có chiến lược cơ bản.

---

## Cài đặt và chạy chương trình

1. Cài đặt thư viện Pygame nếu chưa có:
   ```bash
   pip install pygame
   ```
   

---

## Cấu trúc mã nguồn

### 1. Import thư viện và khởi tạo Pygame

```python
import pygame
import random
pygame.init()
```

- **pygame**: Thư viện chính để tạo giao diện trò chơi.
- **random**: Dùng để chọn nước đi ngẫu nhiên cho bot.
- **pygame.init()**: Khởi tạo Pygame.

### 2. Thiết lập cửa sổ trò chơi
```python
WIDTH, HEIGHT = 300, 450
... (các biến màu sắc, font chữ, kích thước, ...)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(WHITE)
```
- Thiết lập kích thước cửa sổ 300x450 pixel.
- Đặt tiêu đề "Tic Tac Toe".
- Tô màu nền trắng.

---

### 3. Các hàm vẽ giao diện

#### **Vẽ các đường chia ô**
```python
def draw_lines():
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, BLACK, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, BLACK, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, WIDTH), LINE_WIDTH)
```
- Vẽ các đường ngang và dọc để chia thành bảng 3x3.

#### **Vẽ X và O trên bảng**
```python
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
```
- Duyệt qua từng ô trong bảng để vẽ "X" và "O" nếu ô đó đã được đánh.

#### **Vẽ đường thắng**
```python
def draw_winning_line():
    if winning_line:
        pygame.draw.line(screen, RED, winning_line[0], winning_line[1], 10)
```
- Nếu có người thắng, vẽ đường gạch đỏ để đánh dấu đường thắng.

---

### 4. Kiểm tra trạng thái trò chơi

#### **Kiểm tra người thắng**
```python
def check_winner():
    global winning_line
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] != " ":
            winning_line = [(0, row * SQUARE_SIZE + SQUARE_SIZE // 2), (WIDTH, row * SQUARE_SIZE + SQUARE_SIZE // 2)]
            return board[row][0]
    ... (kiểm tra cột và đường chéo)
```
- Kiểm tra từng hàng, cột và đường chéo để xác định người thắng.

#### **Kiểm tra bảng có đầy chưa**
```python
def is_full():
    return all(board[row][col] != " " for row in range(BOARD_ROWS) for col in range(BOARD_COLS))
```
- Nếu không còn ô trống, trò chơi kết thúc hòa.

#### **Khởi động lại trò chơi**
```python
def restart_game():
    global board, player, winner, winning_line
    board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    player = starting_player
    winner = None
    winning_line = None
    screen.fill(WHITE)
    draw_lines()
```
- Reset lại bảng, người chơi và màn hình.

---

### 5. Xử lý bot chơi

#### **Tìm nước đi tốt nhất**
```python
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
```
- Kiểm tra xem có thể thắng ngay không, hoặc chặn nước đi thắng của đối thủ.

#### **Chiến lược của bot**
```python
def bot_move():
    # 1. Kiểm tra nước đi thắng
    move = find_winning_move("X")
    if move:
        board[move[0]][move[1]] = "X"
        return True
    # 2. Chặn đối thủ
    move = find_winning_move("O")
    if move:
        board[move[0]][move[1]] = "X"
        return True
    # 3. Ưu tiên trung tâm
    if board[1][1] == " ":
        board[1][1] = "X"
        return True
    # 4. Chọn góc
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    for row, col in corners:
        if board[row][col] == " ":
            board[row][col] = "X"
            return True
    # 5. Nếu không có góc, chọn cạnh
    ...
```
- Bot ưu tiên đánh vào trung tâm, sau đó các góc, rồi mới đến cạnh.
- Tối ưu nước đi để thắng và chặn.

---

## Tổng kết
- **Tic Tac Toe** hỗ trợ chơi với bot hoặc hai người chơi.
- Bot có chiến lược thông minh để tăng độ khó.
