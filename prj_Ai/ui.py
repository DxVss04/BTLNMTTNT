import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Các hằng số cấu hình giao diện
BOARD_SIZE = 15
CELL_SIZE = 40
BOARD_WIDTH = BOARD_SIZE * CELL_SIZE
BOARD_HEIGHT = BOARD_SIZE * CELL_SIZE
BG_COLOR = "#E3C586"  # Màu gỗ bàn cờ
LINE_COLOR = "#000000"
HIGHLIGHT_COLOR = "#90EE90"

class CaroUI:
    def __init__(self, root, game_manager=None):
        self.root = root
        self.root.title("Cờ Caro AI - Python Project")
        self.game_manager = game_manager  # Tham chiếu đến logic game (Controller)
        
        # Biến lưu cấu hình
        self.mode_var = tk.StringVar(value="PVP") # PVP, PVE, EVE [cite: 5, 6, 7]
        self.diff_var = tk.StringVar(value="Dễ")  # Dễ, Trung bình, Khó [cite: 8-11]
        
        # Cấu trúc giao diện chính
        self.setup_layout()
        self.draw_grid()

    def setup_layout(self):
        """Thiết lập layout gồm Bàn cờ (Trái) và Menu điều khiển (Phải) """
        
        # 1. Khung chứa bàn cờ (Canvas)
        self.board_frame = tk.Frame(self.root, padx=10, pady=10)
        self.board_frame.pack(side=tk.LEFT)
        
        self.canvas = tk.Canvas(
            self.board_frame, 
            width=BOARD_WIDTH, 
            height=BOARD_HEIGHT, 
            bg=BG_COLOR,
            highlightthickness=1, 
            highlightbackground="black"
        )
        self.canvas.pack()
        
        # Bắt sự kiện click chuột 
        self.canvas.bind("<Button-1>", self.on_board_click)

        # 2. Khung điều khiển (Menu)
        self.control_frame = tk.Frame(self.root, padx=20, pady=20, width=200)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # --- Tiêu đề ---
        tk.Label(self.control_frame, text="GAME MENU", font=("Arial", 16, "bold")).pack(pady=10)

        # --- Chọn chế độ chơi [cite: 4] ---
        tk.Label(self.control_frame, text="Chế độ chơi:", anchor="w").pack(fill=tk.X)
        modes = [("Người vs Người", "PVP"), ("Người vs Máy", "PVE"), ("Máy vs Máy", "EVE")]
        for text, val in modes:
            tk.Radiobutton(self.control_frame, text=text, variable=self.mode_var, value=val).pack(anchor="w")
        
        # --- Chọn độ khó AI [cite: 8] ---
        tk.Label(self.control_frame, text="Độ khó AI:", anchor="w").pack(fill=tk.X, pady=(10, 0))
        difficulty_box = ttk.Combobox(self.control_frame, textvariable=self.diff_var)
        difficulty_box['values'] = ("Dễ", "Trung bình", "Khó")
        difficulty_box.current(0)
        difficulty_box.pack(fill=tk.X)

        # --- Các nút chức năng  ---
        btn_opts = {'font': ("Arial", 10), 'pady': 5}
        
        tk.Button(self.control_frame, text="Ván mới (Restart)", bg="#4CAF50", fg="white", 
                  command=self.on_restart, **btn_opts).pack(fill=tk.X, pady=15)
        
        # Nhóm nút Undo/Redo
        undo_frame = tk.Frame(self.control_frame)
        undo_frame.pack(fill=tk.X)
        tk.Button(undo_frame, text="Undo", command=self.on_undo, width=8, **btn_opts).pack(side=tk.LEFT, padx=2)
        tk.Button(undo_frame, text="Redo", command=self.on_redo, width=8, **btn_opts).pack(side=tk.RIGHT, padx=2)

        # --- Thông báo trạng thái ---
        self.status_label = tk.Label(self.control_frame, text="Lượt: X", font=("Arial", 12, "bold"), fg="blue")
        self.status_label.pack(side=tk.BOTTOM, pady=20)

    def draw_grid(self):
        """Vẽ lưới bàn cờ 15x15 """
        self.canvas.delete("all") # Xóa bàn cờ cũ
        
        # Vẽ các đường kẻ ngang và dọc
        for i in range(BOARD_SIZE):
            # Đường ngang
            self.canvas.create_line(
                CELL_SIZE//2, i * CELL_SIZE + CELL_SIZE//2,
                BOARD_WIDTH - CELL_SIZE//2, i * CELL_SIZE + CELL_SIZE//2,
                fill=LINE_COLOR
            )
            # Đường dọc
            self.canvas.create_line(
                i * CELL_SIZE + CELL_SIZE//2, CELL_SIZE//2,
                i * CELL_SIZE + CELL_SIZE//2, BOARD_HEIGHT - CELL_SIZE//2,
                fill=LINE_COLOR
            )

    def on_board_click(self, event):
        """Xử lý sự kiện click chuột """
        # Chuyển đổi tọa độ pixel sang tọa độ lưới (row, col)
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE

        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            # Nếu đã kết nối logic game, gửi tọa độ sang Game Manager
            if self.game_manager:
                self.game_manager.handle_click(row, col)
            else:
                # Code dùng để test giao diện khi chưa có logic
                print(f"Clicked cell: ({row}, {col})")
                # Demo vẽ thử (Xóa đoạn này khi ghép code chính thức)
                self.draw_piece(row, col, "X" if (row+col)%2==0 else "O")

    def draw_piece(self, row, col, player, is_last_move=False):
        """Vẽ quân cờ X hoặc O lên bàn cờ"""
        center_x = col * CELL_SIZE + CELL_SIZE // 2
        center_y = row * CELL_SIZE + CELL_SIZE // 2
        offset = CELL_SIZE // 4

        # Xóa hình cũ ở ô đó (nếu có) để tránh vẽ chồng
        self.canvas.addtag_dtag("all", f"cell_{row}_{col}")
        
        if player == "X":
            color = "blue"
            self.canvas.create_line(center_x - offset, center_y - offset,
                                    center_x + offset, center_y + offset,
                                    width=3, fill=color, tags=f"move_{row}_{col}")
            self.canvas.create_line(center_x + offset, center_y - offset,
                                    center_x - offset, center_y + offset,
                                    width=3, fill=color, tags=f"move_{row}_{col}")
        elif player == "O":
            color = "red"
            self.canvas.create_oval(center_x - offset, center_y - offset,
                                    center_x + offset, center_y + offset,
                                    width=3, outline=color, tags=f"move_{row}_{col}")
        
        # Highlight nước đi mới nhất (Yêu cầu Tuần 5) [cite: 32]
        if is_last_move:
             self.canvas.create_rectangle(col * CELL_SIZE, row * CELL_SIZE,
                                         (col+1) * CELL_SIZE, (row+1) * CELL_SIZE,
                                         outline=HIGHLIGHT_COLOR, width=2)

    def update_status(self, message, color="black"):
        """Cập nhật label trạng thái"""
        self.status_label.config(text=message, fg=color)

    def show_message(self, title, msg):
        """Hiển thị popup thông báo (Thắng/Thua)"""
        messagebox.showinfo(title, msg)

    # --- Các hàm Callback (Sẽ gọi sang GameManager) ---
    def on_restart(self):
        if self.game_manager:
            self.game_manager.restart_game()
        else:
            self.draw_grid() # Reset giao diện demo

    def on_undo(self):
        if self.game_manager:
            self.game_manager.undo_move()
        else:
            print("Undo clicked")

    def on_redo(self):
        if self.game_manager:
            self.game_manager.redo_move()
        else:
            print("Redo clicked")

# if __name__ == "__main__":
#     root = tk.Tk()
#     root.geometry(f"{BOARD_WIDTH + 250}x{BOARD_HEIGHT + 50}")
#     app = CaroUI(root)
#     root.mainloop()
