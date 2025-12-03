import random

# ==================================================
# File: ai_easy.py
# Người viết: Thanh Sơn – Nhóm 5 (Caro Bot)
# AI DỄ – chỉ chặn thắng + đánh ngẫu nhiên
# ==================================================

def ai_easy_move(board_manager, player):
    """
    player: 1 (X) hoặc -1 (O)
    board_manager: đối tượng BoardManager từ main.py
    """
    opponent = -player  # Nếu mình là X (1) → đối thủ là O (-1) và ngược lại

    size = board_manager.size

    # 1. Chặn đối thủ thắng ngay
    for x in range(size):
        for y in range(size):
            if board_manager.board[x][y] == 0:
                board_manager.board[x][y] = opponent
                if board_manager.check_win(x, y, opponent):
                    board_manager.board[x][y] = 0  # Khôi phục
                    print(f"[AI Dễ] Chặn đối thủ thắng tại ({x}, {y})")
                    return x, y
                board_manager.board[x][y] = 0

    # 2. Đánh ngẫu nhiên
    empty_cells = [(x, y) for x in range(size) for y in range(size) if board_manager.board[x][y] == 0]
    if empty_cells:
        move = random.choice(empty_cells)
        print(f"[AI Dễ] Đánh ngẫu nhiên tại {move}")
        return move

    print("[AI Dễ] Bàn cờ đầy – Hòa!")
    return None
