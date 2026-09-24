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

#from player import player
#from UI.frontUI import PauseMenu


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

room = s.StartupMenu(screen)
current = "startup"

pause = PauseMenu(screen)
ms_buffer = 0          # leftover milliseconds not yet worth a whole second

########## game loop ##########
room = s.StartupMenu(screen)   ## initial screen
while running:
    dt = clock.tick(60)                     # caps at 60 fps, returns ms since last call
    show_pause = current not in ("startup", "frontD")      # no pause button on the title screen

    for event in pygame.event.get():   ### handle user events
        if event.type == pygame.QUIT:
            running = False
        elif show_pause and pause.handle_event(event):
            continue                        # overlay consumed it, room must not see it
        else:
            room.handle_event(event)
    if room.next_room is not None:    ### handle room and function within the class
        name = room.next_room
        if name not in ROOMS:       ###  check for lack of a room (debugging)
            raise KeyError(f"No room named {name!r}. Known: {sorted(ROOMS)}")
        room = ROOMS[name](screen)

    if show_pause and not pause.paused:
        # clock only advances while unpaused
        ms_buffer += dt
        while ms_buffer >= 1000:
            player.add_time(1)
            ms_buffer -= 1000
    if not pause.paused:
        if room.next_room is not None:
            name = room.next_room
            if name not in ROOMS:
                raise KeyError(f"No room named {name!r}. Known: {sorted(ROOMS)}")
            room = ROOMS[name](screen)
            current = name
            player.position = name
            if name == "startup":
                pause.paused = False

    room.draw()
    if show_pause:
        pause.draw()                        # last, so it sits on top of the room
    pygame.display.flip()


pygame.quit()       # quits pygame