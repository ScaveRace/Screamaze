import pygame
import UI.uiElements as u

pygame.init()
pygame.mixer.init()

CABINET_CODE = "4537"


class GhostRoom:
    def __init__(self, screen):
        self.default_image = u.load_image("assets/gr.ghostRoom.png", screen.get_size())
        self.current_image = self.default_image
        self.screensize = screen.get_size()
        self.screen = screen
        self.conversation = 0
        self.next_room = None
        self.buttons = [
            u.Button(930, 350, 140, 50, "Search", self.teacher),
            u.Button(580, 50, 140, 50, "Search", self.whiteboard),
            u.Button(140, 500, 140, 50, "Search", self.cabinet),
            u.Button(560, 650, 140, 50, "Return", self.returnc),
        ]
        self.current_buttons = self.buttons
        self.returnr_buttons = [
            u.Button(1000, 520, 140, 50, "return", self.returnr)]

    def teacher(self):
        print("teacher")
        self.current_image = u.load_image("assets/gr.teacher.png", self.screensize)
        self.current_buttons = self.returnr_buttons

    def cabinet(self):
        print("cabinet")
        self.current_image = u.load_image("assets/gr.cabinet.homework.png", self.screensize)
        self.current_buttons = self.returnr_buttons

    def whiteboard(self):
        print("whiteboard")
        self.current_image = u.load_image("assets/gr.whiteboard.4537.png", self.screensize)
        self.current_buttons = self.returnr_buttons

    def returnc(self):
        print("return to corridor")
        self.next_room = "corridor"

    def returnr(self):
        self.current_image = self.default_image
        self.current_buttons = self.buttons

    def handle_event(self, event):
        for b in self.current_buttons:
            b.handle_event(event)

    def draw(self):
        self.screen.blit(self.current_image, (0, 0))
        for b in self.current_buttons:
            b.draw2(self.screen)

