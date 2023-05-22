import json

__all__ = ["Data"]

class Data:

    __slots__ = ["path", "progress", "entities"]

    def __init__(self) -> None:
        self.path = "data/"
        self.progress = {}
        self.entities = {}

    def load_progress(self):
        with open(self.path + "progress.json", "r") as progress_file:
            self.progress = json.load(progress_file)

    def save_progress(self):
        with open(self.path + "progress.json", "w") as progress_file:
            json.dump(self.progress, progress_file, indent=4)
        
    def load_game_data(self):
        with open(self.path + "entities.json", "r") as progress_file:
            self.entities = json.load(progress_file)