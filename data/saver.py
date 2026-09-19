import pygame
import json
class savedata:
    def __init__(self, keylist=[], inventory=[], time=0, volume_setting=100):
        self.keylist = []
        self.inventory = []
        self.time = 0
        self.volume_setting = 100


    def save_game(save):
        data = {
                "keylist": save.keylist,
                "inventory": save.inventory,
                "time": save.time,
                "volume_setting": save.volume_setting
        }

        with open("savegame.json", "w") as file:
            json.dump(data, file, indent=4)
    def addkey(self, key):
        self.keylist.append(key)

    def addinv(self, item):
        self.inventory.append(item)

    def timepenalty(self, penalty):
        self.time += penalty

    def setvolume(self, volume):
        self.volume_setting = volume