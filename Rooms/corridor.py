import pygame
import UI.uiElements as u

pygame.init()

pygame.mixer.init()


class Corridor:
    def __init__(self, screen,p, fui):
        self.fui = fui
        self.image = u.load_image("assets/corridor.png", screen.get_size())
        self.p = p
        self.screen = screen
        self.conversation = 0
        self.next_room = None

        self.masks = [
            u.Mask("assets/corridor/room_01.png", self.screen.get_size(), (0, 0), self.ghost, "LAB 2.001"),
            u.Mask("assets/corridor/room_02.png", self.screen.get_size(), (0, 0), self.doPress, "LAB 2.003"),
            u.Mask("assets/corridor/room_03.png", self.screen.get_size(), (0, 0), self.doPress, "Front Desk Office"),
            u.Mask("assets/corridor/room_04.png", self.screen.get_size(), (0, 0), self.vamp, "Classroom 2.015"),
            u.Mask("assets/corridor/room_05.png", self.screen.get_size(), (0, 0), self.doPress, "Classroom 2.021"),
            u.Mask("assets/corridor/room_06.png", self.screen.get_size(), (0, 0), self.doPress, "Teachers Room 4"),
            u.Mask("assets/corridor/room_07.png", self.screen.get_size(), (0, 0), self.doPress, "Classroom 2.031"),
            u.Mask("assets/corridor/room_08.png", self.screen.get_size(), (0, 0), self.doPress, "Stair Exit"),
            u.Mask("assets/corridor/room_09.png", self.screen.get_size(), (0, 0), self.doPress, "Teachers Room 1"),
            u.Mask("assets/corridor/room_10.png", self.screen.get_size(), (0, 0), self.doPress, "Teachers Room 2"),
            u.Mask("assets/corridor/room_11.png", self.screen.get_size(), (0, 0), self.doPress, "Teachers Room 3"),
            u.Mask("assets/corridor/room_12.png", self.screen.get_size(), (0, 0), self.equin,
                   "Equinox Student Society"),
            u.Mask("assets/corridor/room_13.png", self.screen.get_size(), (0, 0), self.projRoom, "Project Room 3"),
            u.Mask("assets/corridor/room_14.png", self.screen.get_size(), (0, 0), self.storr, "Storage"),
            u.Mask("assets/corridor/room_15.png", self.screen.get_size(), (0, 0), self.doPress, "Classroom 2.035"),
            u.Mask("assets/corridor/room_16.png", self.screen.get_size(), (0, 0), self.projRoom, "Project Room 1"),
            u.Mask("assets/corridor/room_17.png", self.screen.get_size(), (0, 0), self.projRoom, "Project Room 2"),
        ]



    def doPress(self):
        self.next_room = "vampR"

    def storr(self):
        self.next_room = "storrR"

    def vamp(self):
        self.next_room = "vampR"

    def ghost(self):
        self.next_room = "ghostR"

    def lab(self):
        self.next_room = "frontD"

    def projRoom(self):
        self.next_room = "projRoom"

    def equin(self):
        self.next_room = "equinR"

    def handle_event(self, event):
        for m in self.masks:
            m.handle_event(event)

    def draw(self):
        self.screen.blit(self.image, (0, 0))
        for m in self.masks:
            m.draw(self.screen)

        self.p.draw(self.screen)