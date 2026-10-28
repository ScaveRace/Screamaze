# roomFunc/ghoRoomFunc.py

import pygame
import UI.uiElements as u

pygame.font.init()

ROOM = "GhostRoom"
A = "assets/ghostRoom/"
CABINET_CODE = "4537"                               # string to avoid strange behaviour
CODE_POS = (615, 205)                               # where typed digits are drawn
KEYPAD_ORIGIN, KEY, STEP = (500, 300), 70, 80
STONE_ICON = "assets/stones/white.png"              # inventory icon for the stone
HOMEWORK_CUTOUT = A + "gr_homework_cutout.png"      # the cutout is cropped to make the icon
HOMEWORK_ICON = A + "gr.homework_icon.png"           # homework inventory icon
CODE_FONT = pygame.font.Font(None, 56)
DESCRIBE_DELAY_MS = 400                             # wait after entering so the chatbox clear is over
                   # set to False when everything works

# saved events (player.completion["GhostRoom"]["all"])
DESCRIBED, UNLOCKED = "gr.described", "gr.cabinet_unlocked"
HW_TAKEN, HW_DONE, STONE = "gr.homework_taken", "gr.homework_done", "gr.stone_taken"
TALK = ("gr.talk_1", "gr.talk_2", "gr.talk_3")

next_room = None
_player = _fui = None
_ui = {"view": "room", "code": ""}    # screen-only state: room/teacher/cabinet/keypad/whiteboard
_pending = True                       # True = the room still has to be described
_enter_at = None                      # time of the first frame after entering


images = {}                           # all pictures, made once in start()
masks = {}                            # all masks, made once in start()
buttons = {}                          # all buttons, made once in start()



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


def homework_visible():
    """The homework lies in the open cabinet until it is picked up."""
    return _ui["view"] == "cabinet" and done(UNLOCKED) and not done(HW_TAKEN)


def reset():
    _ui.update(view="room", code="")


def state():
    """Changes whenever the view or the saved progress changes -> room rebuilds."""
    return (_ui["view"], done(UNLOCKED), done(HW_TAKEN), done(HW_DONE), done(STONE),
            len(_player.getCompletion(ROOM)["all"]))




