import pygame
import UI.uiElements as u

pygame.init()
pygame.mixer.init()

font = pygame.font.Font(None, 28)
fontSmall = pygame.font.Font(None, 22)
fontBig = pygame.font.Font(None, 40)





class ProjectRoom:
    def __init__(self, screen):
        self.screen = screen
        self.next_room = None

        self.background = u.load_image("assets/project_room.png", screen.get_size(), (22, 20, 26))
        self.boxImage = u.load_image("assets/", (420, 300), (40, 32, 26))

        self.found = {"circle": False, "triangle": False, "square": False}
        self.placed = {"circle": False, "triangle": False, "square": False}
        self.holding = None
        self.hasFlyer = False

        self.view = "room"
        self.riddleDone = False

        self.message = ""
        self.messageUntil = 0

        self.corners = [
            u.Button(60, 120, 230, 60, "Bookshelf", self.searchShelf),
            u.Button(990, 120, 230, 60, "Whiteboard", self.readRiddle),
            u.Button(60, 560, 230, 60, "Beanbags", self.searchBeanbags),
            u.Button(990, 560, 230, 60, "Locked box", self.openBox),
        ]

        self.riddleButtons = [
            u.Button(340, 420, 200, 50, "Four", self.riddleWrong),
            u.Button(560, 420, 200, 50, "Three", self.riddleRight),
            u.Button(780, 420, 200, 50, "Eight", self.riddleWrong),
        ]

        self.backButton = u.Button(60, 650, 160, 45, "Back", self.backToRoom)
        self.leaveButton = u.Button(540, 650, 200, 45, "Leave the room", self.leave)

        self.slots = {
            "circle": (450, 300),
            "triangle": (580, 300),
            "square": (710, 300),
        }
        self.slotSize = 100

    def searchShelf(self):
        if self.found["circle"]:
            self.say("Nothing else behind the books.")
        else:
            self.found["circle"] = True
            self.say("A round wooden disc was wedged between two folders.")

    def searchBeanbags(self):
        if self.found["square"]:
            self.say("Just crumbs down there.")
        else:
            self.found["square"] = True
            self.say("Under the beanbag: a square block.")

    def readRiddle(self):
        if self.found["triangle"]:
            self.say("The whiteboard is wiped clean now.")
        else:
            self.view = "riddle"

    def openBox(self):
        self.view = "box"

    def riddleRight(self):
        self.found["triangle"] = True
        self.riddleDone = True
        self.view = "room"
        self.say("The marker tray slides open. A triangle falls out.")

    def riddleWrong(self):
        self.say("Nothing happens.")

    def pickUp(self, shape):
        if self.found[shape] and not self.placed[shape]:
            self.holding = shape

    def tryPlace(self, slot):
        if self.holding is None:
            return
        if self.holding == slot:
            self.placed[slot] = True
            self.holding = None
            self.say("It clicks into place.")
            if all(self.placed.values()):
                self.hasFlyer = True
                self.say("The lid springs open. Inside is a flyer: EQUINOX STUDENT SOCIETY.")
        else:
            self.holding = None
            self.say("That does not fit.")

    def backToRoom(self):
        self.view = "room"
        self.holding = None

    def leave(self):
        self.next_room = "corridor"

    def say(self, text):
        self.message = text
        self.messageUntil = pygame.time.get_ticks() + 4000

    def handle_event(self, event):
        if self.view == "room":
            for b in self.corners:
                b.handle_event(event)

        elif self.view == "riddle":
            for b in self.riddleButtons:
                b.handle_event(event)
            self.backButton.handle_event(event)

        elif self.view == "box":
            self.backButton.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.boxClick(event.pos)
        self.leaveButton.handle_event(event)

    def boxClick(self, pos):
        x = 420
        for shape in ("circle", "triangle", "square"):
            if self.found[shape] and not self.placed[shape]:
                if pygame.Rect(x, 470, 90, 90).collidepoint(pos):
                    self.pickUp(shape)
                x = x + 110

        for shape in self.slots:
            sx, sy = self.slots[shape]
            if pygame.Rect(sx, sy, self.slotSize, self.slotSize).collidepoint(pos):
                self.tryPlace(shape)

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        if self.view == "room":
            self.drawRoom()
        elif self.view == "riddle":
            self.drawRiddle()
        elif self.view == "box":
            self.drawBox()

        self.drawMessage()

    def drawRoom(self):
        title = fontBig.render("PROJECT ROOM 1", True, (230, 225, 235))
        self.screen.blit(title, (60, 50))

        for b in self.corners:
            b.draw2(self.screen)

        x = 60
        for shape in ("circle", "triangle", "square"):
            if self.found[shape] and not self.placed[shape]:
                self.drawShape(shape, x, 300, 70, (215, 190, 130))
                x = x + 90

        if self.hasFlyer:
            self.screen.blit(font.render("You have the Equinox flyer.", True, (210, 200, 160)), (60, 420))
        self.leaveButton.draw2(self.screen)

    def drawRiddle(self):
        panel = pygame.Surface((760, 300))
        panel.fill((18, 18, 20))
        panel.set_alpha(220)
        self.screen.blit(panel, (260, 180))
        pygame.draw.rect(self.screen, (200, 200, 200), pygame.Rect(260, 180, 760, 300), 1)

        lines = [
            "Written across the whiteboard:",
            "",
            "I have three sides and stand on one.",
            "How many corners do I have?",
        ]
        y = 210
        for text in lines:
            self.screen.blit(font.render(text, True, (235, 235, 235)), (300, y))
            y = y + 38

        for b in self.riddleButtons:
            b.draw2(self.screen)
        self.backButton.draw2(self.screen)

    def drawBox(self):
        self.screen.blit(self.boxImage, (420, 180))
        pygame.draw.rect(self.screen, (170, 150, 120), pygame.Rect(420, 180, 420, 300), 1)

        for shape in self.slots:
            sx, sy = self.slots[shape]
            if self.placed[shape]:
                self.drawShape(shape, sx, sy, self.slotSize, (215, 190, 130))
            else:
                self.drawShape(shape, sx, sy, self.slotSize, (90, 80, 70))

        x = 420
        for shape in ("circle", "triangle", "square"):
            if self.found[shape] and not self.placed[shape]:
                color = (255, 235, 170) if self.holding == shape else (215, 190, 130)
                self.drawShape(shape, x, 470, 90, color)
                x = x + 110

        if self.hasFlyer:
            self.screen.blit(font.render("EQUINOX STUDENT SOCIETY - open evening", True, (230, 215, 160)), (420, 600))
        elif self.holding is None:
            self.screen.blit(fontSmall.render("Click a shape, then click the hole it belongs in.", True, (170, 170, 170)), (420, 600))
        else:
            self.screen.blit(fontSmall.render("Now click a hole.", True, (170, 170, 170)), (420, 600))

        self.backButton.draw2(self.screen)

    def drawShape(self, shape, x, y, size, color):
        if shape == "circle":
            pygame.draw.circle(self.screen, color, (x + size // 2, y + size // 2), size // 2, 3)
        elif shape == "square":
            pygame.draw.rect(self.screen, color, pygame.Rect(x, y, size, size), 3)
        elif shape == "triangle":
            points = [(x + size // 2, y), (x, y + size), (x + size, y + size)]
            pygame.draw.polygon(self.screen, color, points, 3)

    def drawMessage(self):
        if self.message != "" and pygame.time.get_ticks() < self.messageUntil:
            text = font.render(self.message, True, (235, 230, 220))
            self.screen.blit(text, (60, 690))