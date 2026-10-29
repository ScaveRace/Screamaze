# Rooms/ghostRoom.py

import roomFunc.ghoRoomFunc as gF
from Rooms.baseRoom import BaseRoom, register


@register
class GhostRoom(BaseRoom):
    key = "ghostR"


    def __init__(self, screen, player, fui):
        super().__init__(screen, player, fui)
        self.images, self.masks,  self.buttons = [], [], []
        self.state = None

    def build(self):
        self.images, self.masks, self.buttons = gF.getElements(self.player, self.fui, self.screen)
        self.state = gF.state()

    def on_enter(self):
        gF.reset()
        self.build()
        gF.describe()


    def handle_event(self, event):
        for e in self.masks + self.buttons:
            e.handle_event(event)
        gF.keyboard(event)
        if gF.next_room is not None:
            self.next_room, gF.next_room = gF.next_room, None
        if gF.state() != self.state:      # view or saved progress changed
            self.build()

    def draw(self):
        for i in self.images:
            self.screen.blit(i, (300, 0))
        gF.drawExtras(self.screen)
        for m in self.masks:
            m.draw(self.screen)
        for b in self.buttons:
            b.draw2(self.screen)