import pygame
import UI.uiElements as u
from player import Player
import UI.frontUI as Fui


def set_current():
    return "hello"

# roomFunc/ghostFunc.py
from functools import lru_cache, partial

import pygame
import UI.uiElements as u

ROOM = "GhostRoom"

CABINET_CODE = "4537"            # string to avoid strange behaviour
CODE_DISPLAY_POS = (615, 205)    # where typed digits are drawn -> tune to your art
KEYPAD_ORIGIN = (500, 300)       # top left corner of the "1" key
KEYPAD_SIZE = 70
KEYPAD_GAP = 10
HOMEWORK_SPOT = pygame.Rect(600, 400, 56, 56)
STONE_SPOT = pygame.Rect(750, 400, 44, 44)

# inventory icons (both still point at the room background, see notes)
STONE_ICON = "assets/gr.room.teacher.jpg"
HOMEWORK_ICON = "assets/gr.room.teacher.jpg"

# --- saved events (stored in player.completion["GhostRoom"]["all"]) ---
DESCRIBED = "gr.described"
TALK = ("gr.talk_1", "gr.talk_2", "gr.talk_3")
UNLOCKED = "gr.cabinet_unlocked"
HW_TAKEN = "gr.homework_taken"
HW_DONE = "gr.homework_done"
STONE = "gr.stone_taken"

# --- images ---
_IMAGES = {
    "room":           "assets/ghostRoom/gr.room.teacher.jpg",
    "room_empty":     "assets/ghostRoom/gr.ghostRoom.no.teacher.png",
    "teacher":        "assets/ghostRoom/gr.teacher.png",
    "no_teacher":     "assets/ghostRoom/gr.bureau.no.teacher.png",
    "whiteboard":     "assets/ghostRoom/gr.whiteboard.4537.png",
    "cabinet_locked": "assets/ghostRoom/gr.cabinet.homework.png",
    "cabinet_open":   "assets/ghostRoom/gr.cabinet.open.keypad.png",
}

_KEYPAD_LABELS = ["1", "2", "3",
                  "4", "5", "6",
                  "7", "8", "9",
                  "C", "0", "E"]

# --- module state ---
next_room = None
# Screen-only state, never saved. view is one of:
# "room", "teacher", "cabinet", "keypad", "whiteboard"
_ui = {"view": "room", "code": "", "dirty": False}


# ---------------------------------------------------------------- helpers
def _done(player, event):
    return event in player.getCompletion(ROOM)["all"]


def _save(player, event, msg=None):
    """Record an event. Keeps the old msg when none is given."""
    if msg is None:
        msg = player.getCompletion(ROOM)["msg"]
    player.addCompletion(ROOM, event, msg)


def _say(fui, n, who="You"):
    fui.sendMessage(who, ROOM, n)


def _has_homework(player):
    return _done(player, HW_TAKEN) and not _done(player, HW_DONE)


def _remove_item(player, kind, name):
    for d in player.inventory[kind]:
        if name in d:
            player.inventory[kind].remove(d)
            return


def _set_view(view):
    _ui["view"] = view
    _ui["dirty"] = True


def reset_view():
    _ui.update(view="room", code="", dirty=False)


def needs_refresh():
    """True once after anything that changes images/masks/buttons."""
    dirty = _ui["dirty"]
    _ui["dirty"] = False
    return dirty


@lru_cache(maxsize=1)
def _code_font():
    return pygame.font.Font(None, 56)


# ---------------------------------------------------------------- building
def _image_key(player, view):
    if view == "room":
        return "room_empty" if _done(player, HW_DONE) else "room"
    if view == "teacher":
        return "no_teacher" if _done(player, HW_DONE) else "teacher"
    if view in ("cabinet", "keypad"):
        return "cabinet_open" if _done(player, UNLOCKED) else "cabinet_locked"
    return "whiteboard"


def _masks(player, fui, view):
    """(mask image, callback, label) for the current view."""
    if view == "room":
        return [
            ("assets/ghostRoom/gr_room_teacher_ghost.png", partial(show_teacher, player, fui), "Teacher"),
            ("assets/ghostRoom/gr_room_whiteboard.png", partial(show_whiteboard, fui), "Whiteboard"),
            ("assets/ghostRoom/gr_room_cabinet.png", partial(show_cabinet, player, fui), "Cabinet"),
        ]
    if view == "teacher" and not _done(player, HW_DONE):
        return [("assets/ghostRoom/gr_teacher_ghost.png", partial(talk, player, fui), "Talk to the ghost")]
    if view == "cabinet" and not _done(player, UNLOCKED):
        return [("assets/ghostRoom/gr_cabinet_homework_keypad.png", partial(open_keypad, fui), "Keypad")]
    return []


