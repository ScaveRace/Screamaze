
#####  player data  #####
#  use: from player import player
#  call function like: player.add_item("testitem")

import UI.uiElements as u
SAVE_PATH = "data/savegame.json"


class Player:

    def __init__(self, volume = 1.):
        self.pImage = None
        self.name = ""
        self.time = 0            # seconds, integer
        self.position = "corridor"
        self.inventory = []
        self.volume = volume     # 0.0 - 1.0
        self.gender = ""

    def createPlayer(self,name,gender):
        self.pImage = u.load_image(self.setGenderIm(gender), (64, 64))
        self.name = name
        self.gender = gender

    def getVolume(self):
        return self.volume
    # --- inventory ---
    def add_item(self, item, amount=1):
        for _ in range(amount):
            self.inventory.append(item)


    def setGenderIm(self, g):
        return (f"assets/player/player_{g.lower()}.png")


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

