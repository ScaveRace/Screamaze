import roomFunc.startupFunc as sF


class StartupMenu:
    def __init__(self, screen,player):
        self.screen = screen
        self.player = player
        self.next_room = None
        self.image = []
        self.buttons = []
        self.getElements()

    def getElements(self):
        tmp = sF.getElements(self.player,self.screen)
        self.image = tmp[0]
        self.buttons = tmp[1]

    def handle_event(self, event):
        for b in self.buttons:
            b.handle_event(event)
        self.next_room = sF.next_room
        sF.next_room = None

    def draw(self):
        for i in self.image:
            self.screen.blit(i, (0, 0))

        for b in self.buttons:
            b.draw2(self.screen)
