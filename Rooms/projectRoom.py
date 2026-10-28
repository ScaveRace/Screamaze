import pygame
import roomFunc.projRoomFunc as pF
from Rooms.baseRoom import BaseRoom, register

pygame.init()

@register
class ProjectRoom(BaseRoom):
    key ="projRoom"

    def __init__(self, screen, player, fui):
        super().__init__(screen, player, fui)

        self.view = "room"
        self.holding = None             # the badge in your hand

        self.font = pygame.font.Font(None, 40)
        self.smallFont = pygame.font.Font(None, 28)
        self.image, self.boxImage, self.shapes = pF.loadImages(screen)
        self.btn = pF.buildButtons(self)
        self.allMasks = pF.buildMasks(self)
        self.buttons, self.masks = [], []

        pF.intro(self)
        self.getElements()

    def getElements(self):
        self.buttons, self.masks = pF.getElements(self)

    def handle_event(self, event):
        for m in self.masks:
            m.handle_event(event)
        for b in self.buttons:
            b.handle_event(event)
        self.getElements()

    def draw(self):
        pF.drawScene(self)
        for m in self.masks:
            m.draw(self.screen)
        for b in self.buttons:
            b.draw2(self.screen)
