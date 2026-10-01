##### import alllllll the rooms ######
import pygame
import menu.startupMenu as s
import Rooms.frontDesk as fd
import Rooms.ghostRoom as gr
import Rooms.storrageRoom as st
import Rooms.vampireRoom as vp
import Rooms.corridor as corri
import Rooms.projectRoom as pR
import Rooms.equinoxRoom as eq

import player as p
import functions.savingFunc as load
from functions.settingsFunc import settings as sett
import UI.frontUI as fui
pygame.init()
pygame.mixer.init()
##########  setting the display and mode   ################
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("THUAS's Screamazing")
#########  clock to measure time   ################
clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)

######## game loop boolean  ##########
running = True

######## dictionary of rooms  ########
ROOMS = {
    "startup": s.StartupMenu,
    "frontD": fd.FrontDesk,
    "corridor": corri.Corridor,
    "ghostR" : gr.GhostRoom,
    "storrR" : st.StorrageRoom,
    "vampR" : vp.VampireRoom,
    "equinR" : eq.EquinoxRoom,
    "projRoom" : pR.ProjectRoom
    #"lab" : lab.Lab2001
}

if not load.is_json_empty("data/gameSettings.json"):
    load.load(sett,"data/gameSettings.json")
    print(sett.getMusicVolume())


player = p.Player()
frontui = fui.FrontUI(player,screen)
room = s.StartupMenu(screen,player)
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

        else:
            frontui.handleEvenet(event)
            room.handle_event(event)



    if room.next_room is not None:
        name = room.next_room
        if name not in ROOMS:
            raise KeyError(f"No room named {name!r}. Known: {sorted(ROOMS)}")
        if current != "startup" and current != "frontD":
            room = ROOMS[name](screen,player)
        else:
            room = ROOMS[name](screen, player,fui)
        current = name
        player.location = name


    room.draw()
    if current != "startup" and current != "frontD":
        if not frontui.pause.paused:
            # clock only advances while unpaused
            ms_buffer += dt
            while ms_buffer >= 1000:
                player.add_time(1)
                ms_buffer -= 1000
        frontui.draw()
    pygame.display.flip()


pygame.quit()       # quits pygame