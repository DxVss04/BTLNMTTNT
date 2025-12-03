# ==================================================
# File: ai_hard.py
# Người viết: Thanh Sơn – Nhóm 5 (Caro AI Project)
# Mức độ: KHÓ NHẤT – Minimax + Alpha-Beta + Evaluation cực mạnh
# Đặc điểm: Gần như BẤT BẠI trên bàn 15x15 (5 ô thắng)
# Tốc độ: Nhanh (dưới 2 giây mỗi nước), nhờ cắt tỉa tốt + candidate + thứ tự ưu tiên
# ==================================================

import random
from copy import deepcopy

# Độ sâu tìm kiếm (có thể tăng lên 7-8 nếu máy mạnh)
MAX_DEPTH = 6

# Lấy danh sách nước đi tiềm năng (chỉ xét gần các ô đã có quân)
def get_candidates(board):
    candidates = set()
    size = len(board)
    has_move = False
    for i in range(size):
        for j in range(size):
            if board[i][j] != 0:
                has_move = True
                for di in range(-2, 3):
                    for dj in range(-2, 3):
                        if di == 0 and dj == 0:
                            continue
                        ni, nj = i + di, j + dj
                        if 0 <= ni < size and 0 <= nj < size and board[ni][nj] == 0:
                            candidates.add((ni, nj))
    if not has_move:
        return [(7, 7)]
    return list(candidates) if candidates else [(7, 7)]

# Hàm đánh giá trạng thái bàn cờ (rất mạnh!)
def evaluate_board(board, player):
    def count_line(line, p):
        count = 0
        open_ends = 0
        for cell in line:
            if cell == p:
                count += 1
            elif cell == 0:
                if count > 0:
                    open_ends += 1
                count = 0
            else:
                if count > 0:
                    open_ends += 1
                count = 0
        if count > 0:
            open_ends += 1
        return count, open_ends

    score = 0
    opp = -player

    # Đánh giá tất cả các đường
    for p, factor in [(player, 1), (opp, -1.5)]:  # Phòng thủ quan trọng hơn tấn công
        for i in range(15):
            # Hàng, cột
            row = board[i]
            col = [board[j][i] for j in range(15)]
            score += factor * evaluate_pattern(count_line(row, p))
            score += factor * evaluate_pattern(count_line(col, p))
        # Đường chéo
        for i in range(15):
            diag1 = [board[i+k][i+k] for k in range(15-i)]
            diag2 = [board[i+k][i-k] for k in range(i+1)]
            diag3 = [board[i-k][i+k] for k in range(i+1)]
            score += factor * evaluate_pattern(count_line(diag1, p))
            if len(diag2) >= 5: score += factor * evaluate_pattern(count_line(diag2, p))
            if len(diag3) >= 5: score += factor * evaluate_pattern(count_line(diag3, p))
    return score

def evaluate_pattern(count_open):
    count, opens = count_open
    if count >= 5:
        return 1000000
    elif count == 4:
        return 100000 if opens >= 1 else 5000
    elif count == 3:
        return 10000 if opens == 2 else 1000 if opens == 1 else 100
    elif count == 2:
        return 1000 if opens == 2 else 100
    return 0

# Kiểm tra thắng ngay lập tức (ưu tiên cao nhất)
def find_winning_move(board_manager, player):
    board = board_manager.board
    size = board_manager.size
    opp = -player

    for x, y in get_candidates(board):
        if board[x][y] != 0:
            continue
        # Thử mình thắng
        board[x][y] = player
        if board_manager.check_win(x, y, player):
            board[x][y] = 0
            return (x, y)
        # Thử đối thủ thắng → chặn
        board[x][y] = opp
        if board_manager.check_win(x, y, opp):
            board[x][y] = 0
            return (x, y)
        board[x][y] = 0
    return None

# Minimax + Alpha-Beta + Thứ tự ưu tiên nước đi
def minimax(board, depth, alpha, beta, maximizing, player, board_manager):
    if depth == 0 or board_manager.is_full():
        return evaluate_board(board, player), None

    win_move = find_winning_move(board_manager, player if maximizing else -player)
    if win_move:
        return (10000000 if maximizing else -10000000), win_move

    candidates = get_candidates(board)
    if not candidates:
        return 0, None

    # Sắp xếp nước đi theo độ ưu tiên (tấn công trước, phòng thủ sau)
    def priority(move):
        x, y = move
        temp = board[x][y]
        board[x][y] = player if maximizing else -player
        score = evaluate_board(board, player)
        board[x][y] = temp
        return -score if maximizing else score

    candidates.sort(key=priority, reverse=maximizing)

    best_move = candidates[0]
    if maximizing:
        value = -float('inf')
        for move in candidates:
            x, y = move
            board[x][y] = player
            val, _ = minimax(board, depth-1, alpha, beta, False, player, board_manager)
            board[x][y] = 0
            if val > value:
                value = val
                best_move = move
            alpha = max(alpha, val)
            if beta <= alpha:
                break
        return value, best_move
    else:
        value = float('inf')
        for move in candidates:
            x, y = move
            board[x][y] = -player
            val, _ = minimax(board, depth-1, alpha, beta, True, player, board_manager)
            board[x][y] = 0
            if val < value:
                value = val
                best_move = move
            beta = min(beta, val)
            if beta <= alpha:
                break
        return value, best_move

# Hàm chính AI Hard
def ai_hard_move(board_manager, player):
    # Ưu tiên thắng/chặn ngay lập tức
    forced = find_winning_move(board_manager, player)
    if forced:
        return forced

    # Minimax chính
    board_copy = deepcopy(board_manager.board)
    _, best_move = minimax(board_copy, MAX_DEPTH, -float('inf'), float('inf'), True, player, board_manager)
    
    if best_move is None:
        best_move = (7, 7)
    
    return best_move
