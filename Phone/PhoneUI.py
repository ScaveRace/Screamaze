import pygame
from Phone.pages.homescreen import HomeScreen, PHONE_SIZE
from Phone.pages.browser import Browser
from Phone.pages.chatPage import ChatPage, CHAT_AREA
from Phone.pages.settingsPage import SettingsPage
from Phone.pages.dialerPage import DialerPage
import UI.uiElements as u
import functions.leaderboard as lb
from player import Player

# every page of the phone: name -> class, a new page is one line here
PAGES = {
    "home": HomeScreen,
    "browser" : Browser,
    "chat": ChatPage,
    "settings": SettingsPage,
    "dialer": DialerPage,
}
HOMEBUTTON = pygame.Rect(130, 655, 40, 40)
HOME_OUTLINE = (140, 140, 140)       # like the home button of the old iPhones: a circle with a rounded square in it
HOME_INNER_SIZE = 16

font = pygame.font.Font(None, 24)

BATTERY = pygame.Rect(250, 32, 24, 12)       # top right of the phone, the body of the battery, the little knob sits on its right
BATTERY_COLOUR = (210, 200, 160)             # the same as the name and the timer

# the phone on the left of the screen, in the place of the chat, it shows one page at a time
class Phone:
    def __init__(self, screen, player, fui):
        self.screen = screen
        self.player = player
        self.fui = fui              # the pages get ARIA and the inventory from it
        self.chat = u.Chatbox(*CHAT_AREA)       # the NPC talks, the rooms add theirs through fui.chat
        self.aiChat = u.Chatbox(*CHAT_AREA)     # the AI chat, the browser page shows it
        self.pages = {name: page(screen, player, self) for name, page in PAGES.items()}
        self.page = "home"

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
        self.drawBattery()
        self.drawHomeButton()

    # a battery of rectangles, it fills with the completion percentage of the game (the same number as on the leaderboard)
    def drawBattery(self):
        percent = lb.completion(self.player)
        pygame.draw.rect(self.screen, BATTERY_COLOUR, BATTERY, 1)                                  # the outline
        pygame.draw.rect(self.screen, BATTERY_COLOUR, (BATTERY.right, BATTERY.centery - 3, 2, 6))  # the knob
        inside = BATTERY.inflate(-6, -6)                                                           # the room for the fill, 2 pixels from the outline
        pygame.draw.rect(self.screen, BATTERY_COLOUR, (inside.x, inside.y, round(inside.width * percent / 100), inside.height))
        text = font.render(f"{percent}%", True, BATTERY_COLOUR)
        self.screen.blit(text, text.get_rect(midright=(BATTERY.left - 6, BATTERY.centery)))

    def drawHomeButton(self):
        self.screen.blit(font.render(f"{self.player.name}", True, (210, 200, 160)), (30, 30))

        seconds = self.player.time
        timeText = font.render(f"{seconds // 60:02d}:{seconds % 60:02d}", True, (210, 200, 160))
        self.screen.blit(timeText, timeText.get_rect(topleft=(130, 30)))
        centre = HOMEBUTTON.center
        pygame.draw.circle(self.screen, (40, 38, 42), centre, HOMEBUTTON.width // 2)
        pygame.draw.circle(self.screen, HOME_OUTLINE, centre, HOMEBUTTON.width // 2, 1)       # the outer outline
        inner = pygame.Rect(0, 0, HOME_INNER_SIZE, HOME_INNER_SIZE)
        inner.center = centre
        pygame.draw.rect(self.screen, HOME_OUTLINE, inner, 1, border_radius=4)                # the inner outline


# runs only the phone, in a window of its size, to build the pages, from the project folder: python -m Phone.PhoneUI
if __name__ == "__main__":
    import player as p
    import AI.aria as aria
    from UI.frontUI import FrontUI
    pygame.init()
    screen = pygame.display.set_mode(PHONE_SIZE, pygame.SCALED | pygame.RESIZABLE)      # resizing keeps its shape
    pygame.display.set_caption("Phone")
    clock = pygame.time.Clock()
    phone = FrontUI(p.Player(), screen, aria).phone       # the phone needs the FrontUI: it gives the pages ARIA and the inventory
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
