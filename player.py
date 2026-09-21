
#####  player data  #####
#  use: from player import player
#  call function like: player.add_item("testitem")

import json
import os

SAVE_PATH = "savegame.json"


class Player:
    def __init__(self, name="", time=0, position="", inventory=None, volume=1.0):
        self.name = name
        self.time = time            # seconds, integer
        self.position = position
        self.inventory = inventory if inventory is not None else []
        self.volume = volume        # 0.0 - 1.0

    # --- inventory ---
    def add_item(self, item, amount=1):
        for _ in range(amount):
            self.inventory.append(item)

    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False

    def has_item(self, item):
        return item in self.inventory

    def count(self, item):
        return self.inventory.count(item)

    # --- time ---
    def add_time(self, seconds):
        self.time += int(seconds)

    def reset(self):
        self.__init__()

    # --- saving / loading ---
    def to_dict(self):
        return {
            "name": self.name,
            "time": self.time,
            "position": self.position,
            "inventory": self.inventory,
            "volume": self.volume,
        }

    def save(self, path=SAVE_PATH):
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)
        os.replace(tmp, path)

    def load(self, path=SAVE_PATH):
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return False

        self.name = data.get("name", "")
        self.time = int(data.get("time", 0))
        self.position = data.get("position", "")
        self.inventory = list(data.get("inventory", []))
        self.volume = float(data.get("volume", 1.0))
        return True



# for import
player = Player()