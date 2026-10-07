import pygame
import UI.uiElements as u

images = []
masks = []
next_room = None

def getElements(player,fui,screen):
    if len(player.inventory["Stones"]) == 5:
            end(screen)
    else:
        if player.getCompletion("Corridor")["current"] == "corr.start":
            start(fui,screen,player)
        current(screen)
    return images,masks

def current(screen):
    global masks
    masks = [
        u.Mask("assets/corridor/room_01.png", screen.get_size(), (0, 0), ghost, "LAB 2.001"),
        u.Mask("assets/corridor/room_02.png", screen.get_size(), (0, 0), doPress, "LAB 2.003"),
        u.Mask("assets/corridor/room_03.png", screen.get_size(), (0, 0), doPress, "Front Desk Office"),
        u.Mask("assets/corridor/room_04.png", screen.get_size(), (0, 0), vamp, "Classroom 2.015"),
        u.Mask("assets/corridor/room_05.png", screen.get_size(), (0, 0), doPress, "Classroom 2.021"),
        u.Mask("assets/corridor/room_06.png", screen.get_size(), (0, 0), teachR, "Teachers Room 4"),
        u.Mask("assets/corridor/room_07.png", screen.get_size(), (0, 0), doPress, "Classroom 2.031"),
        u.Mask("assets/corridor/room_08.png", screen.get_size(), (0, 0), doPress, "Stair Exit"),
        u.Mask("assets/corridor/room_09.png", screen.get_size(), (0, 0), doPress, "Teachers Room 1"),
        u.Mask("assets/corridor/room_10.png", screen.get_size(), (0, 0), doPress, "Teachers Room 2"),
        u.Mask("assets/corridor/room_11.png", screen.get_size(), (0, 0), doPress, "Teachers Room 3"),
        u.Mask("assets/corridor/room_12.png", screen.get_size(), (0, 0), equin,
               "Equinox Student Society"),
        u.Mask("assets/corridor/room_13.png", screen.get_size(), (0, 0), projRoom, "Project Room 3"),
        u.Mask("assets/corridor/room_14.png", screen.get_size(), (0, 0), storr, "Storage"),
        u.Mask("assets/corridor/room_15.png", screen.get_size(), (0, 0), doPress, "Classroom 2.035"),
        u.Mask("assets/corridor/room_16.png", screen.get_size(), (0, 0), projRoom, "Project Room 1"),
        u.Mask("assets/corridor/room_17.png", screen.get_size(), (0, 0), projRoom, "Project Room 2"),
    ]


def start(fui,screen,player):
    global images
    player.addCompletion("Corridor","corr.going","")
    images =[ u.load_image("assets/corridor_closed.png", screen.get_size())]
    fui.sendMessage("Thuas: ","FrontDesk","msg_1")


def end(screen):
    global images
    images = [u.load_image("assets/corridor.png", screen.get_size())]



def doPress():
    global next_room
    next_room = "vampR"


def storr():
    global next_room
    next_room = "storrR"


def vamp():
    global next_room
    next_room = "vampR"


def ghost():
    global next_room
    next_room = "ghostR"


def lab():
    global next_room
    next_room = "frontD"


def projRoom():
    global next_room
    next_room = "projRoom"


def equin():
    global next_room
    next_room = "equinR"


def teachR():
    global next_room
    next_room = "teacherR"




