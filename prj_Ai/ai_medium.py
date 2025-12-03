import random

# ==================================================
# File: ai_medium.py
# Người viết: Thanh Sơn – Nhóm 5 (Caro Bot)
# AI TRUNG BÌNH – Tính điểm tấn công + phòng thủ
# ==================================================

def evaluate_position(board, x, y, player):
    if board[x][y] != 0: return -1
    opponent = -player
    score = 0
    directions = [(0,1), (1,0), (1,1), (1,-1)]

    for dx, dy in directions:
        my_count = opp_count = 0
        for i in range(1, 6):
            nx, ny = x + dx*i, y + dy*i
            if 0 <= nx < 15 and 0 <= ny < 15:
                if board[nx][ny] == player: my_count += 1
                if board[nx][ny] == opponent: opp_count += 1
            nx, ny = x - dx*i, y - dy*i
            if 0 <= nx < 15 and 0 <= ny < 15:
                if board[nx][ny] == player: my_count += 1
                if board[nx][ny] == opponent: opp_count += 1

        if my_count + 1 >= 5: return 999_999_999
        if opp_count + 1 >= 5: return 999_999_998

        if my_count >= 4: score += 100000
        elif my_count == 3: score += 5000
        if opp_count >= 4: score += 90000
        elif opp_count == 3: score += 4000

    # Gần tâm + điểm
    center = 7
    score += 100 - (abs(x - center) + abs(y - center))
    return score


def ai_medium_move(board_manager, player):
    size = board_manager.size
    best_score = -999_999_999
    best_moves = []

    for x in range(size):
        for y in range(size):
            if board_manager.board[x][y] == 0:
                score = evaluate_position(board_manager.board, x, y, player)
                if score > best_score:
                    best_score = score
                    best_moves = [(x, y)]
                elif score == best_score:
                    best_moves.append((x, y))

    if not best_moves:
        return None

    move = random.choice(best_moves)
    return move

