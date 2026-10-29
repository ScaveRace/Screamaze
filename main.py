##### import alllllll the rooms ######
import pygame
import Rooms.baseRoom as bR
from Rooms import load_all

import player as p
import functions.savingFunc as load
from functions.settingsFunc import settings as sett
from functions.paranormal import paranormal
import UI.frontUI as fui
pygame.init()
pygame.mixer.init()
##########  setting the display and mode   ################
SCREEN_WIDTH = 1480
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption("THUAS's Screamazing")
#########  clock to measure time   ################
clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)

######## game loop boolean  ##########
running = True
load_all()

if not load.is_json_empty("data/gameSettings.json"):
    load.load(sett,"data/gameSettings.json")
    print(sett.getMusicVolume())


player = p.Player()
frontui = fui.FrontUI(player,screen)
room = bR.REGISTRY["startup"](screen,player,frontui)
room.on_enter()
current = "startup"

ms_buffer = 0          # leftover milliseconds not yet worth a whole second

########## game loop ##########
 ## initial screen
while running:
    dt = clock.tick(60)                     # caps at 60 fps, returns ms since last call
    #show_pause = current not in ("startup", "frontD")      # no pause button on the title screen

    for event in pygame.event.get():   ### handle user events
        if event.type == pygame.QUIT:
            running = False
        elif not (room.show_ui and frontui.handleEvenet(event)):
            room.handle_event(event)

    if room.next_room is not None:
        name = room.next_room
        if name not in bR.REGISTRY:
            raise KeyError(f"No room named {name!r}. Known: {sorted(bR.REGISTRY)}")
        room = bR.REGISTRY[name](screen,player,frontui)
        room.on_enter()
        current = name
        player.location = name
    paranormal.setActive(room.paranormal)
    paranormal.update()

    if current == "startup":
        frontui.reset()
    room.draw()
    if room.show_ui:
        if not frontui.pause.paused:
            # clock only advances while unpaused
            ms_buffer += dt
            while ms_buffer >= 1000:
                player.add_time(1)
                ms_buffer -= 1000
        frontui.draw()
    pygame.display.flip()


pygame.quit()       # quits pygame