import pygame
import roomFunc.VampFunc as vF
from Rooms.baseRoom import BaseRoom, register

pygame.init()
pygame.mixer.init()

@register
class VampireRoom(BaseRoom):
    key = "vampR"

    def __init__(self, screen, player, fui):
        super().__init__(screen, player, fui)
        self.titleFont = pygame.font.Font(None, 40)

        self.images = {}
        self.buttons = {}
        self.masks = {}
        self.getElements()

    def getElements(self):
        tmp = vF.getElements(self.player, self.fui, self.screen)
        self.images = tmp[0]
        self.buttons = tmp[1]
        self.masks = tmp[2]

    ########## input ##########
    def handle_event(self, event):
        self.dispatch(event)
        self.next_room = vF.next_room
        vF.next_room = None

    def dispatch(self, event):
        # snapshot both lists first, so a click that changes the view
        # can't also click something in the new view
        masks = vF.activeMasks()
        buttons = list(vF.currentButtons())
        viewBefore = vF.view

        for m in masks:
            m.handle_event(event)
            if vF.view != viewBefore:
                return

        for b in buttons:
            b.handle_event(event)
            if vF.view != viewBefore:
                return

    ########## drawing ##########
    def draw(self):
        self.screen.blit(vF.currentImage(), (300, 0))

        for m in vF.activeMasks():
            m.draw(self.screen)

        for b in vF.currentButtons():
            b.draw2(self.screen)