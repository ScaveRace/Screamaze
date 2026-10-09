import pygame
import UI.uiElements as u

SHAPES = ("Circle", "Triangle", "Square")                                   # item names, found in other rooms
OWNERS = {"Circle": "Mina", "Triangle": "Sam", "Square": "Jorn"}            # whose badge it is, see the whiteboard
STONE_PATH = "assets/stones/purple.png"
STONE_WIDTH = 50
STONE_POS = (630, 240)                                                      # centre of the stone in the open box, relative to the room picture
HOLDING_COLOUR = (255, 235, 170)                                            # the frame around the badge in your hand
SHAPE_PATHS = {s: "assets/shapes/" + s.lower() + ".png" for s in SHAPES}    # the pictures of the badges, also their icons in the inventory
BADGE_WIDTH = 80                                                            # the badges you carry, below the box
SLOT_SHAPE_WIDTH = 88                                                       # a badge in its slot

MASK_DIR = "assets/project_room/masks/"                                    # the things in the room you can press: cut out of the room picture

# you'll notice some lambdas below in the code, that is to prevent buttons from firing their functions upon being built.

DB_TABLE = "ProjectRoom"
INTRO = [(None, "intro_1")]
PHONE = [(None, "phone"), ("Voicemail", "voicemail_1"), ("Voicemail", "voicemail_2")]
BOARD = [(None, "board"), ("Whiteboard", "board_mina"), ("Whiteboard", "board_jorn"), ("Whiteboard", "board_sam")]
OPEN = [(None, "open"), (None, "stone")]


def fitWidth(path, width): # the size of a picture at a given width
    w, h = pygame.image.load(path).get_size()
    return (width, round(width * h / w))


