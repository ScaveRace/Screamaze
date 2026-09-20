import pygame
import UI.uiElements as u
from player import player

BG = (26, 25, 28)
FG = (222, 222, 214)
DIM = (150, 150, 142)
OK = (150, 200, 150)


class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.paused = False
        self.message = ""
        self.message_until = 0

        w, h = screen.get_size()
        pw, ph = 380, 280
        self.panel = pygame.Rect((w - pw) // 2, (h - ph) // 2, pw, ph)

        # always on screen, top right
        self.pause_button = u.Button(w - 106, 16, 90, 36, "pause", self.toggle)

        cx = self.panel.centerx - 70
        self.buttons = [
            u.Button(cx, self.panel.y + 160, 140, 44, "save game", self.save_game),
            u.Button(cx, self.panel.y + 212, 140, 44, "resume", self.toggle),
        ]
        self.slider = u.Slider(self.panel.x + 40, self.panel.y + 110, pw - 80, 18,
                               "volume", self.set_volume, player.volume)

        self.font = pygame.font.Font(None, 36)
        self.small = pygame.font.Font(None, 24)

        self.set_volume(player.volume)   # apply the saved volume at startup

    # --- actions wired to the widgets ---
    def toggle(self):
        self.paused = not self.paused

    def set_volume(self, value):
        player.volume = value
        pygame.mixer.music.set_volume(value)

    def save_game(self):
        player.save()
        self.flash("saved")

    def flash(self, text, ms=1500):
        self.message = text
        self.message_until = pygame.time.get_ticks() + ms

    # --- main loop hooks ---
    def handle_event(self, event):
        """Return True if the pause UI swallowed the event, so the room
        underneath doesn't also react to the same click."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.toggle()
            return True

        self.pause_button.handle_event(event)

        if self.paused:
            self.slider.handle_event(event)
            for b in self.buttons:
                b.handle_event(event)
            return True
        return False

    def draw(self):
        self.pause_button.draw2(self.screen)
        if not self.paused:
            return

        w, h = self.screen.get_size()
        shade = pygame.Surface((w, h))
        shade.fill((0, 0, 0))
        shade.set_alpha(150)
        self.screen.blit(shade, (0, 0))

        pygame.draw.rect(self.screen, BG, self.panel)
        pygame.draw.rect(self.screen, FG, self.panel, 1)

        title = self.font.render("paused", True, FG)
        self.screen.blit(title, title.get_rect(midtop=(self.panel.centerx,
                                                       self.panel.y + 24)))

        mins, secs = divmod(player.time, 60)
        played = self.small.render(f"time played   {mins:02d}:{secs:02d}", True, DIM)
        self.screen.blit(played, played.get_rect(midtop=(self.panel.centerx,
                                                         self.panel.y + 64)))

        self.slider.draw(self.screen)
        for b in self.buttons:
            b.draw2(self.screen)

        if self.message and pygame.time.get_ticks() < self.message_until:
            note = self.small.render(self.message, True, OK)
            self.screen.blit(note, note.get_rect(midbottom=(self.panel.centerx,
                                                            self.panel.bottom - 10)))