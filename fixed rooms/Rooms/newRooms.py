import pygame
import roomFunc.newRoomFunc as nF
from Rooms.baseRoom import BaseRoom

pygame.init()
pygame.mixer.init()


# one class for all the secondary rooms, what is in a room comes from its file in Rooms/secondaryRooms
class NewRoom(BaseRoom):
    FOLDER = ""
    ELEMENTS = []
    FOUND = {}
    BUTTONS = []
    LOCKS = {}      # element id -> the item that opens its lock, see newRoomFunc.unlock
    CLOSEUPS = {}   # element id -> id of a second close-up inside its changed view, see newRoomFunc.zoom

    def __init__(self, screen, player, fui):
        super().__init__(screen, player, fui)
        self.view = "room"      # "room" or the element you are looking at
        self.image = {}
        self.elements = {}
        self.buttons = []
        self.extra = []         # buttons of this room besides its elements, only in the room view
        self.getElements()

    def getElements(self):
        tmp = nF.getElements(self)
        self.image = tmp[0]
        self.elements = tmp[1]
        self.buttons = tmp[2]
        self.extra = tmp[3]

    def goTo(self, room):
        self.next_room = room

    def handle_event(self, event):
        view = self.view
        if view != "room":      # the back button only exists in a close-up
            for b in self.buttons:
                b.handle_event(event)
        else:
            for b in self.extra:
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
        else:
            for b in self.extra:
                b.draw2(self.screen)



