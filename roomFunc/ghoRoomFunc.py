# roomFunc/ghoRoomFunc.py
import pygame
import UI.uiElements as u

pygame.font.init()

ROOM = "GhostRoom"
A = "assets/ghostRoom/"
CABINET_CODE = "4537"                 # string to avoid strange behaviour
CODE_POS = (615, 205)                 # where typed digits are drawn
KEYPAD_ORIGIN, KEY, STEP = (500, 300), 70, 80
HOMEWORK_SPOT = pygame.Rect(600, 400, 56, 56)
ICON = "assets/gr.room.teacher.jpg"   # inventory icon for stone and homework
CODE_FONT = pygame.font.Font(None, 56)

# saved events (player.completion["GhostRoom"]["all"])
DESCRIBED, UNLOCKED = "gr.described", "gr.cabinet_unlocked"
HW_TAKEN, HW_DONE, STONE = "gr.homework_taken", "gr.homework_done", "gr.stone_taken"
TALK = ("gr.talk_1", "gr.talk_2", "gr.talk_3")

next_room = None
_player = _fui = None
_ui = {"view": "room", "code": ""}    # screen-only state: room/teacher/cabinet/keypad/whiteboard


# ---------------------------------------------------------------- helpers
def done(event):
    return event in _player.getCompletion(ROOM)["all"]


def save(event, msg):
    _player.addCompletion(ROOM, event, msg)


def say(n, who="You"):
    _fui.sendMessage(who, ROOM, n)


def show(*numbers):
    for n in numbers:
        say(n)


def has_homework():
    return done(HW_TAKEN) and not done(HW_DONE)


def stone_visible():
    """The stone floats behind the empty desk until it is picked up."""
    return _ui["view"] == "teacher" and done(HW_DONE) and not done(STONE)


def reset():
    _ui.update(view="room", code="")


def state():
    """Changes whenever the view or the saved progress changes -> room rebuilds."""
    return _ui["view"], len(_player.getCompletion(ROOM)["all"])


# ---------------------------------------------------------------- building
def background():
    view, hw = _ui["view"], done(HW_DONE)
    if view == "room":
        return A + ("gr.ghostRoom.no.teacher.png" if hw else "gr.room.teacher.jpg")
    if view == "teacher":
        return A + ("gr.bureau.no.teacher.png" if hw else "gr.teacher.png")
    if view in ("cabinet", "keypad"):
        return A + ("gr.cabinet.open.keypad.png" if done(UNLOCKED) else "gr.cabinet.homework.png")
    return A + "gr.whiteboard.4537.png"


def masks():
    """(mask file, callback, label)"""
    view = _ui["view"]
    if view == "room":
        found = [("gr_room_whiteboard.png", show_whiteboard, "Whiteboard"),
                 ("gr_room_cabinet.png", show_cabinet, "Cabinet")]
        if not done(HW_DONE):            # the teacher is gone after the homework
            found.insert(0, ("gr_room_teacher_ghost.png", show_teacher, "Teacher"))
        return found
    if view == "teacher" and not done(HW_DONE):
        return [("gr_teacher_ghost.png", talk, "Talk to the ghost")]
    if stone_visible():
        # empty label: the stone is too small for text
        return [("gr_white_stone_2.png", take_stone, "")]
    if view == "cabinet" and not done(UNLOCKED):
        return [("gr_cabinet_homework_keypad.png", open_keypad, "Keypad")]
    return []


def buttons():
    """(x, y, w, h, label, callback)"""
    view = _ui["view"]
    back = (1000, 520, 140, 50, "Return", back_to_room)
    if view == "room":
        return [(560, 650, 140, 50, "Return", leave)]
    if view == "teacher" and not done(HW_DONE):
        return [(830, 660, 140, 50, "Give", give_homework), back]
    if view == "cabinet" and done(UNLOCKED) and not done(HW_TAKEN):
        return [(550, 600, 180, 50, "Take Homework", take_homework), back]
    if view == "keypad":
        keys = []
        for i, label in enumerate("123456789C0E"):
            action = clear_code if label == "C" else check_code if label == "E" \
                else (lambda d=label: press_digit(d))
            keys.append((KEYPAD_ORIGIN[0] + i % 3 * STEP, KEYPAD_ORIGIN[1] + i // 3 * STEP,
                         KEY, KEY, label, action))
        return keys + [(1000, 520, 140, 50, "Back", close_keypad)]
    return [back]


