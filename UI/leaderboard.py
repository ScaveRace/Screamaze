import pygame
import UI.uiElements as u
import functions.leaderboard as lb


font = pygame.font.Font(None, 36)
rowFont = pygame.font.Font(None, 28)

COLUMNS = [770, 815, 990, 1085, 1175]     # x of: place, name, completion, time, finished


class Leaderboard:
    def __init__(self, screen):
        self.screen = screen
        self.visible = False
        self.rows = []
        self.buttons = [
            u.Button(940, 500, 140, 44, "back", self.toggle),
        ]

    def toggle(self):
        self.visible = not self.visible
        if self.visible:
            self.rows = lb.topFive()    # read again every time the page opens

    def handle_event(self, event):
        # returns True when the page used the event, so the menu behind it ignores it
        if not self.visible:
            return False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.toggle()
            return True
        for b in self.buttons:
            b.handle_event(event)
        return True

    def drawRow(self, y, texts, colour):
        for x, text in zip(COLUMNS, texts):
            self.screen.blit(rowFont.render(text, True, colour), (x, y))

    def draw(self):
        if not self.visible:
            return
        panel = pygame.Rect(740, 180, 540, 380)
        pygame.draw.rect(self.screen, (0, 0, 0), panel)
        pygame.draw.rect(self.screen, (255, 255, 255), panel, 1)
        title = font.render("LEADERBOARD", True, (255, 255, 255))
        self.screen.blit(title, title.get_rect(center=(panel.centerx, 215)))

        self.drawRow(255, ["#", "name", "done", "time", ""], (210, 200, 160))
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(765, 282, 490, 1), 1)
        if not self.rows:
            self.drawRow(300, ["", "no saved runs yet", "", "", ""], (222, 222, 214))
        for i, (name, seconds, completion, finished) in enumerate(self.rows):
            time = f"{seconds // 60:02d}:{seconds % 60:02d}"
            done = "finished" if finished else ""
            self.drawRow(300 + i * 36, [str(i + 1), name[:14], f"{completion}%", time, done], (222, 222, 214))

        for b in self.buttons:
            b.draw2(self.screen)
