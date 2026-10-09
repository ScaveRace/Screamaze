import pygame
import roomFunc.projRoomFunc as pF

pygame.init()


class ProjectRoom:
    def __init__(self, screen, player, fui):
        self.fui = fui
        self.screen = screen
        self.player = player
        self.next_room = None

        self.view = "room"
        self.holding = None             # the badge in your hand

        self.font = pygame.font.Font(None, 40)
        self.image, self.boxImage = pF.loadImages(screen)
        self.btn = pF.buildButtons(self)
        self.stoneMask = pF.buildMasks(self)
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
