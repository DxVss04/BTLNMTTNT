"""
logic.py - Module quản lý bàn cờ Caro
Sử dụng: from logic import BoardManager
"""

class BoardManager:
    """
    Class quản lý bàn cờ Caro
    - 0: Ô trống
    - 1: Quân X
    - -1: Quân O
    """
    
    def __init__(self, size=15):
        """
        Khởi tạo bàn cờ
        
        """
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.move_count = 0  # Đếm số nước đã đi
    
    def update_board(self, x, y, player):
        """
        Đánh một nước cờ
        
        Args:
            x (int): Tọa độ hàng (0 đến size-1)
            y (int): Tọa độ cột (0 đến size-1)
            player (int): 1 cho X, -1 cho O
        
        Returns:
            bool: True nếu đi thành công, False nếu ô đã có quân
        """
        # Kiểm tra tọa độ hợp lệ
        if not (0 <= x < self.size and 0 <= y < self.size):
            return False
        
        # Kiểm tra ô đã có quân chưa
        if self.board[x][y] != 0:
            return False
        
        # Đánh quân cờ
        self.board[x][y] = player
        self.move_count += 1
        return True
    
    def reset_board(self):
        """Xóa trắng bàn cờ"""
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.move_count = 0
    
    def check_win(self, current_x, current_y, player):
        """
        Kiểm tra thắng thua sau nước đi vừa rồi
        Tối ưu: Chỉ kiểm tra xung quanh vị trí vừa đánh
        
        Args:
            current_x (int): Tọa độ x của nước vừa đi
            current_y (int): Tọa độ y của nước vừa đi
            player (int): 1 hoặc -1
        
        Returns:
            bool: True nếu thắng, False nếu chưa thắng
        """
        # 4 hướng: Ngang, Dọc, Chéo chính (\), Chéo phụ (/)
        directions = [
            (0, 1),   # Ngang (horizontal)
            (1, 0),   # Dọc (vertical)
            (1, 1),   # Chéo chính (diagonal \)
            (1, -1)   # Chéo phụ (diagonal /)
        ]
        
        for dx, dy in directions:
            if self._count_consecutive(current_x, current_y, dx, dy, player) >= 5:
                return True
        
        return False
    
    def _count_consecutive(self, x, y, dx, dy, player):
        """
        Đếm số quân liên tiếp theo một hướng
        
        Args:
            x, y (int): Vị trí bắt đầu
            dx, dy (int): Hướng di chuyển
            player (int): Người chơi (1 hoặc -1)
        
        Returns:
            int: Số quân liên tiếp
        """
        count = 1  # Đếm quân tại vị trí hiện tại
        
        # Đếm theo hướng thuận (+dx, +dy)
        i = 1
        while True:
            new_x = x + i * dx
            new_y = y + i * dy
            
            if (0 <= new_x < self.size and 
                0 <= new_y < self.size and 
                self.board[new_x][new_y] == player):
                count += 1
                i += 1
            else:
                break
        
        # Đếm theo hướng ngược (-dx, -dy)
        i = 1
        while True:
            new_x = x - i * dx
            new_y = y - i * dy
            
            if (0 <= new_x < self.size and 
                0 <= new_y < self.size and 
                self.board[new_x][new_y] == player):
                count += 1
                i += 1
            else:
                break
        
        return count
    
    def is_full(self):
        """
        Kiểm tra bàn cờ đã đầy chưa (Hòa)
        
        Returns:
            bool: True nếu không còn ô trống (Hòa)
        """
        return self.move_count == self.size * self.size
    
    def get_valid_moves(self):
        """
        Lấy danh sách các nước đi hợp lệ (các ô trống)
        Dành cho cho AI Bot
        
        Returns:
            list: Danh sách các tuple (x, y) của ô trống
        """
        valid_moves = []
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] == 0:
                    valid_moves.append((x, y))
        return valid_moves
    
    def get_board_state(self):
        """
        Trả về trạng thái bàn cờ hiện tại
        Dùng cho UI để vẽ lại bàn cờ
        
        Returns:
            list: Mảng 2 chiều chứa trạng thái bàn cờ
        """
        # Trả về copy để tránh UI thay đổi trực tiếp board
        return [row[:] for row in self.board]
    
    def get_cell_value(self, x, y):
        """
        Lấy giá trị một ô cụ thể
        
        Args:
            x, y (int): Tọa độ ô cần lấy
        
        Returns:
            int: 0 (trống), 1 (X), -1 (O), hoặc None nếu tọa độ không hợp lệ
        """
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.board[x][y]
        return None
    
    def print_board(self):
        """In bàn cờ ra console (dùng cho debug)"""
        print("\n   ", end="")
        for i in range(self.size):
            print(f"{i:2}", end=" ")
        print()
        
        for x in range(self.size):
            print(f"{x:2} ", end="")
            for y in range(self.size):
                cell = self.board[x][y]
                if cell == 1:
                    symbol = 'X'
                elif cell == -1:
                    symbol = 'O'
                else:
                    symbol = '.'
                print(f" {symbol} ", end="")
            print()


