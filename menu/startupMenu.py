import roomFunc.startupFunc as sF
import UI.pauseMenu as pause
import UI.leaderboard as leaderboard
from Rooms.baseRoom import BaseRoom, register

@register
class StartupMenu(BaseRoom):
    key = "startup"
    show_ui = False

    def __init__(self, screen, player, fui=None):
        super().__init__(screen, player, fui)
        self.paranormal = False
        self.image = []
        self.buttons = []
        self.pause = pause.PauseMenu(screen, player, False)
        self.leaderboard = leaderboard.Leaderboard(screen)
        self.getElements()

    def getElements(self):
        tmp = sF.getElements(self.player,self.screen,self.goTo,self.pause.toggle,self.leaderboard.toggle)
        self.image = tmp[0]
        self.buttons = tmp[1]

    def handle_event(self, event):
        if self.pause.paused:
            self.pause.handle_event(event)
        elif self.leaderboard.handle_event(event):
            return
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
        self.leaderboard.draw()
