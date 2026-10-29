import pygame
import UI.uiElements as u
import roomFunc.corrFunc as cF
from Rooms.baseRoom import BaseRoom, register
pygame.init()

pygame.mixer.init()

@register
class Corridor(BaseRoom):
    key = "corridor"

    def __init__(self, screen, player, fui):
        super().__init__(screen, player, fui)
        self.conversation = 0
        self.image = []
        self.elements = []
        self.getElements()


    def getElements(self):
        tmp = cF.getElements(self.player,self.fui,self.screen,self.goTo)
        self.image = tmp[0]
        self.elements = tmp[1]

    def goTo(self, room):
        self.next_room = room


    def handle_event(self, event):
        for e in self.elements:
            e.handle_event(event)


    def draw(self):
        for i in self.image:
            self.screen.blit(i,(300,0))
        for e in self.elements:
            e.draw(self.screen)


        self.player.draw(self.screen)