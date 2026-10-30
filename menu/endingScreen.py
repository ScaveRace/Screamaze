import pygame
import UI.uiElements as u
import UI.leaderboard as leaderboard
import functions.leaderboard as lb
import functions.language as lang
import functions.uiFunc as uF
from Rooms.baseRoom import BaseRoom, register

TABLE = "Ending"
PAGES = ["wake", "skip"]
FADE_IN, HOLD, FADE_OUT = 1500, 3000, 1000
TEXT_COLOUR = (240, 240, 240)
BEDROOM_IMAGE = "assets/bedroom.png"
ANIMATION_DURATION = 8000


def smooth(t):
    t = max(0, min(1, t))
    return t * t * (3 - 2 * t)


@register
class EndingScreen(BaseRoom):
    key = "ending"
    show_ui = False

    def __init__(self, screen, player, fui=None):
        super().__init__(screen, player, fui)
        self.paranormal = False
        self.font = pygame.font.Font(None, 90)
        self.page = 0
        self.pageStart = None
        self.animation_start = pygame.time.get_ticks()
        self.animation_done = False
        self.bedroom = None
        self.blur = []
        try:
            size = self.screen.get_size()
            image = pygame.image.load(BEDROOM_IMAGE).convert()
            image = pygame.transform.smoothscale(image, size)
            self.bedroom = image

            for scale in (16, 8, 4, 2, 1):
                small = pygame.transform.smoothscale(
                    image, (max(1, size[0] // scale),
                            max(1, size[1] // scale))
                )
                self.blur.append(
                    pygame.transform.smoothscale(small, size)
                )

        except (pygame.error, OSError) as e:
            print(f"Bedroom image unavailable: {e}")
        lb.saveRun(player)
        lb.finishRun(player)
        self.board = leaderboard.Leaderboard(screen)
        self.board.toggle()
        self.board.buttons = [
            u.Button(940, 500, 140, 44,
                     lang.chatMessage(TABLE, "menu"), self.menu)]

    def menu(self):
        self.next_room = "startup"

    def nextPage(self):
        self.page += 1
        self.pageStart = pygame.time.get_ticks()

    def handle_event(self, event):
        if not self.animation_done:
            return

        if self.page == len(PAGES):
            self.board.buttons[0].handle_event(event)

        elif ((event.type == pygame.MOUSEBUTTONUP and event.button == 1)
              or (event.type == pygame.KEYDOWN
                  and event.key in (pygame.K_SPACE, pygame.K_RETURN))):
            self.nextPage()

    def alpha(self):
        t = pygame.time.get_ticks() - self.pageStart

        if self.page == len(PAGES):
            return min(255, t * 255 // FADE_IN)

        if t < FADE_IN:
            return t * 255 // FADE_IN
        if t < FADE_IN + HOLD:
            return 255

        return max(0, 255 - (t - FADE_IN - HOLD) * 255 // FADE_OUT)

    def drawText(self, textId, centre, width, show_box=True):
        text = uF.render_wrapped(
            self.font, lang.chatMessage(TABLE, textId),
            TEXT_COLOUR, width)
        alpha = self.alpha()
        text.set_alpha(alpha)
        rect = text.get_rect(center=centre).inflate(90, 70)

        if show_box:
            box = pygame.Surface(rect.size, pygame.SRCALPHA)
            box.fill((0, 0, 0, int(210 * alpha / 255)))
            self.screen.blit(box, rect.topleft)
            pygame.draw.rect(
                self.screen,
                (210, 210, 210),
                rect,
                2)
        self.screen.blit(text, text.get_rect(center=centre))

    def draw_animation(self):
        elapsed = pygame.time.get_ticks() - self.animation_start
        w, h = self.screen.get_size()
        if self.bedroom is None:
            self.screen.fill((0, 0, 0))
        else:
            focus = smooth((elapsed - 3500) / 3500)
            pos = focus * (len(self.blur) - 1)
            low = int(pos)
            high = min(low + 1, len(self.blur) - 1)
            self.screen.blit(self.blur[low], (0, 0))
            if high != low:
                sharp = self.blur[high].copy()
                sharp.set_alpha(int((pos - low) * 255))
                self.screen.blit(sharp, (0, 0))
            dark = pygame.Surface((w, h), pygame.SRCALPHA)
            dark.fill((0, 0, 0, int(130 * (1 - focus))))
            self.screen.blit(dark, (0, 0))
            if elapsed < 500:
                opening = 0
            elif elapsed < 1700:
                opening = .65 * smooth((elapsed - 500) / 1200)
            elif elapsed < 2400:
                opening = .65 * (1 - smooth((elapsed - 1700) / 700))
            elif elapsed < 3200:
                opening = 0
            elif elapsed < 4500:
                opening = .65 * smooth((elapsed - 3200) / 1300)
            elif elapsed < 5200:
                opening = .65 * (1 - smooth((elapsed - 4500) / 700))
            elif elapsed < 6200:
                opening = 0
            else:
                opening = smooth((elapsed - 6200) / 1800)
            if opening < 1:
                mask = pygame.Surface((w, h))
                mask.fill((0, 0, 0))
                gap = int(h * opening / 2)
                pygame.draw.rect(
                    mask, (255, 255, 255),
                    (0, h // 2 - gap, w, gap * 2))
                mask.set_colorkey((255, 255, 255))
                self.screen.blit(mask, (0, 0))
        if elapsed >= ANIMATION_DURATION:
            self.animation_done = True
            self.pageStart = pygame.time.get_ticks()
    def draw(self):
        if not self.animation_done:
            self.draw_animation()
            return
        if self.bedroom:
            self.screen.blit(self.bedroom, (0, 0))
        else:
            self.screen.fill((0, 0, 0))
        w, h = self.screen.get_size()
        if self.page < len(PAGES):
            if pygame.time.get_ticks() - self.pageStart >= FADE_IN + HOLD + FADE_OUT:
                self.nextPage()
            else:
                self.drawText(PAGES[self.page], (w // 2, h // 2), 900)
            return
        board_visible = (
            pygame.time.get_ticks() - self.pageStart >= FADE_IN)
        self.drawText(
            "thanks",
            (370, h // 2),
            600,)
        if board_visible:
            self.board.draw()