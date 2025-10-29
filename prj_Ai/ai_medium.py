import random

# ==================================================
#  File: ai_medium.py
#  Mô tả: Bot Caro cấp độ Trung bình
#  Người viết: Thanh Sơn – Nhóm 5 (Caro Bot)
# ==================================================

def check_winner(board, row, col, mark):
    """Kiểm tra thắng 5 quân liên tiếp."""
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    size = len(board)
    for dx, dy in directions:
        count = 1
        # đếm xuôi
        i, j = row + dx, col + dy
        while 0 <= i < size and 0 <= j < size and board[i][j] == mark:
            count += 1
            i += dx
            j += dy
        # đếm ngược
        i, j = row - dx, col - dy
        while 0 <= i < size and 0 <= j < size and board[i][j] == mark:
            count += 1
            i -= dx
            j -= dy
        if count >= 5:
            return True
    return False


# ==================================================
#  Hàm tính điểm heuristic cho từng ô
# ==================================================
def evaluate_position(board, row, col, mark):
    """
    Tính điểm cho ô (row, col) dựa trên:
    - Số quân liên tiếp của mình (tấn công)
    - Số quân liên tiếp của đối thủ (phòng thủ)
    """
    if board[row][col] != "":
        return -1  # ô đã có quân thì bỏ qua

    size = len(board)
    opponent = "O" if mark == "X" else "X"
    score = 0

    # Hướng 4 chiều
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    for dx, dy in directions:
        # ---- Tấn công ----
        count = 0
        i, j = row + dx, col + dy
        while 0 <= i < size and 0 <= j < size and board[i][j] == mark:
            count += 1
            i += dx
            j += dy
        i, j = row - dx, col - dy
        while 0 <= i < size and 0 <= j < size and board[i][j] == mark:
            count += 1
            i -= dx
            j -= dy

        if count >= 4:
            score += 10000
        elif count == 3:
            score += 500
        elif count == 2:
            score += 100
        elif count == 1:
            score += 10

        # ---- Phòng thủ ----
        count = 0
        i, j = row + dx, col + dy
        while 0 <= i < size and 0 <= j < size and board[i][j] == opponent:
            count += 1
            i += dx
            j += dy
        i, j = row - dx, col - dy
        while 0 <= i < size and 0 <= j < size and board[i][j] == opponent:
            count += 1
            i -= dx
            j -= dy

        if count >= 4:
            score += 9000
        elif count == 3:
            score += 400
        elif count == 2:
            score += 80
        elif count == 1:
            score += 8

    return score


# ==================================================
#  AI Medium: chọn ô có điểm cao nhất
# ==================================================
def ai_medium_move(board, mark):
    """
    AI cấp trung bình:
    - Duyệt toàn bộ bàn cờ.
    - Tính điểm từng ô theo tấn công + phòng thủ.
    - Chọn ô có điểm cao nhất.
    """
    size = len(board)
    best_score = -1
    best_moves = []

    for i in range(size):
        for j in range(size):
            score = evaluate_position(board, i, j, mark)
            if score > best_score:
                best_score = score
                best_moves = [(i, j)]
            elif score == best_score:
                best_moves.append((i, j))

    if not best_moves:
        return None

    # Chọn ngẫu nhiên trong các nước có điểm cao nhất
    move = random.choice(best_moves)
    print(f"[AI Trung bình] Chọn ô {move} với điểm {best_score}")
    return move


# ==================================================
#  Kiểm thử nhanh
# ==================================================
if __name__ == "__main__":
    test_board = [
        ["X", "O", "X", "", ""],
        ["O", "X", "", "", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""]
    ]
    move = ai_medium_move(test_board, "O")
    print("AI Trung bình chọn nước đi:", move)
