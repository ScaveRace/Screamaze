import pygame
import roomFunc.teachRoomFunc as tF
from Rooms.baseRoom import BaseRoom, register

pygame.init()
pygame.mixer.init()


@register
class TeacherRoom(BaseRoom):
    key = "teacherR"

    def __init__(self, screen, player, fui):
        super().__init__(screen, player, fui)
        self.screensize = screen.get_size()
        tF.start(self)

    def on_enter(self):
        tF.on_enter(self)

    def handle_event(self, event):
        tF.handle_event(self, event)

    def draw(self):
        tF.draw(self)
