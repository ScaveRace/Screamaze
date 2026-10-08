import pygame
import roomFunc.vampireRoomFunc as vF

pygame.init()
pygame.mixer.init()


class VampireRoom:
    def __init__(self, screen, player, fui):
        self.screen = screen
        self.player = player
        self.fui = fui
        self.next_room = None

        self.states = {
            "line": 0,
            "task_started": False,
            "task_done": False,
            "inventory": [],
            "fuse_found": False,
            "fuse_inserted": False,
            "stone_collected": False,
            "state": "room"
        }

        self.titleFont = pygame.font.Font(None, 40)

        self.images = vF.loadImages(screen)
        self.masks = vF.buildMasks(self)
        self.buttons = vF.buildButtons(self)

    def handle_event(self, event):
        vF.handle_event(self, event)

    def draw(self):
        vF.draw(self)