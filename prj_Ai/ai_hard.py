
import random
from copy import deepcopy

BOARD_SIZE = 15
MAX_DEPTH = 4                    
CANDIDATE_DIST = 2             


def check_winner(board, row, col, mark):
    """Kiểm tra có 5 quân liên tiếp từ vị trí vừa đánh không"""
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    size = len(board)
    for dx, dy in directions:
        count = 1
        # Đếm xuôi
        x, y = row + dx, col + dy
        while 0 <= x < size and 0 <= y < size and board[x][y] == mark:
            count += 1
            x += dx
            y += dy
        # Đếm ngược
        x, y = row - dx, col - dy
        while 0 <= x < size and 0 <= y < size and board[x][y] == mark:
            count += 1
            x -= dx
            y -= dy
        if count >= 5:
            return True
    return False


# ------------------- Tìm nước thắng / chặn thắng ngay -------------------
def find_forced_move(board, mark):
    """Tìm nước thắng ngay hoặc chặn đối thủ thắng ngay"""
    opponent = "O" if mark == "X" else "X"
    candidates = get_candidate_moves(board)

    # 1. Có nước thắng luôn không?
    for r, c in candidates:
        board[r][c] = mark
        if check_winner(board, r, c, mark):
            board[r][c] = ""
            print(f"[AI Hard] THẮNG NGAY tại ({r}, {c})!")
            return (r, c)
        board[r][c] = ""

    # 2. Đối thủ có nước thắng không? → phải chặn
    for r, c in candidates:
        board[r][c] = opponent
        if check_winner(board, r, c, opponent):
            board[r][c] = ""
            print(f"[AI Hard] CHẶN THẮNG đối thủ tại ({r}, {c})!")
            return (r, c)
        board[r][c] = ""

    return None


# ------------------- Lấy danh sách nước đi tiềm năng -------------------
def get_candidate_moves(board):
    """Chỉ xét các ô trống gần quân đã có (giảm từ 225 → ~30-50 ô)"""
    size = len(board)
    candidates = set()
    has_piece = False

    for i in range(size):
        for j in range(size):
            if board[i][j] != "":
                has_piece = True
                # Quét xung quanh bán kính 2
                for di in range(-CANDIDATE_DIST, CANDIDATE_DIST + 1):
                    for dj in range(-CANDIDATE_DIST, CANDIDATE_DIST + 1):
                        ni, nj = i + di, j + dj
                        if 0 <= ni < size and 0 <= nj < size and ++board[ni][nj] == "":
                            candidates.add((ni, nj))

    if not has_piece:
        center = size // 2
        return [(center, center)]

    return list(candidates)


# ------------------- Đánh giá nhanh nước đi (dùng để sắp xếp) -------------------
def evaluate_move_priority(board, row, col, mark):
    """Đánh giá nhanh để sắp xếp nước đi tốt trước → Alpha-Beta cắt nhanh hơn"""
    if board[row][col] != "":
        return -999999

    opponent = "O" if mark == "X" else "X"
    score = 0
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    for dx, dy in directions:
        my_count = 0
        opp_count = 0

        # Đếm quân mình
        x, y = row + dx, col + dy
        while 0 <= x < len(board) and 0 <= y < len(board) and board[x][y] == mark:
            my_count += 1
            x += dx; y += dy
        x, y = row - dx, col - dy
        while 0 <= x < len(board) and 0 <= y < len(board) and board[x][y] == mark:
            my_count += 1
            x -= dx; y -= dy

        # Đếm quân đối thủ
        x, y = row + dx, col + dy
        while 0 <= x < len(board) and 0 <= y < len(board) and board[x][y] == opponent:
            opp_count += 1
            x += dx; y += dy
        x, y = row - dx, col - dy
        while 0 <= x < len(board) and 0 <= y < len(board) and board[x][y] == opponent:
            opp_count += 1
            x -= dx; y -= dy

        # Ưu tiên cực cao nếu tạo 4 hoặc chặn 4
        if my_count >= 4:   score += 100000
        elif my_count == 3: score += 10000
        elif my_count == 2: score += 1000

        if opp_count >= 4:  score += 200000   # Phải chặn trước!
        elif opp_count == 3: score += 50000

    return score


# ------------------- Minimax + Alpha-Beta Pruning -------------------
def minimax(board, depth, alpha, beta, maximizing_player, ai_mark):
    """Trả về (score, best_move)"""
    if depth == 0:
        return 0, None  # Hòa

    # Kiểm tra đã có người thắng chưa
    size = len(board)
    for i in range(size):
        for j in range(size):
            if board[i][j] != "":
                if check_winner(board, i, j, board[i][j]):
                    return (1000000 if board[i][j] == ai_mark else -1000000), None

    candidates = get_candidate_moves(board)
    if not candidates:
        return 0, None

    # Sắp xếp nước đi tốt trước → Alpha-Beta cắt
    opponent = "O" if ai_mark == "X" else "X"
    current_mark = ai_mark if maximizing_player else opponent

    candidates.sort(
        key=lambda pos: evaluate_move_priority(board, pos[0], pos[1], current_mark),
        reverse=maximizing_player
    )

    best_move = None

    if maximizing_player:
        max_eval = -float('inf')
        for r, c in candidates:
            board[r][c] = ai_mark
            eval_score, _ = minimax(board, depth - 1, alpha, beta, False, ai_mark)
            board[r][c] = ""
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = (r, c)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break  # Cắt tỉa!
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for r, c in candidates:
            board[r][c] = opponent
            eval_score, _ = minimax(board, depth - 1, alpha, beta, True, ai_mark)
            board[r][c] = ""
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = (r, c)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break  # Cắt tỉa!
        return min_eval, best_move


# ------------------- Hàm chính AI Hard -------------------
def ai_hard_move(board, mark):
    """Trả về nước đi tốt nhất của AI Hard"""
    print(f"[AI Hard] Đang suy nghĩ... (depth={MAX_DEPTH})")

    # 1. Kiểm tra nước cờ bắt buộc (thắng/chặn thắng)
    forced = find_forced_move(board, mark)
    if forced:
        return forced

    # 2. Chạy Minimax + Alpha-Beta
    board_copy = deepcopy(board)  # Tránh sửa board gốc
    _, best_move = minimax(board_copy, MAX_DEPTH, -float('inf'), float('inf'), True, mark)

    if best_move is None:
        # Hiếm khi xảy ra → random trong vùng gần
        candidates = get_candidate_moves(board)
        best_move = random.choice(candidates) if candidates else None

    print(f"[AI Hard] Chọn nước đi: {best_move}")
    return best_move


# ==================================================
#  Kiểm thử nhanh
# ==================================================
if __name__ == "__main__":
    print("=== Kiểm thử AI Hard ===")
    board = [["" for _ in range(15)] for _ in range(15)]

    # Tạo tình huống: X sắp có 4 → O phải chặn
    board[7][7] = "X"
    board[7][8] = "X"
    board[7][9] = "X"
    board[7][10] = "X"

    print("X có 4 quân liên tiếp → O phải chặn ở (7,6) hoặc (7,11)")
    move = ai_hard_move(board, "O")
    print(f"→ AI Hard chọn: {move}")