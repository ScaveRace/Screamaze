import pygame
from Phone.pages.homescreen import HomeScreen, PHONE_SIZE
from Phone.pages.bowser import Browser, PHONE_SIZE
from Phone.pages.chatPage import ChatPage, CHAT_AREA
import UI.uiElements as u

# every page of the phone: name -> class, a new page is one line here
PAGES = {
    "home": HomeScreen,
    "browser" : Browser,
    "chat": ChatPage,
}


# the phone on the left of the screen, in the place of the chat, it shows one page at a time
class Phone:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.chat = u.Chatbox(*CHAT_AREA)       # every message of the game, the rooms add theirs through fui.chat, the chat page shows it
        self.pages = {name: page(screen, player, self) for name, page in PAGES.items()}
        self.page = "home"

    def goTo(self, page):
        if page not in self.pages:
            raise KeyError(f"No phone page named {page!r}. Known: {sorted(self.pages)}")
        self.page = page
        self.pages[page].on_enter()

    def handle_event(self, event):
        self.pages[self.page].handle_event(event)

    def draw(self):
        self.pages[self.page].draw()


# runs only the phone, in a window of its size, to build the pages, from the project folder: python -m Phone.PhoneUI
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(PHONE_SIZE, pygame.SCALED | pygame.RESIZABLE)      # resizing keeps its shape
    pygame.display.set_caption("Phone")
    clock = pygame.time.Clock()
    phone = Phone(screen, None)
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