def getElements(player, fui, screen):
    global _player, _fui
    _player, _fui = player, fui
    size = screen.get_size()
    return ([u.load_image(background(), size)],
            [u.Mask(A + f, size, (0, 0), cb, label) for f, cb, label in masks()],
            [u.Button(*b) for b in buttons()])


# ---------------------------------------------------------------- actions
def on_enter():
    if not done(DESCRIBED):
        show(21, 22)                     # cold classroom
        save(DESCRIBED, 22)


def talk():
    if done(HW_DONE):
        say(6, "Ghost")
        return
    line = sum(done(e) for e in TALK)
    if line < 3:
        say(line + 1, "Ghost")
        save(TALK[line], line + 1)
    else:
        say(4 if has_homework() else 5, "Ghost")


def show_teacher():                      # only reachable while the teacher is still there
    _ui["view"] = "teacher"
    say(25)
    talk()


def show_whiteboard():
    _ui["view"] = "whiteboard"
    say(27)


def show_cabinet():
    _ui["view"] = "cabinet"
    if done(UNLOCKED):
        say(32 if done(HW_TAKEN) else 31)
    else:
        show(29, 30, 11)                 # homework painted on doors, keypad, locked


def take_stone():
    if done(STONE):
        say(9)
        return
    _player.add_item("Stones", "White", ICON)
    save(STONE, 10)
    say(10)


def open_keypad():
    _ui.update(view="keypad", code="")
    show(33, 12)


def close_keypad():
    _ui.update(view="cabinet", code="")


def press_digit(digit):
    if len(_ui["code"]) < 4:
        _ui["code"] += digit
        if len(_ui["code"]) == 4:
            check_code()


def clear_code():
    _ui["code"] = ""


def check_code():
    correct = _ui["code"] == CABINET_CODE
    _ui["code"] = ""
    if correct:
        save(UNLOCKED, 31)
        _ui["view"] = "cabinet"
        show(13, 31)                     # clunk, and what is inside
    else:
        say(14)


def take_homework():
    if done(HW_TAKEN):
        say(32)
        return
    _player.add_item("Items", "Homework", ICON)
    save(HW_TAKEN, 16)
    say(16)


def give_homework():
    if done(HW_DONE):
        say(17)
    elif not has_homework():
        say(18)
    else:
        items = _player.inventory["Items"]
        items[:] = [d for d in items if "Homework" not in d]
        save(HW_DONE, 8)                 # view stays "teacher": the empty desk with the stone
        show(19)
        say(20, "Ghost")
        show(26, 8)


def back_to_room():
    _ui.update(view="room", code="")
    say(24 if done(HW_DONE) else 23)


def leave():
    global next_room
    next_room = "corridor"


def keyboard(event):
    if _ui["view"] == "keypad" and event.type == pygame.KEYDOWN:
        if event.unicode.isdigit():
            press_digit(event.unicode)
        elif event.key == pygame.K_BACKSPACE:
            _ui["code"] = _ui["code"][:-1]
        elif event.key == pygame.K_RETURN:
            check_code()


# ---------------------------------------------------------------- drawing
def drawExtras(screen):
    view = _ui["view"]
    if view == "cabinet" and done(UNLOCKED) and not done(HW_TAKEN):
        pygame.draw.rect(screen, (235, 235, 235), HOMEWORK_SPOT)
    if view == "keypad":
        shown = _ui["code"].ljust(4, "-")             # "45" -> "45--"
        screen.blit(CODE_FONT.render(shown, True, (0, 255, 120)), CODE_POS)