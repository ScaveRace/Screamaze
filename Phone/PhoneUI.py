import pygame
from Phone.pages.homescreen import HomeScreen, PHONE_SIZE
from Phone.pages.browser import Browser, PHONE_SIZE
from Phone.pages.chatPage import ChatPage, CHAT_AREA
from Phone.pages.settingsPage import SettingsPage
import UI.uiElements as u

# every page of the phone: name -> class, a new page is one line here
PAGES = {
    "home": HomeScreen,
    "browser" : Browser,
    "chat": ChatPage,
    "settings": SettingsPage,
}
HOMEBUTTON = pygame.Rect(135, 660, 30, 30)

# the phone on the left of the screen, in the place of the chat, it shows one page at a time
class Phone:
    def __init__(self, screen, player, fui):
        self.screen = screen
        self.player = player
        self.fui = fui              # fui.showAiChat says which of the two chats the chat page shows
        self.chat = u.Chatbox(*CHAT_AREA)       # the NPC talks, the rooms add theirs through fui.chat
        self.aiChat = u.Chatbox(*CHAT_AREA)     # the AI chat
        self.pages = {name: page(screen, player, self) for name, page in PAGES.items()}
        self.page = "home"

    # the chat page shows the NPC talks (the chat app) or the AI chat (the handset app)
    def openChat(self, ai):
        self.fui.showAiChat = ai
        self.goTo("chat")

    def shownChat(self):
        return self.aiChat if self.fui.showAiChat else self.chat

    def goTo(self, page):
        if page not in self.pages:
            raise KeyError(f"No phone page named {page!r}. Known: {sorted(self.pages)}")
        self.page = page
        self.pages[page].on_enter()

    def handle_event(self, event):
        self.pages[self.page].handle_event(event)
        if event.type == pygame.MOUSEBUTTONUP:
            if HOMEBUTTON.collidepoint(pygame.mouse.get_pos()):
                self.goTo("home")

    def draw(self):

        self.pages[self.page].draw()
        pygame.draw.rect(self.screen, (40, 38, 42), HOMEBUTTON, border_radius=10)




# runs only the phone, in a window of its size, to build the pages, from the project folder: python -m Phone.PhoneUI
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(PHONE_SIZE, pygame.SCALED | pygame.RESIZABLE)      # resizing keeps its shape
    pygame.display.set_caption("Phone")
    clock = pygame.time.Clock()
    import player as p
    from UI.frontUI import FrontUI
    phone = FrontUI(p.Player(), screen).phone       # the phone needs the FrontUI, it keeps showAiChat
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            phone.handle_event(event)
        phone.draw()
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