def _keypad_buttons(player, fui):
    keys = []
    x0, y0 = KEYPAD_ORIGIN
    step = KEYPAD_SIZE + KEYPAD_GAP
    for i, label in enumerate(_KEYPAD_LABELS):
        x = x0 + (i % 3) * step
        y = y0 + (i // 3) * step
        if label == "C":
            action = clear_code
        elif label == "E":
            action = partial(check_code, player, fui)
        else:
            action = partial(press_digit, player, fui, label)
        keys.append((x, y, KEYPAD_SIZE, KEYPAD_SIZE, label, action))
    keys.append((1000, 520, 140, 50, "Back", close_keypad))
    return keys


def _buttons(player, fui, view):
    """(x, y, w, h, label, callback) for the current view."""
    back = (1000, 520, 140, 50, "Return", partial(return_room, player, fui))

    if view == "room":
        return [(560, 650, 140, 50, "Return", return_corridor)]
    if view == "teacher":
        if not _done(player, HW_DONE):
            return [(830, 660, 140, 50, "Give", partial(give_homework, player, fui)), back]
        if not _done(player, STONE):
            return [(830, 600, 180, 50, "Take stone", partial(collect_stone, player, fui)), back]
        return [back]
    if view == "cabinet":
        if _done(player, UNLOCKED) and not _done(player, HW_TAKEN):
            return [(550, 600, 180, 50, "Take Homework", partial(take_homework, player, fui)), back]
        return [back]
    if view == "keypad":
        return _keypad_buttons(player, fui)
    return [back]   # whiteboard


def getElements(player, fui, screen):
    """Everything is rebuilt from saved state + current view."""
    size = screen.get_size()
    view = _ui["view"]

    images = [u.load_image(_IMAGES[_image_key(player, view)], size)]
    masks = [u.Mask(path, size, (0, 0), cb, label)
             for path, cb, label in _masks(player, fui, view)]
    buttons = [u.Button(x, y, w, h, label, cb)
               for x, y, w, h, label, cb in _buttons(player, fui, view)]
    return images, masks, buttons


# ---------------------------------------------------------------- actions
def on_enter(player, fui):
    if _done(player, DESCRIBED):
        return
    _say(fui, 21)   # cold classroom
    _say(fui, 22)
    _save(player, DESCRIBED, 22)


def talk(player, fui):
    if _done(player, HW_DONE):
        _say(fui, 6, "Ghost")
        return
    line = sum(_done(player, e) for e in TALK)
    if line < 3:
        _say(fui, line + 1, "Ghost")
        _save(player, TALK[line], line + 1)
    elif _has_homework(player):
        _say(fui, 4, "Ghost")
    else:
        _say(fui, 5, "Ghost")


def show_teacher(player, fui):
    _set_view("teacher")
    if _done(player, HW_DONE):
        _say(fui, 26)   # the empty desk
        _say(fui, 7 if _done(player, STONE) else 8)
    else:
        _say(fui, 25)   # ghost behind his desk
        talk(player, fui)


def collect_stone(player, fui):
    if _done(player, STONE):
        _say(fui, 9)
        return
    player.add_item("Stones", "White", STONE_ICON)
    _save(player, STONE, 10)
    _say(fui, 10)
    _ui["dirty"] = True


def show_cabinet(player, fui):
    _set_view("cabinet")
    if _done(player, UNLOCKED):
        _say(fui, 32 if _done(player, HW_TAKEN) else 31)
    else:
        _say(fui, 29)   # HOMEWORK painted on the doors
        _say(fui, 30)   # keypad on the front
        _say(fui, 11)   # locked


def open_keypad(fui):
    _ui["code"] = ""
    _set_view("keypad")
    _say(fui, 33)
    _say(fui, 12)


def close_keypad():
    _ui["code"] = ""
    _set_view("cabinet")


def press_digit(player, fui, digit):
    if len(_ui["code"]) >= 4:
        return
    _ui["code"] += digit
    if len(_ui["code"]) == 4:
        check_code(player, fui)


def clear_code():
    _ui["code"] = ""


def check_code(player, fui):
    if _ui["code"] == CABINET_CODE:
        _ui["code"] = ""
        _save(player, UNLOCKED, 31)
        _set_view("cabinet")
        _say(fui, 13)   # clunk, the cabinet swings open
        _say(fui, 31)
    else:
        _ui["code"] = ""
        _say(fui, 14)


def take_homework(player, fui):
    if _done(player, HW_TAKEN):
        _say(fui, 32)   # empty
        return
    player.add_item("Items", "Homework", HOMEWORK_ICON)
    _save(player, HW_TAKEN, 16)
    _say(fui, 16)
    _ui["dirty"] = True


def give_homework(player, fui):
    if _done(player, HW_DONE):
        _say(fui, 17)
        return
    if not _has_homework(player):
        _say(fui, 18)
        return
    _remove_item(player, "Items", "Homework")
    _save(player, HW_DONE, 8)
    _say(fui, 19)
    _say(fui, 20, "Ghost")
    _say(fui, 26)   # the desk he left behind
    _say(fui, 8)    # he left something on it
    _ui["dirty"] = True


def show_whiteboard(fui):
    _set_view("whiteboard")
    _say(fui, 27)


def return_room(player, fui):
    _set_view("room")
    _say(fui, 24 if _done(player, HW_DONE) else 23)


def return_corridor():
    global next_room
    next_room = "corridor"


def keyboard(event, player, fui):
    """Typing works next to the on-screen keys, only while the keypad is open."""
    if _ui["view"] != "keypad" or event.type != pygame.KEYDOWN:
        return
    if event.unicode.isdigit():
        press_digit(player, fui, event.unicode)
    elif event.key == pygame.K_BACKSPACE:
        _ui["code"] = _ui["code"][:-1]
    elif event.key == pygame.K_RETURN:
        check_code(player, fui)


# ---------------------------------------------------------------- drawing
def drawExtras(screen, player):
    view = _ui["view"]
    if view == "teacher" and _done(player, HW_DONE) and not _done(player, STONE):
        pygame.draw.circle(screen, (245, 245, 245), STONE_SPOT.center, STONE_SPOT.w // 2)
    if view == "cabinet" and _done(player, UNLOCKED) and not _done(player, HW_TAKEN):
        pygame.draw.rect(screen, (235, 235, 235), HOMEWORK_SPOT)
    if view == "keypad":
        shown = _ui["code"].ljust(4, "-")   # "45" -> "45--"
        screen.blit(_code_font().render(shown, True, (0, 255, 120)), CODE_DISPLAY_POS)