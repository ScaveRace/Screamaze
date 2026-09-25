
#####  player data  #####
#  use: from player import player
#  call function like: player.add_item("testitem")

import json
import os
import UI.uiElements as u
import functions.playerFunc
SAVE_PATH = "data/savegame.json"


class Player:
    def __init__(self, name, time, position, inventory, gender, volume=1.0):
        self.pImage = u.load_image(self.setGenderIm(gender),(64,64))
        self.name = name
        self.time = time            # seconds, integer
        self.position = position
        self.inventory = inventory if inventory is not None else []
        self.volume = volume        # 0.0 - 1.0
        self.gender = gender




# for import
player = Player()