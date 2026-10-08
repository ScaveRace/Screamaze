import pygame
import roomFunc.newRoomFunc as nF

pygame.init()
pygame.mixer.init()


# one class for all the rooms from rooms.json, the key decides which room it is
class NewRoom:
    key = ""

    def __init__(self, screen, player, fui):
        self.fui = fui
        self.player = player
        self.screen = screen
        self.next_room = None
        self.view = "room"      # "room" or the element you are looking at
        self.image = {}
        self.elements = {}
        self.buttons = []
        self.getElements()

    def getElements(self):
        tmp = nF.getElements(self)
        self.image = tmp[0]
        self.elements = tmp[1]
        self.buttons = tmp[2]

    def goTo(self, room):
        self.next_room = room

    def handle_event(self, event):
        view = self.view
        if view != "room":      # the back button only exists in a close-up
            for b in self.buttons:
                b.handle_event(event)
        if self.view == view:   # one click can't press the back button and an element at the same time
            for e in self.elements[view]:
                e.handle_event(event)

    def draw(self):
        self.screen.blit(self.image[self.view], (300, 0))
        for e in self.elements[self.view]:
            e.draw(self.screen)
        if self.view != "room":
            for b in self.buttons:
                b.draw2(self.screen)


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
