# main.py - File chính để chạy game Cờ Caro AI

import tkinter as tk
import time  # <--- [MỚI] Thêm thư viện time ở đây
from ui import CaroUI
from logic import BoardManager
from ai_easy import ai_easy_move
from ai_medium import ai_medium_move
from ai_hard import ai_hard_move

class CaroGame:
    def __init__(self):
        self.root = tk.Tk()
        self.ui = CaroUI(
            self.root,
            on_click_callback=self.handle_player_move,
            on_restart_callback=self.restart_game
        )
        self.current_player = 1  # 1: X (người), -1: O (thường là AI)
        self.game_over = False

    def get_ai_function(self):
        """Trả về hàm AI tương ứng với độ khó được chọn"""
        diff = self.ui.diff_var.get()
        if diff == "Dễ":
            return ai_easy_move
        elif diff == "Trung bình":
            return ai_medium_move
        else:  # Khó
            return ai_hard_move

    def handle_player_move(self, row, col):
        """Xử lý khi người chơi click vào ô"""
        if self.game_over:
            return

        mode = self.ui.mode_var.get()

        # Chỉ cho phép người chơi đánh nếu là PVP hoặc PVE và đến lượt X
        if mode == "PVE" and self.current_player == -1:
            return  # Đang lượt AI → không cho click
        if mode == "EVE":
            return  # Máy vs Máy → không cho người click

        if not self.ui.logic.update_board(row, col, self.current_player):
            return  # Ô đã có quân hoặc tọa độ sai

        self.ui.redraw_board()

        if self.ui.logic.check_win(row, col, self.current_player):
            self.end_game(f"{'X' if self.current_player == 1 else 'O'} thắng!")
            return

        if self.ui.logic.is_full():
            self.end_game("Hòa cờ!")
            return

        # Chuyển lượt
        self.current_player = -self.current_player
        self.ui.update_status(f"Lượt: {'X' if self.current_player == 1 else 'O'}",
                              "blue" if self.current_player == 1 else "red")

        # Nếu là PVE hoặc EVE và đến lượt AI → gọi AI đánh
        if (mode == "PVE" and self.current_player == -1) or mode == "EVE":
            self.root.after(500, self.ai_turn)  # Delay 0.5s cho mượt

    def ai_turn(self):
        """Lượt máy đánh"""
        if self.game_over:
            return

        mode = self.ui.mode_var.get()
        if mode == "EVE" and self.current_player == 1:
            # Trong EVE: cả 2 bên đều là AI → lượt X cũng dùng AI
            player_for_ai = 1
        else:
            player_for_ai = self.current_player

        ai_func = self.get_ai_function()

        # ==========================================
        # [MỚI] ĐO THỜI GIAN SUY NGHĨ CỦA AI TẠI ĐÂY
        # ==========================================
        start_time = time.time()     # 1. Bấm giờ
        
        move = ai_func(self.ui.logic, player_for_ai) # AI tính toán
        
        end_time = time.time()       # 2. Ngắt giờ
        
        # 3. In kết quả ra màn hình Console
        diff_name = self.ui.diff_var.get()
        duration = end_time - start_time
        print(f"AI [{diff_name}] đã suy nghĩ mất: {duration:.4f} giây")
        # ==========================================

        if move is None:
            self.end_game("Hòa cờ!")
            return

        row, col = move
        self.ui.logic.update_board(row, col, player_for_ai)
        self.ui.redraw_board()

        if self.ui.logic.check_win(row, col, player_for_ai):
            winner_symbol = 'X' if player_for_ai == 1 else 'O'
            self.end_game(f"{winner_symbol} thắng!")
            return

        if self.ui.logic.is_full():
            self.end_game("Hòa cờ!")
            return

        # Chuyển lượt
        self.current_player = -self.current_player
        self.ui.update_status(f"Lượt: {'X' if self.current_player == 1 else 'O'}",
                              "blue" if self.current_player == 1 else "red")

        # Nếu là EVE → tiếp tục lượt AI ngay
        if mode == "EVE":
            self.root.after(500, self.ai_turn)

    def end_game(self, message):
        self.game_over = True
        color = "green" if "thắng" in message else "orange"
        self.ui.update_status(message, color)

    def restart_game(self):
        self.ui.reset_board()
        self.current_player = 1
        self.game_over = False
        self.ui.update_status("Lượt: X", "blue")
        
        # Tự động bắt đầu nếu là Máy vs Máy
        mode = self.ui.mode_var.get()
        if mode == "EVE":
            self.root.after(800, self.ai_turn)

    def run(self):
        self.root.mainloop()


# Chạy game
if __name__ == "__main__":
    game = CaroGame()
    game.run()
