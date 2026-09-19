import pygame
import UI.uiElements as u


pygame.init()

pygame.mixer.init()

class Corridor:
    def __init__(self,screen):
        self.image = u.load_image("assets/corridor.png",screen.get_size())
        self.screen = screen
        self.conversation = 0
        self.next_room = None
        self.buttons = [            ### list of all rooms accessible from the corridor
            u.Button(0, 100, 140, 50, "Storr Room", self.storr),
            u.Button(200, 100, 140, 50, "VampRoom", self.vamp),
            u.Button(400, 100, 140, 50, "Ghost Room", self.ghost),
            u.Button(600, 100, 140, 50, "Project Room", self.projRoom),
            u.Button(800, 100, 140, 50, "equinox Room", self.equin),
        ]

    def storr(self):

        self.next_room = "storrR"

    def vamp(self):
        self.next_room = "vampR"

    def ghost(self):
        self.next_room = "ghostR"

    def lab(self):
        self.next_room = "frontD"

    def projRoom(self):
        self.next_room = "projRoom"

    def equin(self):
        self.next_room = "equinR"

    def handle_event(self, event):
      for b in self.buttons:
          b.handle_event(event)

    def draw(self):
        self.screen.blit(self.image, (0, 0))
        for b in self.buttons:
            b.draw2(self.screen)