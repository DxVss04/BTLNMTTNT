# logic.py
from storage import Storage
import copy

class GameLogic:
    def __init__(self, storage: Storage, board_size=3):
        self.storage = storage
        self.board_size = board_size
        self.board = self._create_empty_board()
        self.current_player = "X"

        # Stack cho undo/redo
        self.history = []       # lưu các trạng thái trước mỗi bước đi
        self.future = []        # lưu các trạng thái undo để redo

    def _create_empty_board(self):
        return [["." for _ in range(self.board_size)]
                for _ in range(self.board_size)]

    # ----------------------------------------------------
    # MOVE
    # ----------------------------------------------------
    def make_move(self, row, col):
        if self.board[row][col] != ".":
            return False, "Invalid move: position is already taken"

        # Save state for undo
        self.history.append(copy.deepcopy(self.board))
        self.future.clear()  # reset redo stack

        self.board[row][col] = self.current_player

        # Check win
        if self.check_win(self.current_player):
            return True, f"Player {self.current_player} wins!"

        # Switch player
        self.current_player = "O" if self.current_player == "X" else "X"
        return True, "Move OK"

    # ----------------------------------------------------
    # WIN CHECK
    # ----------------------------------------------------
    def check_win(self, player):
        b = self.board
        n = self.board_size

        # Check rows
        for r in range(n):
            if all(b[r][c] == player for c in range(n)):
                return True

        # Check columns
        for c in range(n):
            if all(b[r][c] == player for r in range(n)):
                return True

        # Check diagonals
        if all(b[i][i] == player for i in range(n)):
            return True
        if all(b[i][n - 1 - i] == player for i in range(n)):
            return True

        return False

    # ----------------------------------------------------
    # UNDO
    # ----------------------------------------------------
    def undo(self):
        if not self.history:
            return False, "Nothing to undo"

        # Save current state for redo
        self.future.append(copy.deepcopy(self.board))

        # Restore last state
        self.board = self.history.pop()

        # Switch player back
        self.current_player = "O" if self.current_player == "X" else "X"

        return True, "Undo OK"

    # ----------------------------------------------------
    # REDO
    # ----------------------------------------------------
    def redo(self):
        if not self.future:
            return False, "Nothing to redo"

        # Save current state for undo
        self.history.append(copy.deepcopy(self.board))

        # Restore future state
        self.board = self.future.pop()

        # Switch player forward
        self.current_player = "O" if self.current_player == "X" else "X"

        return True, "Redo OK"

    # ----------------------------------------------------
    # RESET GAME
    # ----------------------------------------------------
    def reset(self):
        self.board = self._create_empty_board()
        self.current_player = "X"
        self.history.clear()
        self.future.clear()

    # ----------------------------------------------------
    # OPTIONAL: Save/load game state using storage
    # ----------------------------------------------------
    def save_game(self):
        data = {
            "board": self.board,
            "current_player": self.current_player
        }
        self.storage.add_record({"game_state": data})
        return True

    def load_game(self, game_state):
        self.board = copy.deepcopy(game_state["board"])
        self.current_player = game_state["current_player"]
        self.history.clear()
        self.future.clear()