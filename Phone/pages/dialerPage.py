import pygame
import UI.uiElements as u
import functions.language as lang
import functions.sound as sound
from functions.settingsFunc import settings as sett
from Phone.pages.basePage import BasePage
from Phone.pages.homescreen import PHONE_SIZE

A = "assets/phoneIm/"

# where things are on the phone of 300 x 720, the top 60 is the name and the timer
TITLE = pygame.Rect(24, 66, 252, 28)
DISPLAY = pygame.Rect(24, 104, 252, 40)
KEYS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "*", "0", "#"]
KEY_SIZE = (76, 48)
KEYS_X, KEYS_Y = 24, 190             # the first key, the others are 88 to the right and 56 below
CALL_BUTTON = pygame.Rect(24, 420, 160, 48)
DELETE_BUTTON = pygame.Rect(196, 420, 80, 48)
MAX_DIGITS = 12

# the numbers that can be called: number -> the sound that plays after pressing call, every other number can't be called
NUMBERS = {
    "911": "assets/soundEffects/phone/call911.mp3",
}


# the page of the handset app: a keypad, a display, and a call button that only works for the numbers in NUMBERS
class DialerPage(BasePage):

    def __init__(self, screen, player, phone):
        super().__init__(screen, player, phone)
        self.image = u.load_alpha_image(A + "phone_bg.png", PHONE_SIZE)
        self.titleFont = pygame.font.SysFont(u.Chatbox.CHAT_FONTS, 17, bold=True)
        self.numberFont = pygame.font.SysFont(u.Chatbox.CHAT_FONTS, 24, bold=True)
        self.smallFont = pygame.font.SysFont(u.Chatbox.CHAT_FONTS, 14)
        self.number = ""
        self.status = ""             # "Calling 911..." after pressing call

        self.keys = []
        for i, label in enumerate(KEYS):
            x = KEYS_X + i % 3 * 88
            y = KEYS_Y + i // 3 * 56
            self.keys.append(u.Button(x, y, KEY_SIZE[0], KEY_SIZE[1], label, None))     # the click is handled in handle_event
        self.callButton = u.Button(*CALL_BUTTON, "Call", self.call)
        self.deleteButton = u.Button(*DELETE_BUTTON, "Delete", self.delete)

    def on_enter(self):
        self.number = ""
        self.status = ""

    def canCall(self):
        return self.number in NUMBERS

    def press(self, label):
        if len(self.number) < MAX_DIGITS:
            self.number += label
        self.status = ""

    def delete(self):
        self.number = self.number[:-1]
        self.status = ""

    def call(self):
        if not self.canCall():
            return
        sound.play_sound(NUMBERS[self.number], sett)
        self.status = "Calling " + self.number + "..."

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for key in self.keys:
                if key.rect.collidepoint(event.pos):
                    self.press(key.label)
        self.deleteButton.handle_event(event)
        if self.canCall():                  # a number that can't be called has a call button that does nothing
            self.callButton.handle_event(event)

    def draw(self):
        self.screen.blit(self.image, (0, 0))
        title = self.titleFont.render(lang.ui("Phone"), True, (206, 206, 200))
        self.screen.blit(title, title.get_rect(center=TITLE.center))

        pygame.draw.rect(self.screen, (0, 0, 0), DISPLAY)
        number = self.numberFont.render(self.number, True, (222, 222, 214))
        self.screen.blit(number, number.get_rect(midright=(DISPLAY.right - 10, DISPLAY.centery)))
        status = self.smallFont.render(self.status, True, (206, 206, 200))
        self.screen.blit(status, status.get_rect(midleft=(DISPLAY.left, DISPLAY.bottom + 18)))

        for key in self.keys:
            key.draw2(self.screen)
        self.deleteButton.draw2(self.screen)
        if self.canCall():
            self.callButton.draw2(self.screen)
        else:                               # grey and without the hover, you can see it can't be pressed
            pygame.draw.rect(self.screen, (28, 28, 28), CALL_BUTTON)
            label = self.callButton.font.render(lang.ui("Call"), True, (90, 90, 90))
            self.screen.blit(label, label.get_rect(center=CALL_BUTTON.center))
