import pygame
import UI.uiElements as u
import roomFunc.corrFunc as cF
pygame.init()

pygame.mixer.init()


class Corridor:
    def __init__(self, screen,p, fui):
        self.fui = fui
        self.p = p
        self.screen = screen
        self.conversation = 0
        self.next_room = None
        self.image = []
        self.elements = []
        self.getElements()


    def getElements(self):
        tmp = cF.getElements(self.p,self.fui,self.screen)
        self.image = tmp[0]
        self.elements = tmp[1]





    def handle_event(self, event):
        for e in self.elements:
            e.handle_event(event)
        self.next_room = cF.next_room
        cF.next_room = None


    def draw(self):
        for i in self.image:
            self.screen.blit(i,(300,0))
        for e in self.elements:
            e.draw(self.screen)


        self.p.draw(self.screen)