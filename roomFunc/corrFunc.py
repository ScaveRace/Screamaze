import UI.uiElements as u


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
        u.Mask("assets/corridor/room_01.png", screen.get_size(), (0, 0), ghost, "LAB 2.001"),
        u.Mask("assets/corridor/room_02.png", screen.get_size(), (0, 0), doPress, "LAB 2.003"),
        u.Mask("assets/corridor/room_03.png", screen.get_size(), (0, 0), doPress, "Front Desk Office"),
        u.Mask("assets/corridor/room_04.png", screen.get_size(), (0, 0), vamp, "Classroom 2.015"),
        u.Mask("assets/corridor/room_05.png", screen.get_size(), (0, 0), doPress, "Classroom 2.021"),
        u.Mask("assets/corridor/room_06.png", screen.get_size(), (0, 0), doPress, "Teachers Room 4"),
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
    if player.getCompletion("Corridor")["current"] == "corr.start":
        player.addCompletion("Corridor","corr.going","")
        fui.sendMessage("Thuas: ","FrontDesk","msg_1")
    return [u.load_image("assets/corridor_closed.png", screen.get_size())]


def end(screen):
    return [u.load_image("assets/corridor.png", screen.get_size())]


# makes the action for a door: pressing it sends the player to that room
def door(goTo,room):
    return lambda: goTo(room)
