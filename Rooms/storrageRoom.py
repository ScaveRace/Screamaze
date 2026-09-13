import pygame

import UI.uiElements as ui

pygame.init()
pygame.mixer.init()

class StorrageRoom:
    def __init__(self, screen):
        self.screen = screen
        self.image = ui.load_image("assets/corridor.png", screen.get_size())
        self.next_room = None
        self.buttons = [
            ui.Button(560, 346, 30,30, "", self.action),
            ui.Button(45, 346, 30,30, "", self.action),
            ui.Button(670, 346, 30,30, "", self.action),
        ]
        self.fieldoftext = ui.TextField(1100, 600, 100, 60)

    def action(self):
       print("actions")

    def handle_event(self, event):
        for b in self.buttons:
            b.handle_event(event)
        self.fieldoftext.handle_event(event)

    def draw(self):
        self.screen.blit(self.image, (0, 0))
        for b in self.buttons:
            b.draw2(self.screen)
        self.fieldoftext.draw(self.screen)
