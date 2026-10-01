import UI.uiElements as u
import functions.sound as s
import pygame
from Rooms import frontDesk
import functions.savingFunc as load
from functions.settingsFunc import settings as sett
from player import Player


class StartupMenu:
    def __init__(self, screen,player):
        self.screen = screen
        self.player = player
        self.next_room = None
        self.bgMusic = "assets/music/niceThomas.mp3"
        self.background = u.load_image("assets/startup.png", (screen.get_size()[0]+300,screen.get_size()[1]))
        self.buttons = [
            u.Button(120, 420, 150, 50, "New Game", self.new_game),
            u.Button(120, 470, 150, 50, "Load Game", self.load_game),
            u.Button(120, 520, 150, 50, "Settings",self.settings),
        ]
        s.play_music(self.bgMusic,sett)

    def load_game(self):
        load.load(self.player,"data/savePlayer.json")
        self.player.setImage()
        self.next_room = self.player.location
        return
        print("loading the game")

    def new_game(self):
        print("starting new game")
        self.next_room = "frontD"

    def settings(self):

        print("entering settings menu")

    def handle_event(self, event):
        for b in self.buttons:
            b.handle_event(event)

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        for b in self.buttons:
            b.draw2(self.screen)