import pygame
import UI.uiElements as u

pygame.init()

pygame.mixer.init()


class Corridor:
    def __init__(self, screen):
        self.image = u.load_image("assets/corridor.png", screen.get_size())



        self.screen = screen
        self.conversation = 0
        self.next_room = None
        self.buttons = [  ### list of all rooms accessible from the corridor
            u.Button(0, 100, 140, 50, "Storr Room", self.storr),
            u.Button(200, 100, 140, 50, "VampRoom", self.vamp),
            u.Button(400, 100, 140, 50, "Ghost Room", self.ghost),
            u.Button(600, 100, 140, 50, "Project Room", self.projRoom),
            u.Button(800, 100, 140, 50, "equinox Room", self.equin),
        ]

        self.masks = [
            u.Mask("assets/corridor/room_01.png", self.screen.get_size(), (0, 0), self.doPress, "LAB 2.001"),
            u.Mask("assets/corridor/room_02.png", self.screen.get_size(), (0, 0), self.doPress, "LAB 2.003"),
            u.Mask("assets/corridor/room_03.png", self.screen.get_size(), (0, 0), self.doPress, "Front Desk Office"),
            u.Mask("assets/corridor/room_04.png", self.screen.get_size(), (0, 0), self.doPress, "Classroom 2.015"),
            u.Mask("assets/corridor/room_05.png", self.screen.get_size(), (0, 0), self.doPress, "Classroom 2.021"),
            u.Mask("assets/corridor/room_06.png", self.screen.get_size(), (0, 0), self.doPress, "Teachers Room 4"),
            u.Mask("assets/corridor/room_07.png", self.screen.get_size(), (0, 0), self.doPress, "Classroom 2.031"),
            u.Mask("assets/corridor/room_08.png", self.screen.get_size(), (0, 0), self.doPress, "Stair Exit"),
            u.Mask("assets/corridor/room_09.png", self.screen.get_size(), (0, 0), self.doPress, "Teachers Room 1"),
            u.Mask("assets/corridor/room_10.png", self.screen.get_size(), (0, 0), self.doPress, "Teachers Room 2"),
            u.Mask("assets/corridor/room_11.png", self.screen.get_size(), (0, 0), self.doPress, "Teachers Room 3"),
            u.Mask("assets/corridor/room_12.png", self.screen.get_size(), (0, 0), self.doPress,
                   "Equinox Student Society"),
            u.Mask("assets/corridor/room_13.png", self.screen.get_size(), (0, 0), self.doPress, "Project Room 3"),
            u.Mask("assets/corridor/room_14.png", self.screen.get_size(), (0, 0), self.doPress, "Storage"),
            u.Mask("assets/corridor/room_15.png", self.screen.get_size(), (0, 0), self.doPress, "Classroom 2.035"),
            u.Mask("assets/corridor/room_16.png", self.screen.get_size(), (0, 0), self.doPress, "Project Room 1"),
            u.Mask("assets/corridor/room_17.png", self.screen.get_size(), (0, 0), self.doPress, "Project Room 2"),
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
        for b in self.buttons:
            b.handle_event(event)

    def draw(self):
        self.screen.blit(self.image, (0, 0))
        for m in self.masks:
            m.draw(self.screen)
        for b in self.buttons:
            b.draw2(self.screen)