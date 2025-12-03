import random
# ==================================================
# File: caro_easy.py
# Người viết: Thanh Sơn – Nhóm 5 (Caro Bot)
# Mô tả:
# AI cấp độ DỄ – có khả năng chặn nước thắng của đối thủ.
# Nếu không có mối nguy, AI chọn ngẫu nhiên một ô trống.
# ==================================================

def ai_easy_move(board, mark, game):
    """
    AI cấp độ dễ:
    - Nếu đối thủ sắp thắng -> chặn lại.
    - Nếu không -> chọn ô trống ngẫu nhiên.
    """
    size = len(board)
    opponent = "O" if mark == "X" else "X"

    # 1. Kiểm tra và chặn nước thắng của đối thủ
    for i in range(size):
        for j in range(size):
            if board[i][j] == "":
                game.board[i][j] = opponent
                if game.check_win(opponent):        
                    game.board[i][j] = ""           
                    print(f"[AI dễ] Chặn đối thủ tại ({i}, {j})")
                    return i, j
                game.board[i][j] = ""

    # 2. Không có nước cần chặn → đánh ngẫu nhiên
    empty_cells = [(i, j) for i in range(size) for j in range(size) if board[i][j] == ""]
    if empty_cells:
        move = random.choice(empty_cells)
        print(f"[AI dễ] Đánh ngẫu nhiên tại {move}")
        return move

    # 3. Không còn ô trống
    return None


# ==================================================
# Kiểm thử nhanh
# ==================================================
if __name__ == "__main__":
    from logic import GameLogic  # Chỉ dùng khi test riêng file này
    
    # Tạo bàn cờ test 15x15 (chỉ dùng 5x5 đầu cho dễ nhìn)
    test_board = [[""] * 15 for _ in range(15)]
    test_board[0][0] = "X"
    test_board[0][1] = "X"
    test_board[0][2] = "X"
    test_board[0][3] = "X"  # X sắp có 5 → O phải chặn!

    game = GameLogic(board_size=15)
    game.board = test_board

    move = ai_easy_move(test_board, "O", game)
    print("AI chọn nước đi:", move)  # Kết quả mong đợi: (0, 4) hoặc tương tự
