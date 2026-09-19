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

########## game loop ##########
room = s.StartupMenu(screen)   ## initial screen
while running:

    for event in pygame.event.get():   ### handle user events
        if event.type == pygame.QUIT:
            running = False
        else:
            room.handle_event(event)
    if room.next_room is not None:    ### handle room and function within the class
        name = room.next_room
        if name not in ROOMS:       ###  check for lack of a room (debugging)
            raise KeyError(f"No room named {name!r}. Known: {sorted(ROOMS)}")
        room = ROOMS[name](screen)

    room.draw()
    #ui.draw_base_ui(screen, font)
    pygame.display.flip()


pygame.quit()       # quits pygame