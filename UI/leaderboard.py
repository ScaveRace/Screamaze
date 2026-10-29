import pygame
import UI.uiElements as u
import functions.leaderboard as lb


font = pygame.font.Font(None, 36)
rowFont = pygame.font.Font(None, 28)

COLUMNS = [770, 815, 950, 1033, 1105, 1175]     # x of: place, name, date, done, time, finished
ROWS = 5                                        # how many rows are shown

# how each header sorts, always smallest first, so the first click is the natural order
SORTS = {
    "#":    lambda r: (-r[2], r[1]),                    # the top 5: highest completion, then fastest
    "name": lambda r: r[0].lower(),                     # A-Z, ignoring capitals
    "date": lambda r: -lb.dateKey(r[4]).toordinal(),    # newest first
    "done": lambda r: (-r[2], r[1]),                    # most done first
    "time": lambda r: r[1]                             #, fastest first
}

class Leaderboard:
    def __init__(self, screen):
        self.screen = screen
        self.visible = False
        self.rows = []
        self.sortKey = "#"
        self.reverse = False
        self.buttons = [
            u.Button(940, 500, 140, 44, "back", self.toggle),
        ]
        for key, x in zip(SORTS, COLUMNS):  # one button per header
            w = rowFont.size(key)[0] + 10
            self.buttons.append(u.Button(x - 5, 250, w, 28, key, lambda key=key: self.sortBy(key)))


    def toggle(self):
        self.visible = not self.visible
        if self.visible:
            self.rows = lb.allRuns()  # changed: was lb.topFive()
            self.sortBy("#")  # new

    def sortBy(self, key):
        if key == self.sortKey and key != "#":
            self.reverse = not self.reverse  # same header again: flip
        else:
            self.sortKey, self.reverse = key, False
        self.rows.sort(key=SORTS[key], reverse=self.reverse)

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


        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(765, 282, 490, 1), 1)
        if not self.rows:
            self.drawRow(300, ["", "no saved runs yet", "", "", ""], (222, 222, 214))
        for i, (name, seconds, completion, finished, d) in enumerate(self.rows[:ROWS]):
            done = "finished" if finished else ""
            self.drawRow(300 + i * 36, [str(i + 1), name[:7], lb.fmtDate(d), f"{completion}%",
                                        lb.fmtTime(seconds), done], (222, 222, 214))

        for b in self.buttons:
            b.draw2(self.screen)
