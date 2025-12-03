# ==================================================
# File: ai_easy.py
# Tác giả: Thanh Sơn – Nhóm 5 (Caro AI Project)
# Mức độ: DỄ
# Chiến thuật: 
#   1. Nếu có thể chặn đối thủ thắng ngay → chặn
#   2. Nếu mình có thể thắng ngay → thắng luôn (ưu tiên cao hơn chặn)
#   3. Nếu không → đánh ngẫu nhiên vào ô trống
# ==================================================

import random

def ai_easy_move(board_manager, player):
    """
    Trả về nước đi của AI mức DỄ
    Args:
        board_manager: đối tượng BoardManager
        player: quân của AI (1 = X hoặc -1 = O)
    Returns:
        tuple (x, y) hoặc None nếu không còn nước đi
    """
    board = board_manager.board
    size = board_manager.size  # 15

    # === BƯỚC 1: Kiểm tra nước thắng ngay (mình thắng trước) ===
    for x in range(size):
        for y in range(size):
            if board[x][y] == 0:
                board[x][y] = player
                if board_manager.check_win(x, y, player):
                    board[x][y] = 0
                    print(f"[AI Dễ] Thắng ngay tại ({x}, {y})")
                    return x, y
                board[x][y] = 0  # khôi phục

    # === BƯỚC 2: Chặn đối thủ thắng ngay ===
    opponent = -player
    for x in range(size):
        for y in range(size):
            if board[x][y] == 0:
                board[x][y] = opponent
                if board_manager.check_win(x, y, opponent):
                    board[x][y] = 0
                    return x, y
                board[x][y] = 0

    # === BƯỚC 3: Đánh ngẫu nhiên vào ô trống ===
    empty_cells = [(i, j) for i in range(size) for j in range(size) if board[i][j] == 0]
    if empty_cells:
        move = random.choice(empty_cells)
        return move

    return None  # Hòa hoặc không còn nước đi
