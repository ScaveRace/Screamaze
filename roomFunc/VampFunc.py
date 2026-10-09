import pygame
import UI.uiElements as u
import functions.language as lang

########## constants ##########
TABLE = "VampireRoom"   # name of this room in the language files

texts = {}


def loadTexts():
    global texts
    texts = {int(i): lang.chatMessage(TABLE, i) for i in lang.texts["en"][TABLE]}


def T(textId):
    return texts.get(textId, f"[missing text {textId}]")


ASSET_DIR = "assets/vampire/"
MASK_DIR = ASSET_DIR + "masks/"

# the circle in the drawer: a mask, the picture is also its icon in the inventory
CIRCLE_ICON = "assets/shapes/circle.png"
CIRCLE_WIDTH = 90
CIRCLE_OFFSET = (0, 20)     # moves the circle relative to the centre of the room picture, adjust to fit the drawer

STONE_IMAGE = "assets/stones/red.png"    # adjust to your red stone icon

# item names in the inventory (must match what the other rooms use)
FUSE_ITEM = "Fuse"
CIRCLE_ITEM = "Circle"


class View:
    ROOM = "room"
    CABINET = "cabinet"
    DRAWER = "drawer"
    FUSEBOX_CLOSED = "fusebox_closed"
    FUSEBOX_OPEN = "fusebox_open"


########## room state ##########
images = {}
buttons = {}
masks = {}
next_room = None

player = None
fui = None
view = View.ROOM

# progress: created once and kept when you leave and come back
initialised = False
intro_line = 0
task_done = False
circle_found = False
fuse_inserted = False
stone_collected = False


def resetProgress():
    # call this only for a brand new game
    global initialised, intro_line, task_done, circle_found, fuse_inserted, stone_collected
    intro_line = 0
    task_done = False
    circle_found = False
    fuse_inserted = False
    stone_collected = False
    initialised = True


def getElements(p, f, screen):
    start(p, f, screen)
    current(screen)
    return images, buttons, masks


