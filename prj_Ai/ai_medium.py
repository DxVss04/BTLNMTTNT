# ai_medium.py - MỨC TRUNG BÌNH
# Logic: đánh giá điểm tấn công + phòng thủ + ưu tiên gần quân
import random

SIZE = 15

def is_near_occupied(board, x, y):
    """Kiểm tra ô (x,y) có gần ô nào đã có quân không"""
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < SIZE and 0 <= ny < SIZE and board[nx][ny] != 0:
                return True
    return False

def count_consecutive(board, x, y, dx, dy, symbol):
    """Đếm số quân liên tiếp theo hướng (dx,dy) """
    count = 0
    nx, ny = x + dx, y + dy
    while 0 <= nx < SIZE and 0 <= ny < SIZE and board[nx][ny] == symbol:
        count += 1
        nx += dx
        ny += dy
    return count

def is_open_end(board, x, y):
    """Kiểm tra đầu hướng có trống không"""
    return 0 <= x < SIZE and 0 <= y < SIZE and board[x][y] == 0

def evaluate_position(board, x, y, symbol):
    """Đánh giá 1 vị trí theo 4 hướng """
    score = 0
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # ngang, dọc, chéo \, chéo /

    for dx, dy in directions:
        forward = count_consecutive(board, x, y, dx, dy, symbol)
        backward = count_consecutive(board, x, y, -dx, -dy, symbol)
        count = 1 + forward + backward  # +1 là ô chính đang thử
        open_ends = 0

        # Kiểm tra 2 đầu có mở không
        fx, fy = x + (forward + 1) * dx, y + (forward + 1) * dy
        bx, by = x - (backward + 1) * dx, y - (backward + 1) * dy
        if is_open_end(board, fx, fy):
            open_ends += 1
        if is_open_end(board, bx, by):
            open_ends += 1

        if count >= 5:
            score += 10000
        elif count == 4 and open_ends == 2:
            score += 9000
        elif count == 4 and open_ends == 1:
            score += 5000 if symbol == -1 else 4000  # AI (O) được điểm cao hơn
        elif count == 3 and open_ends == 2:
            score += 500 if symbol == -1 else 400
        elif count == 2 and open_ends == 2:
            score += 100 if symbol == -1 else 80
        elif count == 3 and open_ends == 1:
            score += 200 if symbol == -1 else 150
        elif count == 2 and open_ends == 1:
            score += 50 if symbol == -1 else 30

    return score

def evaluate_move(board, x, y):
    """Tính điểm tổng cho nước đi (x,y)"""
    score = 0
    # Tấn công (O)
    score += evaluate_position(board, x, y, -1) * 2   # AI là O (-1)
    # Phòng thủ (X)
    score += evaluate_position(board, x, y, 1)        # Người là X (1)
    # Ưu tiên gần quân đã đánh (+5 điểm)
    if is_near_occupied(board, x, y):
        score += 5
    return score

def ai_medium_move(board_manager, player):
    """
    Trả về nước đi tốt nhất cho AI mức TRUNG BÌNH
    Args:
        board_manager: BoardManager object
        player: -1 (AI - O)
    Returns:
        (row, col) hoặc None
    """
    board = board_manager.board
    best_score = float('-inf')
    best_move = None

    # Duyệt tất cả ô trống → tìm nước có điểm cao nhất
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == 0:
                # Thử đặt tạm để tính điểm
                board[i][j] = player
                score = evaluate_move(board, i, j)
                board[i][j] = 0  # khôi phục

                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    if best_move:
        return best_move

    # Nếu không tìm được (hòa), chọn ngẫu nhiên
    empty = [(i,j) for i in range(SIZE) for j in range(SIZE) if board[i][j] == 0]
    return random.choice(empty) if empty else None


