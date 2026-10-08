import pygame
import roomFunc.projRoomFunc as pF

pygame.init()
pygame.mixer.init()

########## fonts ##########
font = pygame.font.Font(None, 28)
fontSmall = pygame.font.Font(None, 22)
fontBig = pygame.font.Font(None, 40)


########## project room class ##########
class ProjectRoom:

    def __init__(self, screen, p, fui):
        self.fui = fui
        self.p = p
        self.screen = screen
        self.next_room = None
        self.image = []
        self.buttons = {}
        self.getElements()

    def getElements(self):
        tmp = pF.getElements(self.p, self.fui, self.screen)
        self.image = tmp[0]
        self.buttons = tmp[1]

    ########## handle user input depending on current view ##########
    def handle_event(self, event):
        if pF.view == "room":
            for b in self.buttons["corners"]:
                b.handle_event(event)

        elif pF.view == "riddle":
            for b in self.buttons["riddle"]:
                b.handle_event(event)
            self.buttons["back"].handle_event(event)

        elif pF.view == "box":
            self.buttons["back"].handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pF.boxClick(event.pos)

        self.buttons["leave"].handle_event(event)
        self.next_room = pF.next_room
        pF.next_room = None

    ########## draw the current project room view ##########
    def draw(self):
        self.screen.blit(self.image[0], (0, 0))

        if pF.view == "room":
            self.drawRoom()

        elif pF.view == "riddle":
            self.drawRiddle()

        elif pF.view == "box":
            self.drawBox()

        self.drawMessage()

    ########## draw main room ##########
    def drawRoom(self):
        title = fontBig.render("PROJECT ROOM 1", True, (230, 225, 235))
        self.screen.blit(title, (60, 50))

        for b in self.buttons["corners"]:
            b.draw2(self.screen)

        ########## display collected shapes ##########
        x = 60
        for shape in ("circle", "triangle", "square"):
            if pF.found[shape] and not pF.placed[shape]:
                self.drawShape(shape, x, 300, 70, (215, 190, 130))
                x = x + 90

        ########## display flyer after solving the box ##########
        if pF.hasFlyer:
            self.screen.blit(
                font.render("You have the Equinox flyer.", True, (210, 200, 160)),
                (60, 420)
            )

        self.buttons["leave"].draw2(self.screen)

    ########## draw whiteboard riddle ##########
    def drawRiddle(self):
        panel = pygame.Surface((760, 300))
        panel.fill((18, 18, 20))
        panel.set_alpha(220)
        self.screen.blit(panel, (260, 180))

        pygame.draw.rect(
            self.screen,
            (200, 200, 200),
            pygame.Rect(260, 180, 760, 300),
            1
        )

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

        for b in self.buttons["riddle"]:
            b.draw2(self.screen)

        self.buttons["back"].draw2(self.screen)

    ########## draw locked box and shape puzzle ##########
    def drawBox(self):
        self.screen.blit(self.image[1], (420, 180))

        pygame.draw.rect(
            self.screen,
            (170, 150, 120),
            pygame.Rect(420, 180, 420, 300),
            1
        )

        ########## draw the three shape slots ##########
        for shape in pF.slots:
            sx, sy = pF.slots[shape]

            if pF.placed[shape]:
                self.drawShape(shape, sx, sy, pF.slotSize, (215, 190, 130))
            else:
                self.drawShape(shape, sx, sy, pF.slotSize, (90, 80, 70))

        ########## draw collected shapes below the box ##########
        x = 420

        for shape in ("circle", "triangle", "square"):
            if pF.found[shape] and not pF.placed[shape]:
                color = (255, 235, 170) if pF.holding == shape else (215, 190, 130)
                self.drawShape(shape, x, 470, 90, color)
                x = x + 110

        ########## display instructions or reward ##########
        if pF.hasFlyer:
            self.screen.blit(
                font.render(
                    "EQUINOX STUDENT SOCIETY - open evening",
                    True,
                    (230, 215, 160)
                ),
                (420, 600)
            )

        elif pF.holding is None:
            self.screen.blit(
                fontSmall.render(
                    "Click a shape, then click the hole it belongs in.",
                    True,
                    (170, 170, 170)
                ),
                (420, 600)
            )

        else:
            self.screen.blit(
                fontSmall.render(
                    "Now click a hole.",
                    True,
                    (170, 170, 170)
                ),
                (420, 600)
            )

        self.buttons["back"].draw2(self.screen)

    ########## draw the different puzzle shapes ##########
    def drawShape(self, shape, x, y, size, color):
        if shape == "circle":
            pygame.draw.circle(
                self.screen,
                color,
                (x + size // 2, y + size // 2),
                size // 2,
                3
            )

        elif shape == "square":
            pygame.draw.rect(
                self.screen,
                color,
                pygame.Rect(x, y, size, size),
                3
            )

        elif shape == "triangle":
            points = [
                (x + size // 2, y),
                (x, y + size),
                (x + size, y + size)
            ]
            pygame.draw.polygon(self.screen, color, points, 3)

    ########## display temporary messages ##########
    def drawMessage(self):
        if pF.message != "" and pygame.time.get_ticks() < pF.messageUntil:
            text = font.render(
                pF.message,
                True,
                (235, 230, 220)
            )
            self.screen.blit(text, (60, 690))