import pygame
import UI.uiElements as u
import UI.leaderboard as leaderboard
import functions.leaderboard as lb
import functions.language as lang
import functions.uiFunc as uF
from Rooms.baseRoom import BaseRoom, register

TABLE = "Ending"                # the texts are in the language files under this name
PAGES = ["wake", "skip"]        # the big letters, one after the other. After them comes the thank you page
FADE_IN = 1500                  # milliseconds a page takes to fade in, stay, and fade out
HOLD = 3000
FADE_OUT = 1000
TEXT_COLOUR = (230, 225, 235)


@register
class EndingScreen(BaseRoom):
    key = "ending"
    show_ui = False

    def __init__(self, screen, player, fui=None):
        super().__init__(screen, player, fui)

        self.font = pygame.font.Font(None, 90)
        self.page = 0
        self.pageStart = pygame.time.get_ticks()

        lb.saveRun(player)                              # the run goes on the leaderboard, saved or not
        lb.finishRun(player)                            # and is marked as finished, with the time it ended on

        # the same leaderboard as on the title screen, open from the start, its button takes you back to the menu
        # (after the run is saved, because it reads the rows when it opens)
        self.board = leaderboard.Leaderboard(screen)
        self.board.toggle()
        self.board.buttons = [u.Button(940, 500, 140, 44, lang.chatMessage(TABLE, "menu"), self.menu)]

    def menu(self):
        self.next_room = "startup"

    def nextPage(self):
        self.page += 1
        self.pageStart = pygame.time.get_ticks()

    def handle_event(self, event):
        if self.page == len(PAGES):                     # thank you page: only the menu button
            self.board.buttons[0].handle_event(event)
        elif (event.type == pygame.MOUSEBUTTONUP and event.button == 1) or \
                (event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_RETURN)):
            self.nextPage()                             # skip to the next text

    def alpha(self):
        t = pygame.time.get_ticks() - self.pageStart
        if self.page == len(PAGES):                     # the last page fades in and stays
            return min(255, t * 255 // FADE_IN)
        if t < FADE_IN:
            return t * 255 // FADE_IN
        if t < FADE_IN + HOLD:
            return 255
        return max(0, 255 - (t - FADE_IN - HOLD) * 255 // FADE_OUT)

    def drawText(self, textId, centre, width):
        text = uF.render_wrapped(self.font, lang.chatMessage(TABLE, textId), TEXT_COLOUR, width)
        text.set_alpha(self.alpha())
        self.screen.blit(text, text.get_rect(center=centre))

    def draw(self):
        self.screen.fill((0, 0, 0))
        w, h = self.screen.get_size()

        if self.page < len(PAGES):
            if pygame.time.get_ticks() - self.pageStart >= FADE_IN + HOLD + FADE_OUT:
                self.nextPage()                         # this one has faded out
            else:
                self.drawText(PAGES[self.page], (w // 2, h // 2), 1100)
            return

        self.drawText("thanks", (370, h // 2), 600)     # thank you on the left, the leaderboard on the right
        if pygame.time.get_ticks() - self.pageStart >= FADE_IN:
            self.board.draw()
