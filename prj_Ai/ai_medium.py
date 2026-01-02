# ai_medium.py - MỨC TRUNG BÌNH
# Logic: đánh giá điểm tấn công + phòng thủ + ưu tiên gần quân
# dùng hàm _count_consecutive từ BoardManager
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

def is_open_end(board, x, y):
    """Kiểm tra đầu hướng có trống không"""
    return 0 <= x < SIZE and 0 <= y < SIZE and board[x][y] == 0

def evaluate_position(board_manager, x, y, symbol):
    """Đánh giá 1 vị trí theo 4 hướng, dùng _count_consecutive từ BoardManager"""
    score = 0
    board = board_manager.board
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # ngang, dọc, chéo \, chéo /

    for dx, dy in directions:
        # Dùng hàm _count_consecutive từ board_manager để đếm tổng quân liên tiếp (đã bao gồm 2 bên + ô gốc)
        count = board_manager._count_consecutive(x, y, dx, dy, symbol)

        # Tính open_ends: kiểm tra 2 đầu của hàng (cách 1 ô ngoài hàng)
        # Tìm độ dài một bên để biết vị trí đầu
        forward_count = 0
        nx, ny = x + dx, y + dy
        while 0 <= nx < SIZE and 0 <= ny < SIZE and board[nx][ny] == symbol:
            forward_count += 1
            nx += dx
            ny += dy
        backward_count = count - 1 - forward_count  # tổng - gốc - forward = backward

        open_ends = 0
        # Đầu forward
        fx, fy = x + (forward_count + 1) * dx, y + (forward_count + 1) * dy
        if is_open_end(board, fx, fy):
            open_ends += 1
        # Đầu backward
        bx, by = x - (backward_count + 1) * dx, y - (backward_count + 1) * dy
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

def evaluate_move(board_manager, x, y):
    """Tính điểm tổng cho nước đi (x,y)"""
    score = 0
    board = board_manager.board
    # Tấn công (O)
    score += evaluate_position(board_manager, x, y, -1) * 2   # AI là O (-1)
    # Phòng thủ (X)
    score += evaluate_position(board_manager, x, y, 1)        # Người là X (1)
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
                score = evaluate_move(board_manager, i, j)
                board[i][j] = 0  # khôi phục

                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    if best_move:
        return best_move

    # Nếu không tìm được (hòa), chọn ngẫu nhiên
    empty = [(i,j) for i in range(SIZE) for j in range(SIZE) if board[i][j] == 0]
    return random.choice(empty) if empty else None
