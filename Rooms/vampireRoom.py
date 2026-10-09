import pygame
import roomFunc.VampFunc as vF

pygame.init()
pygame.mixer.init()


class VampireRoom:
    def __init__(self, screen, player, fui):
        self.screen = screen
        self.player = player
        self.fui = fui
        self.next_room = None

        # what the player already did here is saved in player.completion, so it is still done after leaving or loading
        done = player.getCompletion("VampRoom")["all"]
        line = sum(1 for event in done if event.startswith("vamp.talk_"))
        self.states = {
            "line": line,
            "task_started": line == 3,
            "task_done": "vamp.task_done" in done,
            "inventory": ["fuse"] if "vamp.fuse_found" in done and "vamp.fuse_inserted" not in done else [],
            "fuse_found": "vamp.fuse_found" in done,
            "fuse_inserted": "vamp.fuse_inserted" in done,
            "stone_collected": "vamp.stone" in done,
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