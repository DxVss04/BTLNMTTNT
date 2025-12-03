import random
from copy import deepcopy

# ==================================================
# File: ai_hard.py
# Người viết: Thanh Sơn – Nhóm 5 (Caro Bot)
# AI KHÓ NHẤT – Minimax + Alpha-Beta
# ==================================================

MAX_DEPTH = 4
CANDIDATE_DIST = 2

def get_candidates(board):
    size = len(board)
    candidates = set()
    has_piece = False
    for i in range(size):
        for j in range(size):
            if board[i][j] != 0:
                has_piece = True
                for di in range(-2, 3):
                    for dj in range(-2, 3):
                        ni, nj = i + di, j + dj
                        if 0 <= ni < size and 0 <= nj < size and board[ni][nj] == 0:
                            candidates.add((ni, nj))
    return [(7,7)] if not has_piece else list(candidates)

def evaluate_priority(board, x, y, player):
    if board[x][y] != 0: return -999999
    opponent = -player
    score = 0
    for dx, dy in [(0,1),(1,0),(1,1),(1,-1)]:
        my = opp = 0
        for i in range(1, 6):
            nx, ny = x + dx*i, y + dy*i
            if 0 <= nx < 15 and 0 <= ny < 15:
                if board[nx][ny] == player: my += 1
                if board[nx][ny] == opponent: opp += 1
            nx, ny = x - dx*i, y - dy*i
            if 0 <= nx < 15 and 0 <= ny < 15:
                if board[nx][ny] == player: my += 1
                if board[nx][ny] == opponent: opp += 1
        if my >= 4: score += 100000
        if opp >= 4: score += 200000
        if my == 3: score += 10000
        if opp == 3: score += 50000
    return score

def find_forced(board_manager, player):
    opponent = -player
    for x, y in get_candidates(board_manager.board):
        board_manager.board[x][y] = player
        if board_manager.check_win(x, y, player):
            board_manager.board[x][y] = 0
            print(f"[AI Hard] THẮNG NGAY tại ({x},{y})")
            return (x, y)
        board_manager.board[x][y] = opponent
        if board_manager.check_win(x, y, opponent):
            board_manager.board[x][y] = 0
            print(f"[AI Hard] CHẶN THẮNG tại ({x},{y})")
            return (x, y)
        board_manager.board[x][y] = 0
    return None

def minimax(board, depth, alpha, beta, maximizing, player, board_manager):
    if depth == 0: return 0, None
    if board_manager.check_win_from_last_move(player): return 1000000, None
    opp = -player
    if board_manager.check_win_from_last_move(opp): return -1000000, None

    candidates = get_candidates(board)
    if not candidates: return 0, None

    candidates.sort(key=lambda p: evaluate_priority(board, p[0], p[1], player if maximizing else opp),
                    reverse=maximizing)

    best = None
    if maximizing:
        val = -float('inf')
        for x, y in candidates:
            board[x][y] = player
            v, _ = minimax(board, depth-1, alpha, beta, False, player, board_manager)
            board[x][y] = 0
            if v > val: val, best = v, (x,y)
            alpha = max(alpha, v)
            if beta <= alpha: break
        return val, best
    else:
        val = float('inf')
        for x, y in candidates:
            board[x][y] = opp
            v, _ = minimax(board, depth-1, alpha, beta, True, player, board_manager)
            board[x][y] = 0
            if v < val: val, best = v, (x,y)
            beta = min(beta, v)
            if beta <= alpha: break
        return val, best

def ai_hard_move(board_manager, player):
    print(f"[AI Hard] Đang tính toán... (depth={MAX_DEPTH})")
    forced = find_forced(board_manager, player)
    if forced: return forced

    board_copy = deepcopy(board_manager.board)
    _, move = minimax(board_copy, MAX_DEPTH, -float('inf'), float('inf'), True, player, board_manager)
    move = move or random.choice(get_candidates(board_manager.board) or [(7,7)])

    print(f"[AI Hard] Chọn nước đi: {move}")
    return move
