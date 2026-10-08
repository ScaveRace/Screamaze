import pygame
import UI.uiElements as u
import roomFunc.newRoomFunc as nF

pygame.init()
pygame.mixer.init()


# one class for all the rooms from rooms.json, the key decides which room it is
class NewRoom:
    key = ""

    def __init__(self, screen, player, fui):
        self.screen = screen
        self.player = player
        self.fui = fui
        self.next_room = None

        self.element = None     # the element you are looking at, None = the room itself
        self.povImages = {}     # path -> close-up picture
        self.labelFont = pygame.font.Font(None, 24)

        self.image = None
        self.masks = []         # (Mask, label) of every element in the room
        self.hotspots = {}      # element id -> Mask of the clickable part of its close-up
        self.getElements()
        self.backButton = u.Button(1320, 650, 140, 50, "Back", lambda: nF.back(self))
        self.corridorButton = u.Button(1280, 650, 180, 50, "Back to corridor", lambda: nF.leave(self))

    def getElements(self):
        tmp = nF.getElements(self)
        self.image = tmp[0]
        self.masks = tmp[1]
        self.hotspots = tmp[2]

    ########## handle user input depending on current view ##########
    def handle_event(self, event):
        if self.element is None:
            for mask, label in self.masks:
                mask.handle_event(event)
                if self.element is not None:
                    return  # a click that opens a close-up can't also click inside it
            self.corridorButton.handle_event(event)
            return

        # the back button goes first: some hotspots are so big that the button sits on top of them
        self.backButton.handle_event(event)
        if self.element is None:
            return
        hotspot = nF.activeHotspot(self)
        if hotspot:
            hotspot.handle_event(event)

    ########## draw the room or the close-up of an element ##########
    def draw(self):
        if self.element is None:
            self.screen.blit(self.image, (300, 0))
            for mask, label in self.masks:
                mask.draw(self.screen)
            for mask, label in self.masks:
                if mask.hovering:
                    self.drawLabel(label)
            self.corridorButton.draw2(self.screen)
            return

        self.screen.blit(nF.povImage(self), (300, 0))
        hotspot = nF.activeHotspot(self)
        if hotspot:
            hotspot.draw(self.screen)
        self.backButton.draw2(self.screen)

    # name of the element under the mouse, drawn just above the cursor
    def drawLabel(self, label):
        text = self.labelFont.render(label, True, (255, 255, 255))
        rect = text.get_rect(midbottom=pygame.mouse.get_pos()).move(0, -12)
        rect.clamp_ip(pygame.Rect(300, 0, self.screen.get_width() - 300, self.screen.get_height()))
        pygame.draw.rect(self.screen, (0, 0, 0), rect.inflate(10, 6))
        self.screen.blit(text, rect)


class Lab2001(NewRoom):
    key = "lab2001R"

class FrontDeskOffice(NewRoom):
    key = "frontDeskR"

class Classroom2021(NewRoom):
    key = "class2021R"

class Classroom2031(NewRoom):
    key = "class2031R"

class Classroom2035(NewRoom):
    key = "class2035R"

class StairExit(NewRoom):
    key = "stairR"

class TeachersRoom1(NewRoom):
    key = "teach1R"

class TeachersRoom2(NewRoom):
    key = "teach2R"

class TeachersRoom3(NewRoom):
    key = "teach3R"

class TeachersRoom4(NewRoom):
    key = "teach4R"
