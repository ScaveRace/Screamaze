import pygame
import roomFunc.equinRoomFunc as eF
from Rooms.baseRoom import BaseRoom, register

pygame.init()
pygame.mixer.init()

@register
class EquinoxRoom(BaseRoom):
    key = "equinR"
    def __init__(self, screen, player, fui):
        super().__init__(screen, player, fui)

        self.view = "room"
        self.failing = False
        self.fadeStart = 0
        self.fadeAlpha = 0
        self.fadeEnd = None

        self.font = pygame.font.Font(None, 22)
        self.transformStart = 0
        self.roomImage, self.tableImage, self.fade, self.layers, self.demon = eF.loadImages(screen)
        self.allMasks = eF.buildMasks(self)
        self.btn = eF.buildButtons(self)
        self.images, self.masks, self.buttons = [], [], []

        eF.intro(self)
        self.getElements()

    def getElements(self):
        self.images, self.masks, self.buttons = eF.getElements(self)

    def handle_event(self, event):
        if not self.failing:
            for m in self.masks:
                m.handle_event(event)
            for b in self.buttons:
                b.handle_event(event)
        self.getElements()

    def draw(self):
        for image, pos in self.images:
            self.screen.blit(image, pos)
        eF.drawDemon(self)
        for m in self.masks:
            m.draw(self.screen)
        eF.drawInfo(self)
        for b in self.buttons:
            b.draw2(self.screen)
        eF.drawFade(self)
