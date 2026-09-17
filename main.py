import UI.uiElements
import json
import pygame
import UI.frontUI as ui
#import Rooms.corridor as cori
import menu.startupMenu as s
import Rooms.frontDesk as fd
import Rooms.ghostRoom as gr
import Rooms.storrageRoom as st
import Rooms.vampireRoom as vp
import Rooms.corridor as corri
import Rooms.lab2001 as lab
import Rooms.projectRoom as pR
import Rooms.equinoxRoom as eq
import Rooms. lab2001 as lab
#from data.saver import savedata

#save = savedata()


pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("THUAS's Screamazing")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)

isMusician = False
running = True

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
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            room.handle_event(event)
    if room.next_room is not None:
        name = room.next_room
        if name not in ROOMS:
            raise KeyError(f"No room named {name!r}. Known: {sorted(ROOMS)}")
        room = ROOMS[name](screen)

    room.draw()
    #ui.draw_base_ui(screen, font)
    pygame.display.flip()

    #dt2 = clock.tick(60) / 1000
    #save.time += dt2


pygame.quit()