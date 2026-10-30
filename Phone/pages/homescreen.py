import pygame
import UI.uiElements as u
from Phone.pages.basePage import BasePage

# the phone is a picture of 809 x 1944, drawn 300 x 720 on the left of the screen, where the chat is
# phone_bg.png is the phone without apps, the apps are cut out of phone_full.png, where they sit is in CUT in data/maskPositions.py
A = "assets/phoneIm/"
PHONE_SIZE = (300, 720)
GAME_SIZE = (1480, 720)       # the masks are placed in the fixed size of the game, also when only the phone is on the screen


class HomeScreen(BasePage):

    def __init__(self, screen, player, phone):
        super().__init__(screen, player, phone)
        self.image = u.load_alpha_image(A + "phone_bg.png", PHONE_SIZE)
        self.getElements()

    def getElements(self):
        size = GAME_SIZE
        # u.Mask(file, size, position, callback, label)   no label, the apps are too small for text
        self.chatMask = u.Mask(A + "apps/chat.png", size, (0, 0), self.open_chat, "")
        self.masks = [
            u.Mask(A + "apps/globe.png", size, (0, 0), self.open_globe, ""),
            self.chatMask,
            u.Mask(A + "apps/gear.png", size, (0, 0), self.open_gear, ""),
            u.Mask(A + "apps/handset.png", size, (0, 0), self.open_handset, ""),
        ]

    # what pressing an app does: none of the pages is made yet, later it is self.goTo("<name of the page>")
    def open_globe(self):
        self.goTo("browser")

    def open_chat(self):
        self.goTo("chat")

    def open_gear(self):
        self.goTo("settings")

    def open_handset(self):
        pass

    def handle_event(self, event):
        for m in self.masks:
            m.handle_event(event)

    def draw(self):
        self.screen.blit(self.image, (0, 0))
        for m in self.masks:
            m.draw(self.screen)
        if self.phone.chat.unread:
            self.drawDot()

    # the red dot on the top right of the chat app, when there are messages that were not read
    def drawDot(self):
        corner = self.chatMask.image.get_bounding_rect().move(self.chatMask.imageX, self.chatMask.imageY).topright
        pygame.draw.circle(self.screen, (20, 20, 20), corner, 8)
        pygame.draw.circle(self.screen, (230, 40, 40), corner, 6)
