import pygame
import roomFunc.equinRoomFunc as eF

pygame.init()
pygame.mixer.init()


class EquinoxRoom:
    def __init__(self, screen, player, fui):
        self.fui = fui
        self.screen = screen
        self.player = player
        self.next_room = None

        self.view = "room"
        self.failing = False
        self.fadeStart = 0
        self.fadeAlpha = 0
        self.fadeEnd = None

        self.font = pygame.font.Font(None, 22)
        self.roomImage, self.tableImage, self.fade, self.layers = eF.loadImages(screen)
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
        for m in self.masks:
            m.draw(self.screen)
        eF.drawInfo(self)
        for b in self.buttons:
            b.draw2(self.screen)
        eF.drawFade(self)
