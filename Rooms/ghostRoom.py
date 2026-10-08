import pygame
import UI.uiElements as u
from player import Player
import UI.frontUI as Fui

pygame.init()
pygame.mixer.init()

# rooms/ghostRoom.py
import roomFunc.ghoRoomFunc as gF


class GhostRoom:
    def __init__(self, screen, player, fui):
        self.screen = screen
        self.player = player
        self.fui = fui
        self.next_room = None
        self.images = []
        self.masks = []
        self.buttons = []
        gF.reset_view()
        self.getElements()

    def getElements(self):
        self.images, self.masks, self.buttons = gF.getElements(self.player, self.fui, self.screen)

    def on_enter(self):
        gF.reset_view()
        gF.on_enter(self.player, self.fui)
        self.getElements()

    def handle_event(self, event):
        for m in self.masks:
            m.handle_event(event)
        for b in self.buttons:
            b.handle_event(event)
        gF.keyboard(event, self.player, self.fui)

        if gF.next_room is not None:
            self.next_room = gF.next_room
            gF.next_room = None
        if gF.needs_refresh():
            self.getElements()

    def draw(self):
        for i in self.images:
            self.screen.blit(i, (300, 0))
        gF.drawExtras(self.screen, self.player)
        for m in self.masks:
            m.draw(self.screen)
        for b in self.buttons:
            b.draw2(self.screen)