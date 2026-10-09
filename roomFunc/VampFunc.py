import pygame
import UI.uiElements as u

ASSETS = {
    "bg_closed": "assets/vampire/Room2015_1_win_clo.png",
    "bg_open": "assets/vampire/Room2015_1_win_op.png",
    "cabinet": "assets/vampire/vp.cabinet.closed.png",
    "drawer": "assets/vampire/cabinet_drawer_open.png",
    "fusebox_closed": "assets/vampire/fuse_box.png",
    "fusebox_open": "assets/vampire/fuse_box2.png",
    "fusebox_three": "assets/vampire/fuse_box2_three_fuses.png",
}

MASKS = {
    "vampire": "assets/vampire/masks/vampire.png",
    "cabinet": "assets/vampire/masks/cabinet.png",
    "fusebox": "assets/vampire/masks/fusebox.png",
    "fusebox_closed": "assets/vampire/masks/fusebox_closed.png",
    "reset": "assets/vampire/masks/red_button.png",
    "drawer": "assets/vampire/masks/cabinet_drawer.png",
    "fuse": "assets/vampire/masks/fuse.png",
    "stone": "assets/vampire/masks/red.png",
}

STONE_PATH = "assets/stones/red.png"


# saves a step of this room in player.completion["VampRoom"]["all"]
def add(room, event):
    room.player.addCompletion("VampRoom", event, "")


def loadImages(screen):
    fallbacks = {
        "bg_closed": (35, 8, 18),
        "bg_open": (120, 100, 60),
        "cabinet": (120, 100, 60),
        "drawer": (120, 100, 60),
        "fusebox_closed": (20, 20, 20),
        "fusebox_open": (20, 20, 20),
        "fusebox_three": (20, 20, 20),
    }
    return {
        name: u.load_image(path, screen.get_size(), fallback=fallbacks[name])
        for name, path in ASSETS.items()
    }

def buildMasks(room):
    size = room.screen.get_size()
    return {
        "room": [
            u.Mask(MASKS["vampire"], size, (0, 0), lambda: talk(room)),
            u.Mask(MASKS["cabinet"], size, (0, 0), lambda: search_corner(room)),
            u.Mask(MASKS["fusebox"], size, (0, 0), lambda: open_fusebox_closeup(room)),
            u.Mask(MASKS["stone"], size, (0, 0), lambda: collect_stone(room))
        ],
        "fusebox_closed": [
            u.Mask(MASKS["fusebox_closed"], size, (0, 0), lambda: open_fusebox_door(room))
        ],
        "fusebox_open": [
            u.Mask(MASKS["reset"], size, (0, 0), lambda: press_reset(room))
        ],
        "cabinet": [
            u.Mask(MASKS["drawer"], size, (0, 0), lambda: open_drawer(room))
        ],
        "drawer": [
            u.Mask(MASKS["fuse"], size, (0, 0), lambda: collect_fuse(room))
        ]
    }

def buildButtons(room):
    return {
        "room": [u.Button(780, 660, 220, 50, "Leave Room", lambda: leave(room))],
        "fusebox_closed": [u.Button(870, 650, 150, 50, "Close", lambda: close_fusebox(room))],
        "fusebox_open": [
            u.Button(560, 600, 150, 50, "Insert Fuse", lambda: insert_fuse(room)),
            u.Button(900, 600, 150, 50, "Close", lambda: close_fusebox(room))
        ],
        "cabinet": [u.Button(900, 600, 150, 50, "Close", lambda: close_cabinet(room))],
        "drawer": [u.Button(900, 600, 150, 50, "Close", lambda: close_drawer(room))]
    }

def handle_event(room, event):
    state = room.states["state"]

    if state == "room":
        masks = room.masks["room"]
        if not room.states["task_done"]:
            masks[0].handle_event(event)
        if not room.states["fuse_found"]:
            masks[1].handle_event(event)
        masks[2].handle_event(event)
        if room.states["task_done"] and not room.states["stone_collected"]:
            masks[3].handle_event(event)

    elif state in room.masks:
        for mask in room.masks[state]:
            mask.handle_event(event)

    for button in room.buttons.get(state, []):
        button.handle_event(event)

