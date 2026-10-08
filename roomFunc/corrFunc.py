import math
import pygame
import UI.uiElements as u

# size of the full corridor picture, the door positions below are measured in it
PICTURE_SIZE = (1672, 941)


def getElements(player,fui,screen,goTo):
    if len(player.inventory["Stones"]) == 5:
        images = end(screen)
    else:
        images = start(fui,screen,player)
    masks = current(screen,goTo)
    return images,masks

def current(screen,goTo):
    doPress = door(goTo,"vampR")
    storr = door(goTo,"storrR")
    vamp = door(goTo,"vampR")
    ghost = door(goTo,"ghostR")
    projRoom = door(goTo,"projRoom")
    equin = door(goTo,"equinR")
    return [
        makeMask(screen, "assets/corridor/room_01.png", (105, 144), ghost, "LAB 2.001"),
        makeMask(screen, "assets/corridor/room_02.png", (271, 144), doPress, "LAB 2.003"),
        makeMask(screen, "assets/corridor/room_03.png", (736, 144), doPress, "Front Desk Office"),
        makeMask(screen, "assets/corridor/room_04.png", (872, 143), vamp, "Classroom 2.015"),
        makeMask(screen, "assets/corridor/room_05.png", (1028, 143), doPress, "Classroom 2.021"),
        makeMask(screen, "assets/corridor/room_06.png", (1212, 143), doPress, "Teachers Room 4"),
        makeMask(screen, "assets/corridor/room_07.png", (1397, 143), doPress, "Classroom 2.031"),
        makeMask(screen, "assets/corridor/room_08.png", (1213, 211), doPress, "Stair Exit"),
        makeMask(screen, "assets/corridor/room_09.png", (765, 383), doPress, "Teachers Room 1"),
        makeMask(screen, "assets/corridor/room_10.png", (872, 384), doPress, "Teachers Room 2"),
        makeMask(screen, "assets/corridor/room_11.png", (960, 383), doPress, "Teachers Room 3"),
        makeMask(screen, "assets/corridor/room_12.png", (1051, 383), equin, "Equinox Student Society"),
        makeMask(screen, "assets/corridor/room_13.png", (1141, 383), projRoom, "Project Room 3"),
        makeMask(screen, "assets/corridor/room_14.png", (1224, 383), storr, "Storage"),
        makeMask(screen, "assets/corridor/room_15.png", (1397, 340), doPress, "Classroom 2.035"),
        makeMask(screen, "assets/corridor/room_16.png", (455, 438), projRoom, "Project Room 1"),
        makeMask(screen, "assets/corridor/room_17.png", (551, 438), projRoom, "Project Room 2"),
    ]


def start(fui,screen,player):
    if player.getCompletion("Corridor")["current"] == "corr.start":
        player.addCompletion("Corridor","corr.going","")
        fui.sendMessage("Thuas: ","FrontDesk","msg_1")
    return [u.load_image("assets/corridor_closed.png", screen.get_size())]


def end(screen):
    return [u.load_image("assets/corridor.png", screen.get_size())]


# makes a door cutout: pos is where the cutout sits in the full corridor picture,
# it gets scaled to the room the same way the corridor picture is
def makeMask(screen,path,pos,action,label):
    roomW = screen.get_size()[0] - u.startX
    roomH = screen.get_size()[1]
    scaleX = roomW / PICTURE_SIZE[0]
    scaleY = roomH / PICTURE_SIZE[1]
    w, h = pygame.image.load(path).get_size()
    left, top = math.ceil(pos[0] * scaleX), math.ceil(pos[1] * scaleY)
    right, bottom = math.ceil((pos[0] + w) * scaleX), math.ceil((pos[1] + h) * scaleY)
    return u.Mask(path, (right - left + u.startX, bottom - top), (left, top), action, label)


# makes the action for a door: pressing it sends the player to that room
def door(goTo,room):
    return lambda: goTo(room)
