# ==================================================
# File: ai_medium.py
# Người viết: Thanh Sơn – Nhóm 5 (Caro AI Project)
# Mức độ: TRUNG BÌNH (rất mạnh, gần Hard)
# Chiến thuật:
#   - Ưu tiên CHẶN đối thủ tạo 4 hoặc sắp thắng
#   - Ưu tiên TẤN CÔNG tạo 4 mở hoặc 3 mở
#   - Tính điểm chi tiết theo dạng (4 mở > 3 mở 2 bên > 3 mở 1 bên > 2 mở...)
#   - Ưu tiên đánh gần tâm + gần các nước đã đi
# ==================================================

import random

def evaluate_position(board, x, y, player):
    if board[x][y] != 0:
        return -1

    opponent = -player
    score = 0
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for dx, dy in directions:
        # Đếm số quân của mình và đối thủ theo hướng
        my_count = 1    # chính ô (x,y) đang xét
        opp_count = 1
        my_open = 0     # số đầu mở của mình
        opp_open = 0    # số đầu mở của đối thủ

        # Kiểm tra 2 bên của hướng
        for sign in [1, -1]:
            for step in range(1, 6):
                nx = x + sign * dx * step
                ny = y + sign * dy * step
                if not (0 <= nx < 15 and 0 <= ny < 15):
                    break  # ra ngoài bàn cờ → đầu bị chặn
                cell = board[nx][ny]
                if cell == player:
                    my_count += 1
                elif cell == opponent:
                    opp_count += 1
                    break  # bị chặn bởi đối thủ
                else:
                    # ô trống → vẫn mở
                    if step == 1:
                        my_open += 1 if cell == 0 else 0
                    break  # chỉ cần ô trống đầu tiên

        # === ĐÁNH GIÁ TỪNG HƯỚNG ===
        # Tấn công (mình)
        if my_count >= 5:
            return 999_999_999  # thắng ngay
        elif my_count == 4:
            if my_open >= 1:        # 4 mở 1 đầu → cực nguy hiểm
                score += 1_000_000
            else:
                score += 100_000        # 4 bị chặn 1 đầu
        elif my_count == 3:
            if my_open == 2:            # 3 mở 2 đầu
                score += 100_000
            elif my_open == 1:          # 3 mở 1 đầu
                score += 10_000
        elif my_count == 2 and my_open == 2:
            score += 1_000

        # Phòng thủ (ưu tiên cao hơn tấn công!)
        if opp_count >= 5:
            return 999_999_998  # đối thủ thắng → phải chặn ngay
        elif opp_count == 4:
            if opp_open >= 1:
                score += 5_000_000      # đối thủ 4 mở → CHẶN NGAY!
            else:
                score += 500_000
        elif opp_count == 3:
            if opp_open == 2:
                score += 500_000        # 3xx3 → rất nguy hiểm
            elif opp_open == 1:
                score += 50_000

    # Ưu tiên đánh gần tâm bàn cờ
    center = 7
    score += 200 - (abs(x - center) + abs(y - center)) * 10

    # Ưu tiên đánh gần các nước đã đi (tạo thế trận)
    near_bonus = 0
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            nx, ny = x + dx, y + dy
            if 0 <= nx < 15 and 0 <= ny < 15 and board[nx][ny] != 0:
                near_bonus += 20
    score += near_bonus

    return score


def ai_medium_move(board_manager, player):
    """
    Trả về nước đi tốt nhất cho AI mức TRUNG BÌNH
    """
    board = board_manager.board
    size = board_manager.size  # 15
    best_score = -999_999_999
    best_moves = []

    # Duyệt tất cả ô trống
    for i in range(size):
        for j in range(size):
            if board[i][j] == 0:
                score = evaluate_position(board, i, j, player)
                if score > best_score:
                    best_score = score
                    best_moves = [(i, j)]
                elif score == best_score:
                    best_moves.append((i, j))

    if not best_moves:
        return None

    # Chọn ngẫu nhiên trong số các nước tốt nhất
    chosen = random.choice(best_moves)
    return chosen
