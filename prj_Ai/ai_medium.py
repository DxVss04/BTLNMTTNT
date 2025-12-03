import random

# ==================================================
# File: ai_medium.py
# Mô tả: Bot Caro cấp độ Trung bình
# Người viết: Thanh Sơn – Nhóm 5 (Caro Bot)
# ==================================================

def evaluate_position(board, row, col, mark, game):
    """
    Tính điểm cho ô (row, col)
    Tham số game được truyền từ main để dùng game.check_win()
    """
    if board[row][col] != "":
        return -1  # ô đã có quân thì bỏ qua

    size = len(board)
    opponent = "O" if mark == "X" else "X"
    score = 0
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    for dx, dy in directions:
        # ---- TẤN CÔNG ----
        my_count = 0
        i, j = row + dx, col + dy
        while 0 <= i < size and 0 <= j < size and board[i][j] == mark:
            my_count += 1
            i += dx
            j += dy
        i, j = row - dx, col - dy
        while 0 <= i < size and 0 <= j < size and board[i][j] == mark:
            my_count += 1
            i -= dx
            j -= dy

        # ---- PHÒNG THỦ ----
        opp_count = 0
        i, j = row + dx, col + dy
        while 0 <= i < size and 0 <= j < size and board[i][j] == opponent:
            opp_count += 1
            i += dx
            j += dy
        i, j = row - dx, col - dy
        while 0 <= i < size and 0 <= j < size and board[i][j] == opponent:
            opp_count += 1
            i -= dx
            j -= dy

        # ƯU TIÊN CAO NHẤT: Thắng ngay hoặc chặn thắng ngay
        if my_count + 1 >= 5:    # Đánh vào đây sẽ có 5
            return 999_999_999
        if opp_count + 1 >= 5:   # Phải chặn ngay!
            return 999_999_998

        # Điểm tấn công
        if my_count >= 4:   score += 100000
        elif my_count == 3: score += 5000
        elif my_count == 2: score += 500
        elif my_count == 1: score += 50

        # Điểm phòng thủ
        if opp_count >= 4:   score += 90000
        elif opp_count == 3: score += 4000
        elif opp_count == 2: score += 400
        elif opp_count == 1: score += 40

    # Ưu tiên đánh gần tâm bàn cờ
    center = size // 2
    distance = abs(row - center) + abs(col - center)
    score += (50 - distance)

    return score


def ai_medium_move(board, mark, game):
    """
    AI cấp trung bình:
    - Tính điểm từng ô trống
    - Chọn ô có điểm cao nhất
    - game: đối tượng GameLogic được truyền từ main.py
    """
    size = len(board)
    best_score = -999_999_999
    best_moves = []

    for i in range(size):
        for j in range(size):
            if board[i][j] == "":
                score = evaluate_position(board, i, j, mark, game)
                if score > best_score:
                    best_score = score
                    best_moves = [(i, j)]
                elif score == best_score:
                    best_moves.append((i, j))

    if not best_moves:
        return None

    # Chọn ngẫu nhiên trong số nước tốt nhất
    move = random.choice(best_moves)
    print(f"[AI Trung bình] Chọn ô {move} với điểm {best_score}")
    return move


# ==================================================
# Kiểm thử nhanh (chỉ dùng khi chạy riêng file này)
# ==================================================
if __name__ == "__main__":
    from logic import GameLogic
    
    test_board = [[""] * 15 for _ in range(15)]
    # Tạo tình huống đẹp để test
    test_board[7][7] = "X"
    test_board[7][8] = "X"
    test_board[7][9] = "X"
    test_board[7][10] = "X"  # X có 4 → O phải chặn hoặc tạo thế mạnh

    game = GameLogic(board_size=15)
    game.board = test_board

    move = ai_medium_move(test_board, "O", game)
    print("AI Trung bình chọn nước đi:", move)
