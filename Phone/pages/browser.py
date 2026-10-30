import UI.uiElements as u
from Phone.pages.basePage import BasePage
from Phone.pages.homescreen import PHONE_SIZE
import functions.language as lang
import pygame

A = "assets/phoneIm/"
PHONE_SIZE = (300,720)

TITLE = pygame.Rect(24, 66, 252, 28)
TITLE_COLOUR = (40, 38, 42)
TITLE_RADIUS = 10
CHAT_AREA = (24, 98, 252, 556)

class Browser(BasePage):

    def __init__(self, screen, player, phone):
        super().__init__(screen, player, phone)
        self.image = u.load_alpha_image(A + "phone_bg.png", PHONE_SIZE)
        self.titleFont = pygame.font.SysFont(u.Chatbox.CHAT_FONTS, 14, bold=True)
        self.reply = None       # the message of ARIA that is being written, None until the first text arrives

    def on_enter(self):
        self.phone.aiChat.focus = True
        self.phone.aiChat.unread = False

    def handle_event(self, event):
        if self.phone.aiChat.handle_event(event):      # True when the player sent a message
            self.reply = None
            self.phone.fui.aria.ask_in_background(self.phone.aiChat.messages[-1].text, self.addText)

    # the AI sends its answer in small pieces, they all go in one message
    def addText(self, text):
        if not text:
            return
        if self.reply is None:
            self.reply = u.Message("ARIA")
            self.phone.aiChat.add(self.reply)
        self.reply.text += text

    def draw(self):
        self.phone.aiChat.unread = False  ## the chat is open, so nothing is new
        self.screen.blit(self.image, (0, 0))
        pygame.draw.rect(self.screen, TITLE_COLOUR, TITLE, border_radius=TITLE_RADIUS)     # the rounded bar the title sits on
        title = self.titleFont.render(lang.ui("ARIA HELP Chat"), True, (206, 206, 200))
        self.screen.blit(title, title.get_rect(center=TITLE.center))
        self.phone.aiChat.draw(self.screen)




