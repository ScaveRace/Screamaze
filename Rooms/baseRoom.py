import pygame


REGISTRY = {}


def register(cls):
    if cls.key:
        REGISTRY[cls.key] = cls
    return cls


class BaseRoom:

    key = ""
    show_ui = True #define if chat and other elements are shown
    paranormal = True   #paranormal sounds turned on

    def __init__(self,screen,player,fui = None):
        self.screen = screen
        self.player = player
        self.fui = fui
        self.next_room = None

    def goTo(self,room):
        self.next_room = room

    def on_enter(self):pass
    def handle_event(self,event):pass
    def draw(self):pass
