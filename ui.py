import tkinter as tk
from tkinter import messagebox

#=================init====================
root = tk.Tk()
root.title("Caro")
root.geometry("800x600")
root.resizable(False, False)

BOARD_SIZE = 15
cell_size = 30
start = 20
board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
current_player = ["X"]
game_mode = ["PVP"]  # PVP, PVE, EVE
difficulty = ["Dễ"]  # Dễ, Trung bình, Khó
#=================Check Win====================
def check_winner(row, col, mark):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for dx, dy in directions:
        count = 1
        i, j = row + dx, col + dy
        while 0 <= i < BOARD_SIZE and 0 <= j < BOARD_SIZE and board[i][j] == mark:
            count += 1
            i += dx
            j += dy
        i, j = row - dx, col - dy
        while 0 <= i < BOARD_SIZE and 0 <= j < BOARD_SIZE and board[i][j] == mark:
            count += 1
            i -= dx
            j -= dy
        if count >= 5:
            return True
    return False

#=========================New Game====================
def new_game():
    canvas.delete("all")
    for i in range(BOARD_SIZE + 1):
        canvas.create_line(start, start + i * cell_size, start + BOARD_SIZE * cell_size, start + i * cell_size)
        canvas.create_line(start + i * cell_size, start, start + i * cell_size, start + BOARD_SIZE * cell_size)
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            board[i][j] = ""
    current_player[0] = "X"
    turn_label.config(text="Lượt: X")
    canvas.bind("<Button-1>", draw_mark)

#=================Menu====================
menu_bar = tk.Menu(root)
game_menu = tk.Menu(menu_bar, tearoff=0)
game_menu.add_command(label="Bắt đầu ván mới", command=new_game)
game_menu.add_command(label="Lưu ván")
game_menu.add_command(label="Thoát", command=root.quit)
menu_bar.add_cascade(label="Trò chơi", menu=game_menu)

help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Luật chơi", command=lambda: messagebox.showinfo("Luật chơi", "Người chơi nào xếp được 5 quân liên tiếp sẽ thắng!"))
help_menu.add_command(label="Thông tin", command=lambda: messagebox.showinfo("Thông tin", "Game Caro Python"))
menu_bar.add_cascade(label="Trợ giúp", menu=help_menu)

root.config(menu=menu_bar)

#=================Giao dien====================
main_frame = tk.Frame(root, bg="#f0f0f0")
main_frame.pack(fill=tk.BOTH, expand=True)

board_frame = tk.Frame(main_frame, bg="white", bd=2, relief=tk.SUNKEN)
board_frame.place(x=20, y=20, width=520, height=520)

canvas = tk.Canvas(board_frame, width=520, height=520, bg="white")
canvas.pack(fill=tk.BOTH, expand=True)

# Ban co
for i in range(16):
    canvas.create_line(start, start + i*cell_size, start + 15*cell_size, start + i*cell_size, fill="gray")
    canvas.create_line(start + i*cell_size, start, start + i*cell_size, start + 15*cell_size, fill="gray")

side_frame = tk.Frame(main_frame, bg="#dfe6e9", bd=2, relief=tk.GROOVE)
side_frame.place(x=550, y=20, width=220, height=500)

tk.Label(side_frame, text="Thông tin người chơi", font=("Arial", 12, "bold"), bg="#dfe6e9").pack(pady=10)
tk.Label(side_frame, text="Người chơi 1: X", font=("Arial", 11), bg="#dfe6e9").pack(pady=5)
tk.Label(side_frame, text="Người chơi 2: O", font=("Arial", 11), bg="#dfe6e9").pack(pady=5)

tk.Button(side_frame, text="Bắt đầu ván mới", font=("Arial", 10), width=20, command=new_game).pack(pady=20)
tk.Button(side_frame, text="Thoát", font=("Arial", 10), width=20, command=root.quit).pack(pady=10)

#=================Luot====================
turn_label = tk.Label(root, text="Lượt: X", font=("Arial", 14))
turn_label.pack(pady=10)

#=================click====================
def draw_mark(event):
    x, y = event.x, event.y
    col = (x - start) // cell_size
    row = (y - start) // cell_size

    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
        if board[row][col] == "":
            px = start + col * cell_size + cell_size / 2
            py = start + row * cell_size + cell_size / 2
            mark = current_player[0]

            color = "red" if mark == "X" else "blue"
            canvas.create_text(px, py, text=mark, fill=color, font=("Arial", 18, "bold"))
            board[row][col] = mark

            if check_winner(row, col, mark):
                messagebox.showinfo("Kết quả", f"Người chơi {mark} thắng!")
                canvas.unbind("<Button-1>")
                return

            if all(board[i][j] != "" for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)):
                messagebox.showinfo("Kết quả", "Hòa!")
                canvas.unbind("<Button-1>")
                return
            
            current_player[0] = "O" if mark == "X" else "X"
            turn_label.config(text=f"Lượt: {current_player[0]}")
        else:
            messagebox.showwarning( "Ô này đã được đánh rồi!")

canvas.bind("<Button-1>", draw_mark)
#========================================
#Menu GameMode
mode_menu = tk.Menu(menu_bar, tearoff=0)
def set_mode(mode):
    game_mode[0] = mode
    new_game()
    turn_label.config(text=f"Chế độ: {mode}")

mode_menu.add_command(label="Người vs Người (PVP)", command=lambda: set_mode("PVP"))
mode_menu.add_command(label="Người vs Máy (PVE)", command=lambda: set_mode("PVE"))
mode_menu.add_command(label="Máy vs Máy (EVE)", command=lambda: set_mode("EVE"))
menu_bar.add_cascade(label="Chế độ chơi", menu=mode_menu)

#Menu do kho
difficulty_menu = tk.Menu(menu_bar, tearoff=0)
def set_difficulty(level):
    difficulty[0] = level
    messagebox.showinfo("Độ khó", f"Đã chọn độ khó: {level}")
difficulty_menu.add_command(label="Dễ", command=lambda: set_difficulty("Dễ"))
difficulty_menu.add_command(label="Trung bình", command=lambda: set_difficulty("Trung bình"))
difficulty_menu.add_command(label="Khó", command=lambda: set_difficulty("Khó"))
menu_bar.add_cascade(label="Độ khó", menu=difficulty_menu)


root.config(menu=menu_bar)
root.mainloop()


