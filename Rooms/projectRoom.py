import pygame
import roomFunc.projRoomFunc as pF

fontBig = pygame.font.Font(None, 40)


########## project room class ##########
class ProjectRoom:
    # class variable, so the progress stays when you leave and come back
    memory = {
        "visited": False,        # the intro line was said
        "stoneTaken": False,     # the box was opened and the purple stone given
        "placed": {"Circle": False, "Triangle": False, "Square": False},   # badges already in the box
    }

    def __init__(self, screen, p, fui):
        self.screen = screen
        self.next_room = None
        self.image = pF.getElements(p, fui, screen, ProjectRoom.memory)

    ########## only the buttons of the current view get clicks ##########
    def handle_event(self, event):
        for b in pF.currentButtons():
            b.handle_event(event)
        self.next_room = pF.next_room
        pF.next_room = None

    ########## draw the current project room view ##########
    def draw(self):
        self.screen.blit(self.image, (pF.X, 0))

        if pF.view == "room":
            self.screen.blit(fontBig.render("PROJECT ROOM 1", True, (230, 225, 235)), (pF.X + 60, 50))
        else:
            self.screen.blit(pF.boxImage, (pF.X + 420, 180))
            pygame.draw.rect(self.screen, (170, 150, 120), pygame.Rect(pF.X + 420, 180, 420, 300), 1)

        for b in pF.currentButtons():
            b.draw2(self.screen)