# ---------------------------------------------------------------- building
def start(player, fui, screen):
    """Makes every image, mask and button once. Nothing is rebuilt after this."""
    size = screen.get_size()

    images["room"] = u.load_image(A + "gr.room.teacher.jpg", size)
    images["room_stone"] = u.load_image(A + "gr.ghostroom_with_stone.png", size)  # teacher became a stone, stone not taken yet
    images["room_empty"] = u.load_image(A + "gr.ghostRoom.no.teacher.png", size)
    images["teacher"] = u.load_image(A + "gr.teacher.png", size)
    images["teacher_empty"] = u.load_image(A + "gr.bureau.no.teacher.png", size)
    images["cabinet_locked"] = u.load_image(A + "gr.cabinet.homework.png", size)
    images["cabinet_open"] = u.load_image(A + "gr.cabinet.open.keypad.png", size)
    images["whiteboard"] = u.load_image(A + "gr.whiteboard.code.png", size)

    # u.Mask(file, size, position, callback, label)
    masks["teacher"] = u.Mask(A + "gr_room_teacher_ghost.png", size, (0, 0), show_teacher, "Teacher")
    masks["whiteboard"] = u.Mask(A + "gr_room_whiteboard.png", size, (0, 0), show_whiteboard, "Whiteboard")
    masks["cabinet"] = u.Mask(A + "gr_room_cabinet.png", size, (0, 0), show_cabinet, "Cabinet")
    # the stone lying in the room after the teacher turned into it (no label, too small)
    masks["room_stone"] = u.Mask(A + "gr.wh_stone_cutout.png", size, (0, 0), take_stone, "")
    masks["ghost"] = u.Mask(A + "gr_teacher_ghost.png", size, (0, 0), talk, "Talk to the ghost")
    # empty label: the stone is too small for text
    masks["stone"] = u.Mask(A + "gr_white_stone_2.png", size, (0, 0), take_stone, "")
    masks["homework"] = u.Mask(A + "gr_homework_cutout.png", size, (0, 0), take_homework, "Homework")
    masks["keypad"] = u.Mask(A + "gr_cabinet_homework_keypad.png", size, (0, 0), open_keypad, "Keypad")

    keys = []
    for i, label in enumerate("123456789C0E"):
        action = clear_code if label == "C" else check_code if label =="E"\
            else (lambda d=label: press_digit(d))
        keys.append(u.Button(KEYPAD_ORIGIN[0]  +  i % 3 * STEP, KEYPAD_ORIGIN[1]  + i // 3 * STEP, KEY , KEY, label, action))
    keys.append(u.Button(1000, 520, 140, 50, "Back", close_keypad))

    buttons["room"] = [u.Button(560, 650, 140, 50, "Corridor", leave)]
    buttons["teacher"] = [u.Button(830, 660, 140, 50, "Give", give_homework),
                          u.Button(1000, 520, 140, 50, "Return", back_to_room)]
    buttons["back"] = [u.Button(1000, 520, 140, 50, "Return", back_to_room)]
    buttons["keypad"] = keys


def currentImage():
    """The picture for the current view."""
    view, hw = _ui["view"], done(HW_DONE)
    if view == "room":
        if not hw:
            return images["room"]
        # teacher became aa stone: the stone lies there until it is taken
        return images["room_empty"] if done(STONE) else images["room_stone"]
    if view == "teacher":
        return images["teacher_empty"] if hw else images["teacher"]
    if view in ("cabinet", "keypad"):
        return images["cabinet_open"] if done(UNLOCKED) else images["cabinet_locked"]
    return images["whiteboard"]


def activeMasks():
    """The masks that can be clicked in the current view."""
    view = _ui["view"]
    if view == "room":
        found = [masks["whiteboard"], masks["cabinet"]]
        if not done(HW_DONE):            # the teacher is gone after the homework
            found.insert(0, masks["teacher"])
        if done(HW_DONE) and not done(STONE):
            found.append(masks["room_stone"])
        return found
    if view == "teacher" and not done(HW_DONE):
        return [masks["ghost"]]
    if stone_visible():
        return [masks["stone"]]
    if homework_visible():
        # disappears by itself once the homework is taken
        return [masks["homework"]]
    if view == "cabinet" and not done(UNLOCKED):
        return [masks["keypad"]]
    return []


def currentButtons():
    """The buttons shown in the current view."""
    view = _ui["view"]
    if view == "room":
        return buttons["room"]
    if view == "teacher" and not done(HW_DONE):
        return buttons["teacher"]
    if view == "keypad":
        return buttons["keypad"]
    return buttons["back"]


def getElements(player, fui, screen):
    global _player, _fui
    _player, _fui = player, fui
    if not images:  # only the very first time
        start(player, fui, screen)
    return [currentImage()], activeMasks(), currentButtons()


# ---------------------------------------------------------------- actions
def describe():
    """Describes the whole room."""
    if done(HW_DONE):
        show(21, 34)                     # teacher is gone: empty desk
    else:
        show(21, 22)                     # full description with the ghost teacher
    save(DESCRIBED, 22)                  # kept so older saves still work


def on_enter(player=None, fui=None):
    """Called when the player walks into the room: reset the view, describe soon."""
    global _player, _fui, _pending, _enter_at
    if player is not None:
        _player, _fui = player, fui
    reset()
    _pending, _enter_at = True, None


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
    _player.add_item("Stones", "White", STONE_ICON)
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
    """Clicking the homework cutout in the open cabinet."""
    if done(HW_TAKEN):
        say(32)
        return
    _player.add_item("Items", "Homework", HOMEWORK_ICON)
    save(HW_TAKEN, 16)                   # saving rebuilds the room, so the mask disappears
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
    global next_room, _pending, _enter_at
    next_room = "corridor"
    reset()
    _pending, _enter_at = True, None     # describe again next time the room is entered


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
    global _pending, _enter_at
    if _pending:                         # runs every frame while the room is on screen
        now = pygame.time.get_ticks()
        if _enter_at is None:
            _enter_at = now              # first frame after entering
        elif now - _enter_at >= DESCRIBE_DELAY_MS:
            _pending, _enter_at = False, None
            describe()

    if _ui["view"] == "keypad":
        shown = _ui["code"].ljust(4, "-")             # "45" -> "45--"
        screen.blit(CODE_FONT.render(shown, True, (0, 255, 120)), CODE_POS)