def draw(room):
    state = room.states["state"]

    if state == "room":
        image = room.images["bg_open"] if room.states["task_done"] else room.images["bg_closed"]
        room.screen.blit(image, (300, 0))

        title = room.titleFont.render("The Vampire's Crypt", True, (200, 30, 40))
        room.screen.blit(title, (60, 40))

        masks = room.masks["room"]

        if not room.states["task_done"]:
            masks[0].draw(room.screen)
        if not room.states["fuse_found"]:
            masks[1].draw(room.screen)

        masks[2].draw(room.screen)

        if room.states["task_done"] and not room.states["stone_collected"]:
            masks[3].draw(room.screen)

    elif state == "fusebox_closed":
        room.screen.blit(room.images["fusebox_closed"], (300, 0))

    elif state == "fusebox_open":
        image = room.images["fusebox_three"] if room.states["fuse_inserted"] else room.images["fusebox_open"]
        room.screen.blit(image, (300, 0))

    elif state == "cabinet":
        room.screen.blit(room.images["cabinet"], (300, 0))

    elif state == "drawer":
        room.screen.blit(room.images["drawer"], (300, 0))

    for mask in room.masks.get(state, []):
        if state == "room":
            continue
        mask.draw(room.screen)

    for button in room.buttons.get(state, []):
        button.draw2(room.screen)

def talk(room):
    line = room.states["line"]

    if line < 3:
        room.fui.sendMessage("Vampire", "VampireRoom", 1)
        room.states["line"] += 1
        add(room, "vamp.talk_" + str(room.states["line"]))
        if room.states["line"] == 3:
            room.states["task_started"] = True
    elif not room.states["task_done"]:
        room.fui.sendMessage("Vampire", "VampireRoom", 4)
    else:
        room.fui.sendMessage("Vampire", "VampireRoom", 5)

def search_corner(room):
    room.states["state"] = "cabinet"

def open_drawer(room):
    room.states["state"] = "drawer"

def close_cabinet(room):
    room.states["state"] = "room"

def close_drawer(room):
    room.states["state"] = "cabinet"

def open_fusebox_closeup(room):
    room.states["state"] = "fusebox_closed"

def open_fusebox_door(room):
    room.states["state"] = "fusebox_open"

def close_fusebox(room):
    room.states["state"] = "room"

def collect_fuse(room):
    if room.states["fuse_found"]:
        return

    room.states["fuse_found"] = True
    add(room, "vamp.fuse_found")
    room.states["inventory"].append("fuse")
    room.fui.sendMessage("You", "VampireRoom", 6)

def insert_fuse(room):
    if room.states["fuse_inserted"]:
        return

    if "fuse" not in room.states["inventory"]:
        room.fui.sendMessage("You", "VampireRoom", 7)
        return

    room.states["inventory"].remove("fuse")
    room.states["fuse_inserted"] = True
    add(room, "vamp.fuse_inserted")
    room.fui.sendMessage("You", "VampireRoom", 8)

def press_reset(room):
    if room.states["task_done"]:
        return

    if not room.states["fuse_inserted"]:
        room.fui.sendMessage("You", "VampireRoom", 9)
        return

    room.states["task_done"] = True
    add(room, "vamp.task_done")
    room.fui.sendMessage("You", "VampireRoom", 10)
    room.fui.sendMessage("You", "VampireRoom", 11)

def collect_stone(room):
    if not room.states["task_done"] or room.states["stone_collected"]:
        return

    room.states["stone_collected"] = True
    room.states["inventory"].append("red_stone")
    room.player.add_item("Stones", "Red", STONE_PATH)   # the teacher room looks for this stone in the inventory
    add(room, "vamp.stone")
    room.fui.sendMessage("You", "VampireRoom", 12)

def leave(room):
    room.next_room = "corridor"