import pygame
import roomFunc.equinRoomFunc as eF

pygame.init()
pygame.mixer.init()

SHAPE_NAME = "Triangle" # one of the three project room badges, exactly this spelling
SHAPE_PATH = "assets/equinoxRoom/triangle.png" # not drawn yet


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
        self.giveShape()
        self.getElements()

    def giveShape(self): # the project room needs this badge, you get it together with the stone
        if eF.has(self, "equin.stone") and not eF.has(self, "equin.shape"):
            self.player.add_item("Items", SHAPE_NAME, SHAPE_PATH) # no image for it yet, the inventory shows a placeholder
            eF.add(self, "equin.shape") # so it is only given once, even after the project room used it

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
