import tkinter as tk
from tkinter import ttk
from logic import BoardManager

# --- CẤU HÌNH GIAO DIỆN (THEME) ---
CELL_SIZE = 35
BOARD_SIZE = 15
BOARD_WIDTH = CELL_SIZE * BOARD_SIZE
BOARD_HEIGHT = CELL_SIZE * BOARD_SIZE

# Bảng màu (Palette)
COLOR_BOARD_BG = "#EECFA1"   # Màu gỗ sáng
COLOR_GRID = "#8B4513"       # Màu kẻ lưới (nâu đất)
COLOR_BG_MAIN = "#FDF5E6"    # Màu nền app (OldLace)
COLOR_PANEL_BG = "#FFF8DC"   # Màu nền khung điều khiển

COLOR_X = "#D32F2F"          # Đỏ đậm
COLOR_X_SHADOW = "#8E0000"   # Bóng đỏ tối
COLOR_O = "#1976D2"          # Xanh đậm
COLOR_O_SHADOW = "#0D47A1"   # Bóng xanh tối

# Font chữ
FONT_BOLD = ("Segoe UI", 11, "bold")
FONT_NORMAL = ("Segoe UI", 10)
FONT_TITLE = ("Segoe UI", 16, "bold")

class CaroUI:
    def __init__(self, root, on_click_callback=None, on_restart_callback=None, on_undo_callback=None):
        self.root = root
        self.root.title("Cờ Caro AI - Pro UI")
        self.root.configure(bg=COLOR_BG_MAIN)

        self.on_click_callback = on_click_callback
        self.on_restart_callback = on_restart_callback
        self.on_undo_callback = on_undo_callback

        self.logic = BoardManager(size=BOARD_SIZE)
        self.mode_var = tk.StringVar(value="PVP")
        self.diff_var = tk.StringVar(value="Dễ")

        self.setup_layout()
        self.redraw_board()

    def setup_layout(self):
        # Container chính
        main_container = tk.Frame(self.root, bg=COLOR_BG_MAIN, padx=15, pady=15)
        main_container.pack(fill=tk.BOTH, expand=True)

        # ======== Cột Trái: Bàn cờ ========
        self.board_frame = tk.Frame(main_container, bg=COLOR_BG_MAIN)
        self.board_frame.pack(side=tk.LEFT, padx=(0, 20))

        # --- Thanh công cụ (Undo) ---
        top_bar = tk.Frame(self.board_frame, bg=COLOR_BG_MAIN)
        top_bar.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))
        
        # Nút Undo
        btn_undo = tk.Button(top_bar, text="⟲ Đi lại", font=FONT_NORMAL,
                             bg="white", fg="#333", relief="flat", bd=1,
                             cursor="hand2", command=self.on_undo_click,
                             padx=8, pady=2)
        btn_undo.pack(side=tk.LEFT)

        # --- Canvas bàn cờ ---
        self.canvas = tk.Canvas(
            self.board_frame,
            width=BOARD_WIDTH,
            height=BOARD_HEIGHT,
            bg=COLOR_BOARD_BG,
            highlightthickness=0
        )
        self.canvas.pack(side=tk.TOP, pady=5)
        self.canvas.config(highlightbackground=COLOR_GRID, highlightthickness=2)
        
        self.canvas.bind("<Button-1>", self.handle_click)

        # ======== Cột Phải: Điều khiển ========
        self.control_frame = tk.Frame(main_container, bg=COLOR_PANEL_BG, 
                                      padx=20, pady=20, relief="groove", bd=1)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Tiêu đề
        tk.Label(self.control_frame, text="GAME SETTINGS",
                 font=FONT_TITLE, bg=COLOR_PANEL_BG, fg="#5D4037").pack(pady=(0, 20))

        # Chế độ chơi
        lbl_mode = tk.Label(self.control_frame, text="Chế độ chơi:", 
                           font=FONT_BOLD, bg=COLOR_PANEL_BG, fg="#555")
        lbl_mode.pack(anchor="w", pady=(0, 5))
        
        modes = [("Người vs Người", "PVP"), ("Người vs Máy", "PVE"), ("Máy vs Máy", "EVE")]
        for txt, val in modes:
            tk.Radiobutton(self.control_frame, text=txt, variable=self.mode_var, value=val,
                           font=FONT_NORMAL, bg=COLOR_PANEL_BG, activebackground=COLOR_PANEL_BG,
                           cursor="hand2").pack(anchor="w")

        # Độ khó AI
        tk.Label(self.control_frame, text="Độ khó AI:", 
                 font=FONT_BOLD, bg=COLOR_PANEL_BG, fg="#555").pack(anchor="w", pady=(20, 5))
        
        cb_diff = ttk.Combobox(self.control_frame, textvariable=self.diff_var,
                               values=("Dễ", "Trung bình", "Khó"), state="readonly", font=FONT_NORMAL)
        cb_diff.pack(fill=tk.X)

        # Nút Ván mới
        btn_restart = tk.Button(self.control_frame, text="VÁN MỚI",
                  font=FONT_BOLD, bg="#4CAF50", fg="white", 
                  relief="flat", cursor="hand2", pady=10,
                  command=self.on_restart_click)
        btn_restart.pack(fill=tk.X, pady=30)

        # Trạng thái lượt
        self.status_frame = tk.Frame(self.control_frame, bg=COLOR_PANEL_BG)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        self.status_label = tk.Label(
            self.status_frame, text="Lượt: X",
            fg=COLOR_X, bg=COLOR_PANEL_BG, font=("Segoe UI", 18, "bold")
        )
        self.status_label.pack()

    def handle_click(self, event):
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            if self.on_click_callback:
                self.on_click_callback(row, col)

    def redraw_board(self):
        self.canvas.delete("all")

        # 1. Vẽ lưới
        for i in range(BOARD_SIZE + 1):
            self.canvas.create_line(i * CELL_SIZE, 0, i * CELL_SIZE, BOARD_HEIGHT, 
                                    fill=COLOR_GRID, width=1 if i not in [0, BOARD_SIZE] else 0)
            self.canvas.create_line(0, i * CELL_SIZE, BOARD_WIDTH, i * CELL_SIZE, 
                                    fill=COLOR_GRID, width=1 if i not in [0, BOARD_SIZE] else 0)

        # 3. Vẽ quân cờ
        state = self.logic.get_board_state()
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                val = state[r][c]
                if val == 1:
                    self.draw_x(r, c)
                elif val == -1:
                    self.draw_o(r, c)

    def draw_x(self, r, c):
        pad = 8
        x1 = c * CELL_SIZE + pad
        y1 = r * CELL_SIZE + pad
        x2 = (c + 1) * CELL_SIZE - pad
        y2 = (r + 1) * CELL_SIZE - pad
        
        self.canvas.create_line(x1+1, y1+1, x2+1, y2+1, width=3, fill=COLOR_X_SHADOW, capstyle=tk.ROUND)
        self.canvas.create_line(x1+1, y2+1, x2+1, y1+1, width=3, fill=COLOR_X_SHADOW, capstyle=tk.ROUND)
        self.canvas.create_line(x1, y1, x2, y2, width=3, fill=COLOR_X, capstyle=tk.ROUND)
        self.canvas.create_line(x1, y2, x2, y1, width=3, fill=COLOR_X, capstyle=tk.ROUND)

    def draw_o(self, r, c):
        pad = 8
        x1 = c * CELL_SIZE + pad
        y1 = r * CELL_SIZE + pad
        x2 = (c + 1) * CELL_SIZE - pad
        y2 = (r + 1) * CELL_SIZE - pad
        
        self.canvas.create_oval(x1+1, y1+1, x2+1, y2+1, width=3, outline=COLOR_O_SHADOW)
        self.canvas.create_oval(x1, y1, x2, y2, width=3, outline=COLOR_O)

    def update_status(self, text, color="black"):
        display_color = COLOR_X if "X" in text else (COLOR_O if "O" in text else "#333")
        if "thắng" in text: display_color = "#2E7D32"
        self.status_label.config(text=text, fg=display_color)

    def reset_board(self):
        self.logic.reset_board()
        self.redraw_board()
        self.update_status("Lượt: X")

    def on_restart_click(self):
        if self.on_restart_callback:
            self.on_restart_callback()

    def on_undo_click(self):
        if self.on_undo_callback:
            self.on_undo_callback()
