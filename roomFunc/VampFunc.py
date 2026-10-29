from __future__ import annotations
from typing import TYPE_CHECKING
import UI.uiElements as u
import functions.language as lang
if TYPE_CHECKING:
    import pygame
    from UI.frontUI import FrontUI
    from player import Player

########## constants ##########
TABLE = "VampireRoom"   #name in language file
texts = {}

def load_texts():
    global texts
    texts = {int(i): lang.chatMessage(TABLE, i) for i in lang.texts["en"][TABLE]}

def text_for(text_id: int) -> str:
    return texts.get(text_id, f"[missing text {text_id}]")

ASSET_DIR = "assets/vampire/"
MASK_DIR = ASSET_DIR + "masks/"

# the circle in the drawer: its picture is also the inventory icon
CIRCLE_ICON = "assets/shapes/circle.png"
STONE_IMAGE = "assets/stones/red.png"

# item names in the inventory
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
player: Player | None = None
fui: FrontUI | None = None
view = View.ROOM
intro_line = 0
task_done = False
circle_found = False
fuse_inserted = False
stone_collected = False

def getElements(p: Player, f: FrontUI, screen: pygame.Surface):
    start(p, f, screen)
    current()
    return images, buttons, masks

def start(p: Player, f: FrontUI, screen: pygame.Surface):
    global images, masks, player, fui, view, next_room
    global intro_line, task_done, circle_found, fuse_inserted, stone_collected
    player = p
    fui = f
    size = screen.get_size()
    # Rebuild the room state from the player's save data whenever the room opens.
    completed = set(p.getCompletion("VampRoom")["all"])
    intro_line = max(
        (line for line in range(1, 4) if f"vamp.talk_{line}" in completed),
        default=0,)
    task_done = "vamp.task_done" in completed
    circle_found = (
        "vamp.circle_found" in completed
        or p.has_item("Items", CIRCLE_ITEM))
    fuse_inserted = "vamp.fuse_inserted" in completed
    stone_collected = (
        "vamp.stone" in completed
        or p.has_item("Stones", "Red"))

    fallbacks = {
        "bg_closed": (35, 8, 18),
        "bg_open": (120, 100, 60),
        "cabinet": (120, 100, 60),
        "drawer": (120, 100, 60),
        "fusebox_closed": (20, 20, 20),
        "fusebox_open": (20, 20, 20),
        "fusebox_three": (20, 20, 20),}
    files = {
        "bg_closed": "Room2015_1_win_clo.png",
        "bg_open": "Room2015_1_win_op.png",
        "cabinet": "vp.cabinet.closed.png",
        "drawer": "cabinet_drawer_open.png",
        "fusebox_closed": "fuse_box.png",
        "fusebox_open": "fuse_box2.png",
        "fusebox_three": "fuse_box2_three_fuses.png",}
    images = {
        name: u.load_image(ASSET_DIR + f, size, fallback=fallbacks[name])
        for name, f in files.items()}
    masks = {
        "circle": u.Mask(MASK_DIR + "circle_in_drawer.png", size, (0, 0), collectCircle),
        "vampire": u.Mask(MASK_DIR + "vampire.png", size, (0, 0), talk),
        "cabinet": u.Mask(MASK_DIR + "cabinet.png", size, (0, 0), openCabinet),
        "fusebox": u.Mask(MASK_DIR + "fusebox.png", size, (0, 0), openFuseboxCloseup),
        "stone": u.Mask(MASK_DIR + "red.png", size, (-120, -30), collectStone),
        "fusebox_closed": u.Mask(MASK_DIR + "fusebox_closed.png", size, (0, 0), openFuseboxDoor),
        "reset": u.Mask(MASK_DIR + "red_button.png", size, (0, 0), pressReset),
        "drawer": u.Mask(MASK_DIR + "cabinet_drawer.png", size, (0, 0), openDrawer),}
    load_texts()
    view = View.ROOM
    next_room = None
########## completion tracking ##########
def progress():
    return _require_player().getCompletion("VampRoom")

def has(event):
    return event in progress()["all"]

def add(event):
    _require_player().addCompletion("VampRoom", event, "")

def _require_player() -> Player:
    if player is None:
        raise RuntimeError("Vampire room has not been initialized")
    return player

def _require_front_ui() -> FrontUI:
    if fui is None:
        raise RuntimeError("Vampire room has not been initialized")
    return fui

########## buttons ##########
def current():
    global buttons
    buttons = {
        View.ROOM: [u.Button(780, 660, 220, 50, "Leave Room", leave)],
        View.FUSEBOX_CLOSED: [u.Button(870, 650, 150, 50, "Close", gotoRoom)],
        View.FUSEBOX_OPEN: [
            u.Button(560, 600, 150, 50, "Insert Fuse", insertFuse),
            u.Button(900, 600, 150, 50, "Close", gotoRoom),
        ],
        View.CABINET: [u.Button(900, 600, 150, 50, "Close", gotoRoom)],
        View.DRAWER: [u.Button(900, 600, 150, 50, "Close", gotoCabinet)],}

########## inventory helpers ##########
def hasItem(name):
    return _require_player().has_item("Items", name)

def removeItem(name):
    _require_player().remove_item("Items", name)

########## helpers ##########
def say(text):
    _require_front_ui().chat.say(text)

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
    raise ValueError(f"Unknown vampire room view: {view!r}")

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
        return [] if circle_found else [masks["circle"]]
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
    if intro_line < 4:
        intro_line += 1
        say("Vampire > " + text_for(intro_line))
        # Save the first three dialogue milestones
        if intro_line <= 3:
            event = f"vamp.talk_{intro_line}"
            if not has(event):
                add(event)
    else:
        say("Vampire > " + text_for(5))

########## circle ##########
def collectCircle():
    global circle_found
    if circle_found or hasItem(CIRCLE_ITEM):
        circle_found = True
        return
    _require_player().add_item("Items", CIRCLE_ITEM, CIRCLE_ICON)
    circle_found = True
    if not has("vamp.circle_found"):
        add("vamp.circle_found")
    say("You > " + text_for(6))

########## fuse box ##########
def insertFuse():
    global fuse_inserted

    if fuse_inserted:
        return
    # the fuse is collected in another room
    if not hasItem(FUSE_ITEM):
        say("You > " + text_for(7))
        return
    removeItem(FUSE_ITEM)
    fuse_inserted = True
    if not has("vamp.fuse_inserted"):
        add("vamp.fuse_inserted")
    say("You > " + text_for(8))

def pressReset():
    global task_done
    if task_done:
        return
    if not fuse_inserted:
        say("You > " + text_for(9))
        return
    task_done = True
    if not has("vamp.task_done"):
        add("vamp.task_done")
    say("You > " + text_for(10))
    say("You > " + text_for(11))

########## stone ##########
def collectStone():
    global stone_collected
    if not task_done or stone_collected:
        return
    _require_player().add_item("Stones", "Red", STONE_IMAGE)
    stone_collected = True
    if not has("vamp.stone"):
        add("vamp.stone")
    say("You > " + text_for(12))
