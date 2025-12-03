# ai_easy.py - MỨC DỄ
# Tính năng: thắng ngay → chặn → gần quân → ngẫu nhiên
import random
from copy import deepcopy

SIZE = 15

def is_near_occupied(board, x, y):
    """Kiểm tra ô (x,y) có gần ô nào đã có quân không"""
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < SIZE and 0 <= ny < SIZE and board[nx][ny] != 0:
                return True
    return False

def ai_easy_move(board_manager, player):
    """
    Trả về nước đi của AI mức Dễ
    Args:
        board_manager: đối tượng BoardManager (có .board và .check_win(x,y,player))
        player: -1 (O - AI), thường là -1
    Returns:
        tuple (row, col) hoặc None nếu hòa
    """
    board = board_manager.board
    opponent = -player  # người chơi là X (1)

    # ==================================================================
    # 1. Tấn công: Nếu AI có thể thắng ngay → đánh luôn
    # ==================================================================
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == 0:
                board[i][j] = player
                if board_manager.check_win(i, j, player):
                    board[i][j] = 0
                    return i, j
                board[i][j] = 0

    # ==================================================================
    # 2. Phòng thủ: Chặn nếu người chơi sắp thắng
    # ==================================================================
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == 0:
                board[i][j] = opponent
                if board_manager.check_win(i, j, opponent):
                    board[i][j] = 0
                    return i, j
                board[i][j] = 0

    # ==================================================================
    # 3. Ưu tiên đánh gần các ô đã có quân
    # ==================================================================
    near_cells = []
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == 0 and is_near_occupied(board, i, j):
                near_cells.append((i, j))

    if near_cells:
        move = random.choice(near_cells)
        return move

    # ==================================================================
    # 4. Nếu không có ô nào gần → đánh ngẫu nhiên
    # ==================================================================
    empty_cells = [(i, j) for i in range(SIZE) for j in range(SIZE) if board[i][j] == 0]
    if empty_cells:
        move = random.choice(empty_cells)
        return move

    return None  # Hòa
