import pygame
import UI.uiElements as ui
from Rooms import corridor

pygame.init()
pygame.mixer.init()

class StorrageRoom:
    def __init__(self, screen):
        self.screen = screen
        self.image = ui.load_image("assets/storrageRoom.png", screen.get_size())
        self.next_room = None
        self.buttons = [
            ui.Button(580, 650, 140,30, "Leave Room", self.leave),
            ui.Button(350, 100, 200,30, "Science equipment", self.action),
            ui.Button(800, 100, 90,30, "Flyers", self.action1),
        ]
        self.fieldoftext = ui.TextField(1100, 600, 100, 60)

    def leave(self):
       self.next_room = "corridor"

    def action(self):
        print("ahwidobhabhej")

    def action1(self):
        print("agubhkwjdjke")

    def handle_event(self, event):
        for b in self.buttons:
            b.handle_event(event)
        self.fieldoftext.handle_event(event)

    def draw(self):
        self.screen.blit(self.image, (0, 0))
        for b in self.buttons:
            b.draw2(self.screen)
        self.fieldoftext.draw(self.screen)
