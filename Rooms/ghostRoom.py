import pygame
import UI.uiElements as u


pygame.init()

pygame.mixer.init()

class GhostRoom:
    def __init__(self,screen):
        self.image = u.load_image("assets/corridor.png",screen.get_size())
        self.screen = screen
        self.conversation = 0
        self.next_room = None
        self.buttons = [
            u.Button(930, 350, 140, 50, "Start Run", self.teacher),
            u.Button(0, 350, 140, 50, "Start Run", self.teacher),
            u.Button(200, 350, 140, 50, "Start Run", self.teacher),
            u.Button(200, 350, 140, 50, "Start Run", self.teacher),
            u.Button(600, 350, 140, 50, "Start Run", self.teacher),
        ]



    def teacher(self):
        print("teacher")




    def handle_event(self, event):
      for b in self.buttons:
          b.handle_event(event)

    def draw(self):
        self.screen.blit(self.image, (0, 0))
        for b in self.buttons:
            b.draw2(self.screen)