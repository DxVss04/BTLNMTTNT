# ui.py
import tkinter as tk
from tkinter import ttk, messagebox
from board import Board, BOARD_WIDTH, BOARD_HEIGHT, BG_COLOR

class CaroUI:
    def __init__(self, root, on_click_callback=None, on_restart_callback=None):
        self.root = root
        self.root.title("Cờ Caro AI")
        
        # Callback: Hàm sẽ được gọi khi người dùng tương tác (được truyền từ main hoặc game_manager)
        self.on_click_callback = on_click_callback
        self.on_restart_callback = on_restart_callback

        # Khởi tạo Logic bàn cờ
        self.board_logic = Board()

        # Biến lưu cấu hình giao diện
        self.mode_var = tk.StringVar(value="PVP")
        self.diff_var = tk.StringVar(value="Dễ")

        self.setup_layout()
        
        # Vẽ lưới ban đầu
        self.board_logic.draw_grid(self.canvas)

    def setup_layout(self):
        # --- KHUNG BÀN CỜ (TRÁI) ---
        self.board_frame = tk.Frame(self.root, padx=10, pady=10)
        self.board_frame.pack(side=tk.LEFT)

        self.canvas = tk.Canvas(self.board_frame, width=BOARD_WIDTH, height=BOARD_HEIGHT, 
                                bg=BG_COLOR, highlightthickness=1, highlightbackground="black")
        self.canvas.pack()
        
        # Xử lý click chuột 
        self.canvas.bind("<Button-1>", self.handle_click)

        # Nút Undo/Redo nhỏ trên góc bàn cờ 
        btn_style = {'font': ("Arial", 8, "bold"), 'bg': "#f0f0f0", 'bd': 2}
        tk.Button(self.board_frame, text="⟲ Undo", command=self.on_undo_click, **btn_style)\
            .place(x=BOARD_WIDTH - 110, y=10, width=50, height=25)
        tk.Button(self.board_frame, text="Redo ⟳", command=self.on_redo_click, **btn_style)\
            .place(x=BOARD_WIDTH - 55, y=10, width=50, height=25)

        # --- MENU ĐIỀU KHIỂN (PHẢI)  ---
        self.control_frame = tk.Frame(self.root, padx=20, pady=20)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y)

        tk.Label(self.control_frame, text="CÀI ĐẶT", font=("Arial", 14, "bold")).pack(pady=10)

        # Chọn chế độ chơi (PVP, PVE, EVE)
        tk.Label(self.control_frame, text="Chế độ:", anchor="w").pack(fill=tk.X, pady=(5,0))
        modes = [("Người vs Người", "PVP"), ("Người vs Máy", "PVE"), ("Máy vs Máy", "EVE")]
        for text, val in modes:
            tk.Radiobutton(self.control_frame, text=text, variable=self.mode_var, value=val).pack(anchor="w")

        # Chọn độ khó (Easy, Medium, Hard)
        tk.Label(self.control_frame, text="Độ khó AI:", anchor="w").pack(fill=tk.X, pady=(15,0))
        ttk.Combobox(self.control_frame, textvariable=self.diff_var, 
                     values=("Dễ", "Trung bình", "Khó"), state="readonly").pack(fill=tk.X)

        # Nút chức năng
        tk.Button(self.control_frame, text="Ván Mới", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                  command=self.on_restart_click).pack(fill=tk.X, pady=20)

        # Hiển thị lượt chơi & thông báo 
        self.status_label = tk.Label(self.control_frame, text="Lượt: X", font=("Arial", 12, "bold"), fg="blue")
        self.status_label.pack(side=tk.BOTTOM, pady=20)

    def handle_click(self, event):
        """Xử lý sự kiện click chuột trên bàn cờ"""
        coords = self.board_logic.get_coords(event.x, event.y)
        if coords and self.on_click_callback:
            row, col = coords
            # Gọi callback gửi về main/game_manager xử lý
            self.on_click_callback(row, col)

    def draw_move(self, row, col, player_val):
        """Hàm công khai để Main gọi vẽ nước đi"""
        self.board_logic.draw_piece(self.canvas, row, col, player_val)

    def update_status(self, text, color="black"):
        """Cập nhật dòng trạng thái"""
        self.status_label.config(text=text, fg=color)

    def show_message(self, title, msg):
        """Hiển thị popup kết quả"""
        messagebox.showinfo(title, msg)

    def reset_board(self):
        """Xóa bàn cờ để chơi mới"""
        self.board_logic = Board() # Reset dữ liệu
        self.board_logic.draw_grid(self.canvas) # Vẽ lại lưới
        self.update_status("Lượt: X", "blue")

    # Các hàm placeholder cho nút bấm
    def on_restart_click(self):
        if self.on_restart_callback:
            self.on_restart_callback()
    
    def on_undo_click(self):
        print("")

    def on_redo_click(self):
        print("")
        