def start(p, f, screen):
    global images, masks, player, fui, view, next_room
    player = p
    fui = f
    size = screen.get_size()

    # progress is only reset the very first time, not on every entry
    if not initialised:
        resetProgress()

    fallbacks = {
        "bg_closed": (35, 8, 18),
        "bg_open": (120, 100, 60),
        "cabinet": (120, 100, 60),
        "drawer": (120, 100, 60),
        "fusebox_closed": (20, 20, 20),
        "fusebox_open": (20, 20, 20),
        "fusebox_three": (20, 20, 20),
    }
    files = {
        "bg_closed": "Room2015_1_win_clo.png",
        "bg_open": "Room2015_1_win_op.png",
        "cabinet": "vp.cabinet.closed.png",
        "drawer": "cabinet_drawer_open.png",
        "fusebox_closed": "fuse_box.png",
        "fusebox_open": "fuse_box2.png",
        "fusebox_three": "fuse_box2_three_fuses.png",
    }
    images = {
        name: u.load_image(ASSET_DIR + f, size, fallback=fallbacks[name])
        for name, f in files.items()
    }

    # the circle is a small picture, not as big as the room: its position is relative to the room picture (the chat takes the left 300px)
    w, h = pygame.image.load(CIRCLE_ICON).get_size()
    circle = (CIRCLE_WIDTH, round(CIRCLE_WIDTH * h / w))
    cx = (size[0] - u.startX) // 2 + CIRCLE_OFFSET[0]
    cy = size[1] // 2 + CIRCLE_OFFSET[1]

    masks = {
        "circle": u.Mask(CIRCLE_ICON, (circle[0] + u.startX, circle[1]), (cx - circle[0] // 2, cy - circle[1] // 2), collectCircle),
        "vampire": u.Mask(MASK_DIR + "vampire.png", size, (0, 0), talk),
        "cabinet": u.Mask(MASK_DIR + "cabinet.png", size, (0, 0), openCabinet),
        "fusebox": u.Mask(MASK_DIR + "fusebox.png", size, (0, 0), openFuseboxCloseup),
        "stone": u.Mask(MASK_DIR + "red.png", size, (0, 0), collectStone),
        "fusebox_closed": u.Mask(MASK_DIR + "fusebox_closed.png", size, (0, 0), openFuseboxDoor),
        "reset": u.Mask(MASK_DIR + "red_button.png", size, (0, 0), pressReset),
        "drawer": u.Mask(MASK_DIR + "cabinet_drawer.png", size, (0, 0), openDrawer),
    }

    loadTexts()
    view = View.ROOM
    next_room = None


def current(screen=None):
    global buttons
    buttons = {
        View.ROOM: [u.Button(780, 660, 220, 50, "Leave Room", leave)],
        View.FUSEBOX_CLOSED: [u.Button(870, 650, 150, 50, "Close", gotoRoom)],
        View.FUSEBOX_OPEN: [
            u.Button(560, 600, 150, 50, "Insert Fuse", insertFuse),
            u.Button(900, 600, 150, 50, "Close", gotoRoom),
        ],
        View.CABINET: [u.Button(900, 600, 150, 50, "Close", gotoRoom)],
        View.DRAWER: [u.Button(900, 600, 150, 50, "Close", gotoCabinet)],
    }


########## inventory helpers (the only place that touches the player's inventory) ##########
def hasItem(name):
    return player.has_item("Items", name)      # adjust to your player class


def removeItem(name):
    player.remove_item("Items", name)          # adjust to your player class


########## helpers ##########
def say(text):
    fui.chat.say(text)


def currentButtons():
    return buttons[view]


def currentImage():
    if view == View.ROOM:
        return images["bg_open"] if task_done else images["bg_closed"]
    if view == View.CABINET:
        return images["cabinet"]
    if view == View.DRAWER:
        return images["drawer"]
    if view == View.FUSEBOX_CLOSED:
        return images["fusebox_closed"]
    if view == View.FUSEBOX_OPEN:
        return images["fusebox_three"] if fuse_inserted else images["fusebox_open"]


def activeMasks():
    if view == View.ROOM:
        active = []
        if not task_done:
            active.append(masks["vampire"])
        if not circle_found:
            active.append(masks["cabinet"])
        active.append(masks["fusebox"])
        if task_done and not stone_collected:
            active.append(masks["stone"])
        return active
    if view == View.CABINET:
        return [masks["drawer"]]
    if view == View.FUSEBOX_CLOSED:
        return [masks["fusebox_closed"]]
    if view == View.FUSEBOX_OPEN:
        return [masks["reset"]]
    if view == View.DRAWER:
        return [] if circle_found else [masks["circle"]]       # the circle lies in the drawer until you take it
    return []


########## view transitions ##########
def setView(newView, message=None):
    global view
    view = newView
    if message:
        say(message)


def leave():
    global next_room
    next_room = "corridor"


def gotoRoom():
    setView(View.ROOM)


def gotoCabinet():
    setView(View.CABINET)


def openCabinet():
    setView(View.CABINET)


def openDrawer():
    setView(View.DRAWER)


def openFuseboxCloseup():
    setView(View.FUSEBOX_CLOSED)


def openFuseboxDoor():
    setView(View.FUSEBOX_OPEN)


########## vampire ##########
def talk():
    global intro_line
    if intro_line < 3:
        say("Vampire > " + T(1))
        intro_line += 1
    elif not task_done:
        say("Vampire > " + T(4))
    else:
        say("Vampire > " + T(5))


########## circle (found in the drawer, stays in the inventory) ##########
def collectCircle():
    global circle_found
    if circle_found or hasItem(CIRCLE_ITEM):   # never add a second circle
        circle_found = True
        return
    circle_found = True
    player.add_item("Items", CIRCLE_ITEM, CIRCLE_ICON)
    say("You > " + T(6))


########## fuse box ##########
def insertFuse():
    global fuse_inserted
    if fuse_inserted:
        return
    # the fuse is collected in another room, it must be in the inventory first
    if not hasItem(FUSE_ITEM):
        say("You > " + T(7))
        return
    removeItem(FUSE_ITEM)
    fuse_inserted = True
    say("You > " + T(8))


def pressReset():
    global task_done
    if task_done:
        return
    if not fuse_inserted:
        say("You > " + T(9))
        return
    task_done = True
    say("You > " + T(10))
    say("You > " + T(11))


########## stone ##########
def collectStone():
    global stone_collected
    if not task_done or stone_collected:
        return
    stone_collected = True
    player.add_item("Stones", "Red", STONE_IMAGE)
    say("You > " + T(12))