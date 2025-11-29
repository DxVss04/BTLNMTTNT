# storage.py
import json
from pathlib import Path

class Storage:
    def __init__(self, db_path="game_data.json"):
        self.db_path = Path(db_path)
        if not self.db_path.exists():
            self._init_db()

    # --------------------------------------------------
    # INIT
    # --------------------------------------------------
    def _init_db(self):
        empty_data = {
            "saved_games": []  # danh sách nhiều game state
        }
        self.save_data(empty_data)

    # --------------------------------------------------
    # LOAD / SAVE RAW DATA
    # --------------------------------------------------
    def load_data(self):
        with open(self.db_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_data(self, data):
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    # --------------------------------------------------
    # SAVE ONE GAME STATE
    # --------------------------------------------------
    def save_game_state(self, game_state):
        """
        game_state dạng:
        {
            "board": [[...], [...], ...],
            "current_player": "X"
        }
        """

        data = self.load_data()
        data["saved_games"].append(game_state)
        self.save_data(data)
        return True

    # --------------------------------------------------
    # GET ALL SAVED GAME STATES
    # --------------------------------------------------
    def get_all_saved_games(self):
        data = self.load_data()
        return data.get("saved_games", [])

    # --------------------------------------------------
    # LOAD A SPECIFIC GAME (index)
    # --------------------------------------------------
    def load_game_by_index(self, index):
        data = self.load_data()
        games = data.get("saved_games", [])
        if 0 <= index < len(games):
            return games[index]
        return None