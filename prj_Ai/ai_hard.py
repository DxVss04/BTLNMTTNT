# ai_hard.py
import random
from copy import deepcopy

SIZE = 15
MAX_DEPTH = 3

# ==================================================================
# Candidate reduction giống hệt Java: chỉ xét ô gần quân đã đánh
# ==================================================================
def is_near_occupied(board, x, y):
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < SIZE and 0 <= ny < SIZE and board[nx][ny] != 0:
                return True
    return False

def get_candidates(board):
    candidates = []
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == 0 and is_near_occupied(board, i, j):
                candidates.append((i, j))
    return candidates if candidates else [(7, 7)]

# ==================================================================
# Minimax 
# ==================================================================
def minimax(board, depth, alpha, beta, maximizing, player):
    # Kiểm tra thắng/thua (dùng BoardManager để chính xác)
    winner = check_winner_fast(board)
    if winner == player: return 99999999
    if winner == -player: return -99999999
    if depth == 0:
        return evaluate_board_fast(board, player)

    candidates = get_candidates(board)
    if not candidates:
        return 0

    if maximizing:
        max_eval = float('-inf')
        for x, y in candidates:
            board[x][y] = player
            eval_score = minimax(board, depth - 1, alpha, beta, False, player)
            board[x][y] = 0
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for x, y in candidates:
            board[x][y] = -player
            eval_score = minimax(board, depth - 1, alpha, beta, True, player)
            board[x][y] = 0
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval

# 
# Đánh giá nhanh
# 
def evaluate_board_fast(board, player):
    score = 0
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == player:
                score += evaluate_pos(board, i, j, player)
            elif board[i][j] == -player:
                score -= evaluate_pos(board, i, j, -player) * 1.1
    return score

def evaluate_pos(board, x, y, p):
    score = 0
    for dx, dy in [(0,1),(1,0),(1,1),(1,-1)]:
        count = 1
        for sign in [1, -1]:
            nx, ny = x + sign*dx, y + sign*dy
            for _ in range(4):
                if 0 <= nx < SIZE and 0 <= ny < SIZE:
                    if board[nx][ny] == p:
                        count += 1
                    elif board[nx][ny] != 0:
                        count = 0
                        break
                    nx += sign*dx
                    ny += sign*dy
                else:
                    break
        if count >= 5: score += 100000
        elif count == 4: score += 10000
        elif count == 3: score += 500
        elif count == 2: score += 50
    return score

#Kiểm tra thắng nhanh
def check_winner_fast(board):
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == 0: continue
            p = board[i][j]
            for dx, dy in [(0,1),(1,0),(1,1),(1,-1)]:
                if (count_line(board, i, j, dx, dy, p) +
                    count_line(board, i, j, -dx, -dy, p) >= 4):
                    return p
    return 0

def count_line(board, x, y, dx, dy, p):
    count = 0
    nx, ny = x + dx, y + dy
    while 0 <= nx < SIZE and 0 <= ny < SIZE and board[nx][ny] == p:
        count += 1
        nx += dx
        ny += dy
    return count

# ==================================================================
# Hàm chính
# ==================================================================
def ai_hard_move(board_manager, player):
    print("[AI Hard] Đang tính... (depth=3, siêu nhanh)")
    board = board_manager.board

    # 1. Tìm nước tốt nhất trong các ô gần quân
    candidates = get_candidates(board)
    best_score = float('-inf')
    best_move = candidates[0]

    board_copy = deepcopy(board)
    for x, y in candidates:
        board_copy[x][y] = player
        score = minimax(board_copy, MAX_DEPTH - 1, float('-inf'), float('inf'), False, player)
        board_copy[x][y] = 0
        if score > best_score:
            best_score = score
            best_move = (x, y)
    return best_move
