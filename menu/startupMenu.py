import UI.uiElements as u
import functions.sound as s
import pygame
from Rooms import frontDesk

class StartupMenu:
    def __init__(self, screen):
        self.screen = screen
        self.next_room = None
        self.bgMusic = "assets/music/The_Unmarked_Door.mp3"
        self.background = u.load_image("assets/startup.png", screen.get_size())
        self.buttons = [
            u.Button(120, 420, 150, 50, "New Game", self.new_game),
            u.Button(120, 470, 150, 50, "Load Game", self.load_game),
            u.Button(120, 520, 150, 50, "Settings",self.settings),
        ]
        s.play_music(self.bgMusic,40)

    def load_game(self):

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




    
    
    