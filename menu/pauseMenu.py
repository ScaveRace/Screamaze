#assets

#integers

#floats

#strings

#bool
import UI.uiElements as u
import pygame
from Rooms import frontDesk


#  load game
#  new game
#  settings
#  background
#  music

# assets

# integers

# floats

# strings

# bool
import UI.uiElements as u
import pygame
from Rooms import frontDesk

class PauseMenu:
    def __init__(self, screen):
        self.next_room = None
        self.background = u.load_image("assets/startup.png", screen.get_size())
        self.buttons = [
            u.Button(120, 420, 150, 50, "New Game", self.new_game),

        ]


    def new_game(self):
        print("starting new game")




    def handle_event(self, event):
        for b in self.buttons:
            b.handle_event(event)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        for b in self.buttons:
            b.draw2(screen)






