import pygame
import roomFunc.newRoomFunc as nF
import Rooms.secondaryRooms.lab2001 as lab2001
import Rooms.secondaryRooms.frontDeskOffice as frontDeskOffice
import Rooms.secondaryRooms.classroom2021 as classroom2021
import Rooms.secondaryRooms.classroom2031 as classroom2031
import Rooms.secondaryRooms.classroom2035 as classroom2035
import Rooms.secondaryRooms.stairExit as stairExit
import Rooms.secondaryRooms.teachersRoom1 as teachersRoom1
import Rooms.secondaryRooms.teachersRoom2 as teachersRoom2
import Rooms.secondaryRooms.teachersRoom3 as teachersRoom3
import Rooms.secondaryRooms.teachersRoom4 as teachersRoom4
import Rooms.secondaryRooms.projectRoom1 as projectRoom1
import Rooms.secondaryRooms.projectRoom2 as projectRoom2

pygame.init()
pygame.mixer.init()


# one class for all the secondary rooms, what is in a room comes from its file in Rooms/secondaryRooms
class NewRoom:
    key = ""        # name of the room in main.py and in the language files
    data = None     # the file of the room in Rooms/secondaryRooms

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
    data = lab2001

class FrontDeskOffice(NewRoom):
    key = "frontDeskR"
    data = frontDeskOffice

class Classroom2021(NewRoom):
    key = "class2021R"
    data = classroom2021

class Classroom2031(NewRoom):
    key = "class2031R"
    data = classroom2031

class Classroom2035(NewRoom):
    key = "class2035R"
    data = classroom2035

class StairExit(NewRoom):
    key = "stairR"
    data = stairExit

class TeachersRoom1(NewRoom):
    key = "teach1R"
    data = teachersRoom1

class TeachersRoom2(NewRoom):
    key = "teach2R"
    data = teachersRoom2

class TeachersRoom3(NewRoom):
    key = "teach3R"
    data = teachersRoom3

class TeachersRoom4(NewRoom):
    key = "teach4R"
    data = teachersRoom4

class ProjectRoom1(NewRoom):
    key = "projRoom1R"
    data = projectRoom1

class ProjectRoom2(NewRoom):
    key = "projRoom2R"
    data = projectRoom2