def spriteMask(path, width, centre, action): # a small picture, not as big as the room: the centre is relative to the room picture
    w, h = fitWidth(path, width)
    return u.Mask(path, (w + u.startX, h), (centre[0] - w // 2, centre[1] - h // 2), action)


def loadImages(screen):
    image = u.load_image("assets/project_room.png", screen.get_size(), (22, 20, 26))
    boxImage = u.load_alpha_image("assets/", (420, 300), (40, 32, 26))
    shapes = {s: u.load_alpha_image(SHAPE_PATHS[s], fitWidth(SHAPE_PATHS[s], SLOT_SHAPE_WIDTH)) for s in SHAPES}
    return image, boxImage, shapes


def buildMasks(room): # the things in the room are masks, so are the badges you carry and the stone: it lies in the box once it is open
    size = room.screen.get_size()
    return {
        "bookshelf": u.Mask(MASK_DIR + "bookshelf.png", size, (0, 0), lambda: say(room, None, "binder"), "Bookshelf"),
        "board": u.Mask(MASK_DIR + "whiteboard.png", size, (0, 0), lambda: sayAll(room, BOARD), "Whiteboard"),
        "phone": u.Mask(MASK_DIR + "beanbags.png", size, (0, 0), lambda: sayAll(room, PHONE), "Beanbags"),
        "box": u.Mask(MASK_DIR + "locked_box.png", size, (0, 0), lambda: openBox(room)),   # no label, it is too narrow for text
        "stone": spriteMask(STONE_PATH, STONE_WIDTH, STONE_POS, lambda: takeStone(room)),
        # a badge only shows up while the player carries it, in a row below the box
        "badge": {s: spriteMask(SHAPE_PATHS[s], BADGE_WIDTH, (470 + 110 * i, 525), lambda s=s: pickUp(room, s))
                  for i, s in enumerate(SHAPES)},
    }


def buildButtons(room):
    x = u.startX
    return {
        "leave": u.Button(x + 540, 650, 200, 45, "Leave the room", lambda: leave(room)),
        "back": u.Button(x + 60, 650, 160, 45, "Back", lambda: toRoom(room)),
        # one slot per shape, it shows the name of its owner until the badge is in
        "slot": {s: u.Button(x + 450 + 130 * i, 300, 100, 100, OWNERS[s], lambda s=s: tryPlace(room, s))
                 for i, s in enumerate(SHAPES)},
    }


def progress(room): # just points to specific room project from completion
    return room.player.getCompletion("ProjectRoom")


def has(room, event): # easy check to see if something already happened.
    return event in progress(room)["all"]


def add(room, event):
    room.player.addCompletion("ProjectRoom", event, "")


def placed(room, shape):
    return has(room, "proj.placed." + shape)


def carried(room, shape): # the player has the badge and it is not in the box yet
    return room.player.has_item("Items", shape) and not placed(room, shape)


def say(room, who, messageID):
    text = room.fui.db.chatMessage(DB_TABLE, messageID)
    room.fui.chat.say(f"{who} > {text}" if who else text)


def sayAll(room, lines):
    for who, messageID in lines:
        say(room, who, messageID)


def intro(room):
    if has(room, "proj.stone"):
        say(room, None, "intro_done")
    elif not has(room, "proj.visited"):
        add(room, "proj.visited")
        sayAll(room, INTRO)


def getElements(room): # basically the logic
    if room.view == "room":
        return [room.btn["leave"]], [room.allMasks[name] for name in ("bookshelf", "board", "phone", "box")]

    buttons = [room.btn["back"]]
    masks = [room.allMasks["stone"]] if has(room, "proj.open") and not has(room, "proj.stone") else []
    for shape in SHAPES:
        if not placed(room, shape):
            buttons.append(room.btn["slot"][shape])                 # a filled slot is only a picture, see drawScene
        if carried(room, shape):
            masks.append(room.allMasks["badge"][shape])
    return buttons, masks


def toRoom(room):
    room.view = "room"
    room.holding = None


def leave(room):
    room.next_room = "corridor"


def openBox(room):
    room.view = "box"
    if has(room, "proj.stone"):
        say(room, None, "box_empty")
        return
    if has(room, "proj.open"): # open, the stone is still waiting in it
        say(room, None, "stone")
        return
    say(room, None, "box")
    if not any(carried(room, s) for s in SHAPES):
        say(room, None, "box_nobadges")


def pickUp(room, shape):
    room.holding = shape
    say(room, None, "pickup")


def tryPlace(room, shape):
    if placed(room, shape):
        return
    if room.holding is None:
        say(room, None, "pick_first")
    elif room.holding == shape:
        add(room, "proj.placed." + shape)
        room.holding = None
        say(room, None, "place")
        if all(placed(room, s) for s in SHAPES):
            complete(room)
    else:
        room.holding = None
        say(room, None, "wrong")


def complete(room): # all badges are in: they are used up and the box opens, the stone is in it
    for shape in SHAPES:
        room.player.remove_item("Items", shape)
    add(room, "proj.open")
    sayAll(room, OPEN)


def takeStone(room): # pressing the stone in the open box
    room.player.add_item("Stones", "Purple", STONE_PATH)
    add(room, "proj.stone")                                 # after add_item, so a failed pickup doesn't count as taken
    say(room, None, "stone_taken")


def drawScene(room):
    room.screen.blit(room.image, (u.startX, 0))
    if room.view == "room":
        room.screen.blit(room.font.render("PROJECT ROOM 3", True, (230, 225, 235)), (u.startX + 60, 655))   # in the black below the room, the bookshelf mask is in the top corner
    else:
        room.screen.blit(room.boxImage, (u.startX + 420, 180))
        pygame.draw.rect(room.screen, (170, 150, 120), pygame.Rect(u.startX + 420, 180, 420, 300), 1)
        for shape in SHAPES:
            if placed(room, shape): # the badge sits in its slot, the name of its owner below
                slot = room.btn["slot"][shape].rect
                picture = room.shapes[shape]
                room.screen.blit(picture, picture.get_rect(center=slot.center))
                name = room.smallFont.render(OWNERS[shape], True, (210, 200, 160))
                room.screen.blit(name, name.get_rect(midtop=(slot.centerx, slot.bottom + 8)))
        if room.holding:
            badge = room.allMasks["badge"][room.holding]
            pygame.draw.rect(room.screen, HOLDING_COLOUR, pygame.Rect(badge.imageX, badge.imageY, badge.rect.w, badge.rect.h).inflate(12, 12), 2)
