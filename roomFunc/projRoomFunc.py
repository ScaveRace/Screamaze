import pygame
import UI.uiElements as u

SHAPES = ("Circle", "Triangle", "Square")                                   # item names, found in other rooms
OWNERS = {"Circle": "Mina", "Triangle": "Sam", "Square": "Jorn"}            # whose badge it is, see the whiteboard
STONE_PATH = "assets/stones/purple.png"
STONE_WIDTH = 50
STONE_POS = (630, 240)                                                      # centre of the stone in the open box, relative to the room picture
HOLDING_COLOUR = (110, 95, 60)

# the chat takes the left 300px, so the right-hand buttons sit 60px from the screen edge instead of a plain +300
RIGHT_X = 1480 - 60 - 230

# you'll notice some lambdas below in the code, that is to prevent buttons from firing their functions upon being built.

DB_TABLE = "ProjectRoom"
INTRO = [(None, "intro_1")]
PHONE = [(None, "phone"), ("Voicemail", "voicemail_1"), ("Voicemail", "voicemail_2")]
BOARD = [(None, "board"), ("Whiteboard", "board_mina"), ("Whiteboard", "board_jorn"), ("Whiteboard", "board_sam")]
OPEN = [(None, "open"), (None, "stone")]


def loadImages(screen):
    image = u.load_image("assets/project_room.png", screen.get_size(), (22, 20, 26))
    boxImage = u.load_alpha_image("assets/", (420, 300), (40, 32, 26))
    return image, boxImage


def buildMasks(room): # the stone is a mask, it lies in the box once it is open
    w, h = pygame.image.load(STONE_PATH).get_size()
    size = (STONE_WIDTH, round(STONE_WIDTH * h / w))
    return u.Mask(STONE_PATH, (size[0] + u.startX, size[1]), (STONE_POS[0] - size[0] // 2, STONE_POS[1] - size[1] // 2),
                  lambda: takeStone(room))


def buildButtons(room):
    x = u.startX
    return {
        "bookshelf": u.Button(x + 60, 120, 230, 60, "Bookshelf", lambda: say(room, None, "binder")),
        "board": u.Button(RIGHT_X, 120, 230, 60, "Whiteboard", lambda: sayAll(room, BOARD)),
        "phone": u.Button(x + 60, 560, 230, 60, "Beanbags", lambda: sayAll(room, PHONE)),
        "box": u.Button(RIGHT_X, 560, 230, 60, "Locked box", lambda: openBox(room)),
        "leave": u.Button(x + 540, 650, 200, 45, "Leave the room", lambda: leave(room)),
        "back": u.Button(x + 60, 650, 160, 45, "Back", lambda: toRoom(room)),
        # one slot and one badge button per shape, the badge only shows up while the player carries it
        "slot": {s: u.Button(x + 450 + 130 * i, 300, 100, 100, OWNERS[s], lambda s=s: tryPlace(room, s))
                 for i, s in enumerate(SHAPES)},
        "badge": {s: u.Button(x + 420 + 110 * i, 500, 100, 50, s, lambda s=s: pickUp(room, s))
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
        return [room.btn[name] for name in ("bookshelf", "board", "phone", "box", "leave")], []

    buttons = [room.btn["back"]]
    masks = [room.stoneMask] if has(room, "proj.open") and not has(room, "proj.stone") else []
    for shape in SHAPES:
        slot = room.btn["slot"][shape]
        slot.label = shape if placed(room, shape) else OWNERS[shape]    # the name turns into the badge
        buttons.append(slot)

        if carried(room, shape):
            badge = room.btn["badge"][shape]
            badge.bgCol = HOLDING_COLOUR if room.holding == shape else (0, 0, 0)
            buttons.append(badge)
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
        room.screen.blit(room.font.render("PROJECT ROOM 3", True, (230, 225, 235)), (u.startX + 60, 50))
    else:
        room.screen.blit(room.boxImage, (u.startX + 420, 180))
        pygame.draw.rect(room.screen, (170, 150, 120), pygame.Rect(u.startX + 420, 180, 420, 300), 1)
