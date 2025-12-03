import tkinter as tk
from tkinter import ttk, messagebox
from logic import BoardManager

CELL_SIZE = 30
BOARD_SIZE = 15
BOARD_WIDTH = CELL_SIZE * BOARD_SIZE
BOARD_HEIGHT = CELL_SIZE * BOARD_SIZE


class CaroUI:
    def __init__(self, root, on_click_callback=None, on_restart_callback=None):
        self.root = root
        self.root.title("Cờ Caro AI")

        self.on_click_callback = on_click_callback
        self.on_restart_callback = on_restart_callback

        self.logic = BoardManager(size=BOARD_SIZE)

        self.mode_var = tk.StringVar(value="PVP")
        self.diff_var = tk.StringVar(value="Dễ")

        self.setup_layout()
        self.redraw_board()

    # ============================================================
    #   UI Layout
    # ============================================================
    def setup_layout(self):

        # ======== Khung bàn cờ ========
        self.board_frame = tk.Frame(self.root, padx=10, pady=10)
        self.board_frame.pack(side=tk.LEFT)

        self.canvas = tk.Canvas(
            self.board_frame,
            width=BOARD_WIDTH,
            height=BOARD_HEIGHT,
            bg="#F8F8F8"
        )
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.handle_click)

        # Nút undo/redo 
        btn_frame = tk.Frame(self.board_frame)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="⟲ Undo", width=8,
                  command=self.on_undo_click).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Redo ⟳", width=8,
                  command=self.on_redo_click).pack(side=tk.LEFT, padx=5)

        # ======== Khung điều khiển ========
        self.control_frame = tk.Frame(self.root, padx=20, pady=20)
        self.control_frame.pack(side=tk.RIGHT)

        tk.Label(self.control_frame, text="CÀI ĐẶT",
                 font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self.control_frame, text="Chế độ chơi:").pack(anchor="w")
        for txt, val in [("Người vs Người", "PVP"),
                         ("Người vs Máy", "PVE"),
                         ("Máy vs Máy", "EVE")]:
            tk.Radiobutton(self.control_frame, text=txt,
                           variable=self.mode_var, value=val).pack(anchor="w")

        tk.Label(self.control_frame, text="Độ khó AI:").pack(anchor="w", pady=(10, 0))
        ttk.Combobox(self.control_frame,
                     textvariable=self.diff_var,
                     values=("Dễ", "Trung bình", "Khó"),
                     state="readonly").pack(fill=tk.X)

        tk.Button(self.control_frame, text="Ván Mới",
                  font=("Arial", 10, "bold"),
                  bg="#4CAF50", fg="white",
                  command=self.on_restart_click).pack(fill=tk.X, pady=20)

        self.status_label = tk.Label(
            self.control_frame, text="Lượt: X",
            fg="blue", font=("Arial", 12, "bold")
        )
        self.status_label.pack(side=tk.BOTTOM, pady=20)

    # ============================================================
    #   Canvas Interaction
    # ============================================================
    def handle_click(self, event):
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE

        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            if self.on_click_callback:
                self.on_click_callback(row, col)

    # ============================================================
    #   Vẽ bàn cờ
    # ============================================================
    def redraw_board(self):
        """Vẽ lại toàn bộ bàn cờ """
        self.canvas.delete("all")

        # --- Vẽ lưới ---
        for i in range(BOARD_SIZE):
            # dọc
            self.canvas.create_line(i * CELL_SIZE, 0,
                                    i * CELL_SIZE, BOARD_HEIGHT)
            # ngang
            self.canvas.create_line(0, i * CELL_SIZE,
                                    BOARD_WIDTH, i * CELL_SIZE)

        # --- Vẽ X/O ---
        state = self.logic.get_board_state()

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                val = state[r][c]
                if val == 1:
                    self.draw_x(r, c)
                elif val == -1:
                    self.draw_o(r, c)

    def draw_x(self, r, c):
        pad = 4
        x1 = c * CELL_SIZE + pad
        y1 = r * CELL_SIZE + pad
        x2 = (c + 1) * CELL_SIZE - pad
        y2 = (r + 1) * CELL_SIZE - pad
        self.canvas.create_line(x1, y1, x2, y2, width=2, fill="blue")
        self.canvas.create_line(x1, y2, x2, y1, width=2, fill="blue")

    def draw_o(self, r, c):
        pad = 4
        x1 = c * CELL_SIZE + pad
        y1 = r * CELL_SIZE + pad
        x2 = (c + 1) * CELL_SIZE - pad
        y2 = (r + 1) * CELL_SIZE - pad
        self.canvas.create_oval(x1, y1, x2, y2, width=2, outline="red")

    # ============================================================
    #   Update status
    # ============================================================
    def update_status(self, text, color="black"):
        self.status_label.config(text=text, fg=color)

    # ============================================================
    #   Control buttons
    # ============================================================
    def reset_board(self):
        self.logic.reset_board()
        self.redraw_board()
        self.update_status("Lượt: X", "blue")

    def on_restart_click(self):
        if self.on_restart_callback:
            self.on_restart_callback()

    def on_undo_click(self):
        print("")

    def on_redo_click(self):
        print("")


# if __name__ == "__main__":
#     root = tk.Tk()
#     ui = CaroUI(root)
#     root.mainloop()
