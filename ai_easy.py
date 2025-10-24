import random

# ==================================================
#  File: caro_easy.py
#  Người viết: Thanh Sơn – Nhóm 5 (Caro Bot)
#  Mô tả:
#     AI cấp độ DỄ – có khả năng chặn nước thắng của đối thủ.
#     Nếu không có mối nguy, AI chọn ngẫu nhiên một ô trống.
# ==================================================

def check_winner(board, row, col, mark):
    """Kiểm tra xem người chơi mark có thắng sau nước đi (row, col) không."""
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    size = len(board)
    for dx, dy in directions:
        count = 1
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
        if count >= 5:
            return True
    return False


def ai_easy_move(board, mark):
    """
    AI cấp độ dễ:
    - Nếu đối thủ sắp thắng -> chặn lại.
    - Nếu không -> chọn ô trống ngẫu nhiên.
    """
    size = len(board)
    opponent = "O" if mark == "X" else "X"

    # 1️⃣ Duyệt toàn bộ bàn cờ -> nếu đối thủ sắp thắng thì chặn
    for i in range(size):
        for j in range(size):
            if board[i][j] == "":
                board[i][j] = opponent
                if check_winner(board, i, j, opponent):
                    board[i][j] = ""
                    print(f"[AI dễ] Chặn đối thủ tại ({i}, {j})")
                    return i, j
                board[i][j] = ""

    # 2️⃣ Nếu không có nước cần chặn -> đánh ngẫu nhiên
    empty_cells = [(i, j) for i in range(size) for j in range(size) if board[i][j] == ""]
    if empty_cells:
        move = random.choice(empty_cells)
        print(f"[AI dễ] Đánh ngẫu nhiên tại {move}")
        return move

    # 3️⃣ Không còn ô trống
    return None


# ==================================================
#  Kiểm thử nhanh
# ==================================================
if __name__ == "__main__":
    test_board = [
        ["X", "X", "X", "X", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""]
    ]
    move = ai_easy_move(test_board, "O")
    print("AI chọn nước đi:", move)
