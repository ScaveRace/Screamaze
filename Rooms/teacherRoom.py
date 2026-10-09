import pygame
import roomFunc.teachRoomFunc as tF

pygame.init()
pygame.mixer.init()


# what the room does is in roomFunc/teachRoomFunc.py
class TeacherRoom:
    def __init__(self, screen, player, fui):
        self.screensize = screen.get_size()
        self.screen = screen
        self.next_room = None
        self.player = player
        self.fui = fui
        tF.start(self)

    def on_enter(self):
        tF.on_enter(self)

    def handle_event(self, event):
        tF.handle_event(self, event)

    def draw(self):
        tF.draw(self)
