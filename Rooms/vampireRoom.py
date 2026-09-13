import pygame

import UI.uiElements as u

pygame.init()
pygame.mixer.init()

class Classroom2015:
    def __init__(self,screen):
        self.screen = screen
        self.image = u.load_image("assets/corridor.png",screen.get_size())
        self.next_room = None
        self.buttons = [
            u.Button(1000,600,50,50,"fdf",self.action),
            u.Button(1000,600,50,50,"rfer",self.action1),
            u.Button(1000,600,50,50,"fver",self.action2),
        ]
        self.text=u.TextField(200,200,40,40)


    def action(self):
        print("hello")

    def action1(self):
        print("s")

    def action2(self):
        print("d")

    def handle_event(self,event):
        for b in self.buttons:
            b.handle_event(event)





    def draw(self):
        self.screen.blit(self.image, (0,0))
        for b in self.buttons:
            b.draw2(self.screen)
        self.text.draw(self.screen)


