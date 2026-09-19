import pygame
import UI.uiElements as u

pygame.init()

pygame.mixer.init()

class EquinoxRoom:
    def __init__(self, screen):
        self.image = u.load_image("assets/startup.png", screen.get_size()) #  will change
        self.screen = screen
        self.conversation = 0
        self.next_room = None
        self.buttons = [
            u.Button(400, 400, 140, 50, "corridor", self.corridor)#,
            #u.Button(200, 400, 140, 50, "testitem", self.gettestitem)
        ]


    def corridor(self):
        self.next_room = "corridor"

    def handle_event(self, event):
      for b in self.buttons:
          b.handle_event(event)

    def draw(self):
        self.screen.blit(self.image, (0, 0))
        for b in self.buttons:
            b.draw2(self.screen)

