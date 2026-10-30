import pygame
import UI.uiElements as u
import functions.language as lang
from Phone.pages.basePage import BasePage
from Phone.pages.homescreen import PHONE_SIZE

A = "assets/phoneIm/"

# where things are on the phone of 300 x 720, the pause menu covers the top 60
TITLE = pygame.Rect(24, 66, 252, 28)
CHAT_AREA = (24, 98, 252, 556)      # x, y, w, h of the chatbox, the Phone makes it because the rooms need it from the start


# the page of the chat app, the chat itself is the Chatbox in uiElements, this only puts it on the phone
class ChatPage(BasePage):

    def __init__(self, screen, player, phone):
        super().__init__(screen, player, phone)
        self.image = u.load_alpha_image(A + "phone_bg.png", PHONE_SIZE)
        self.titleFont = pygame.font.SysFont(u.Chatbox.CHAT_FONTS, 17, bold=True)

    def on_enter(self):
        for chat in (self.phone.chat, self.phone.aiChat):
            chat.focus = False
        self.phone.shownChat().unread = False

    def handle_event(self, event):
        self.phone.shownChat().handle_event(event)

    def draw(self):
        chat = self.phone.shownChat()       ## the NPC talks or the AI chat, the phone knows from fui.showAiChat
        chat.unread = False                 ## the chat is open, so nothing is new
        self.screen.blit(self.image, (0, 0))
        title = self.titleFont.render(lang.ui("AI chat" if self.phone.fui.showAiChat else "Chat"), True, (206, 206, 200))
        self.screen.blit(title, title.get_rect(center=TITLE.center))
        chat.draw(self.screen)
