import roomFunc.startupFunc as sF
import UI.pauseMenu as pause


class StartupMenu:
    def __init__(self, screen,player):
        self.screen = screen
        self.player = player
        self.next_room = None
        self.image = []
        self.buttons = []
        self.pause = pause.PauseMenu(screen, player, False)
        self.getElements()

    def getElements(self):
        tmp = sF.getElements(self.player,self.screen,self.goTo,self.pause.toggle)
        self.image = tmp[0]
        self.buttons = tmp[1]

    def goTo(self, room):
        self.next_room = room

    def handle_event(self, event):
        if self.pause.paused:
            self.pause.handle_event(event)
        else:
            for b in self.buttons:
                b.handle_event(event)

    def draw(self):
        for i in self.image:
            self.screen.blit(i, (0, 0))

        for b in self.buttons:
            b.draw2(self.screen)

        if self.pause.paused:
            self.pause.draw()
