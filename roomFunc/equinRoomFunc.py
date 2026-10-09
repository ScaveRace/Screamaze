import pygame
import UI.uiElements as u

RECIPE = [("bread", "assets/equinoxRoom/bottom_bun.png", 190), #name, path, width
          ("butter", "assets/equinoxRoom/butter_spread.png", 170),
          ("cheese", "assets/equinoxRoom/cheese.png", 175),
          ("tomato", "assets/equinoxRoom/tomato.png", 170),
          ("lettuce", "assets/equinoxRoom/lettuce.png", 200),
          ("mayo", "assets/equinoxRoom/mayo_splatter.png", 150),
          ("ham", "assets/equinoxRoom/ham.png", 190),
          ("bread", "assets/equinoxRoom/top_bun.png", 190)]

ITEMS = [
    ("bread", "assets/equinoxRoom/bottom_bun.png", (494, 428), 46, (880, 260), 110), #name, path, roomPos, roomW, tablePos, tableW
    ("bread", "assets/equinoxRoom/top_bun.png", (494, 329), 46, (1000, 260), 110),
    ("butter", "assets/equinoxRoom/butter_block.png", (653, 203), 46, (1110, 260), 110),
    ("cheese", "assets/equinoxRoom/cheese.png", (776, 329), 46, (880, 390), 110),
    ("tomato", "assets/equinoxRoom/tomato.png", (727, 383), 46, (1000, 390), 110),
    ("lettuce", "assets/equinoxRoom/lettuce.png", (459, 536), 50, (1110, 390), 110),
    ("mayo", "assets/equinoxRoom/mayo_bottle.png", (649, 536), 25, (880, 520), 55),
    ("ham", "assets/equinoxRoom/ham.png", (395, 252), 50, (1000, 520), 110),
]

# you'll notice some lambdas below in the code, that is to prevent buttons and masks from firing their functions upon being built.

STUDENT = {"regular": ("assets/equinoxRoom/student_regular.png", 60), # state, path, width. regular -> angry1 -> angry2 per mistake
           "angry1": ("assets/equinoxRoom/student_angry1.png", 60),
           "angry2": ("assets/equinoxRoom/student_angry2.png", 60),
           "demonTrans": ("assets/equinoxRoom/student_demon_trans.png", 73), # after the sandwich: transforms, then the demon
           "demon": ("assets/equinoxRoom/student_demon.png", 68)}
STUDENT_POS = (600, 350) # centre of the student in the room, change to move him
TRANSFORM_TIME = 1500 # how long the transform sprite shows before the demon
DEMON_TIME = 2500 # how long the demon stands there before the blink
BLINK_FRAMES = 40 # frames the screen takes to go black, and to come back

STONE_PATH = "assets/stones/yellow.png"
SHAPE_NAME = "Triangle" # one of the three project room badges, exactly this spelling
SHAPE_PATH = "assets/shapes/triangle.png" # lies next to the stone, also its icon in the inventory
SHAPE_WIDTH = 44
SHAPE_POS = (684, 186) # centre of the badge in the room, next to the stone, change to move it
LAYER_STEP = 14
PLATE_CENTRE = (600, 493)
MAX_MISTAKES = 2

FADE_DELAY = 1500
FADE_FRAMES = 90
FADE_HOLD = 600

DB_TABLE = "EquinoxRoom"
INTRO = [(None, "intro_1"), (None, "intro_2")]
TALK = [("Student", "talk_1"), ("Student", "talk_2"), ("Student", "talk_3")]
LOOK_AWAY = [(None, "lookaway_1"), (None, "lookaway_2")]
FAIL = [("Student", "fail_1"), (None, "fail_2")]
COMPLETE = [(None, "complete_1"), (None, "complete_2"), ("Demon", "complete_3"), ("Demon", "complete_4"),
            ("Demon", "complete_5"), ("Demon", "complete_6"), ("Demon", "complete_7")]


def fitWidth(path, width): # better scaling, will edit in mask later maybe.
    w, h = pygame.image.load(path).get_size()
    return (width, round(width * h / w))


def makeMask(path, width, centre, action):
    w, h = fitWidth(path, width)
    return u.Mask(path, (w + u.startX, h), (centre[0] - w // 2, centre[1] - h // 2), action)


def loadImages(screen):
    roomImage = u.load_image("assets/equinoxRoom/room_empty.png", screen.get_size())
    tableImage = u.load_image("assets/equinoxRoom/background_table_plate.png", screen.get_size())
    fade = pygame.Surface(screen.get_size())
    fade.fill((0, 0, 0))
    layers = [u.load_alpha_image(path, fitWidth(path, width)) for name, path, width in RECIPE]
    demon = {s: u.load_alpha_image(STUDENT[s][0], fitWidth(*STUDENT[s])) for s in ("demonTrans", "demon")}
    return roomImage, tableImage, fade, layers, demon


def buildMasks(room):
    masks = []
    for name, path, roomPos, roomW, tablePos, tableW in ITEMS:
        for view, pos, width, action in (("room", roomPos, roomW, collect), ("table", tablePos, tableW, place)):
            entry = {"view": view, "name": name, "file": path}
            entry["mask"] = makeMask(path, width, pos, lambda e=entry, a=action: a(room, e))
            masks.append(entry)
    stone = {"view": "stone", "name": "stone", "file": STONE_PATH}
    stone["mask"] = makeMask(STONE_PATH, 40, (640, 175), lambda: takeStone(room))
    masks.append(stone)
    masks.append({"view": "shape", "name": "shape", "file": SHAPE_PATH,
                  "mask": makeMask(SHAPE_PATH, SHAPE_WIDTH, SHAPE_POS, lambda: takeShape(room))})
    for state in ("regular", "angry1", "angry2"): # only the one that fits the mistakes made is shown
        path, width = STUDENT[state]
        masks.append({"view": "student", "name": state, "file": path,
                      "mask": makeMask(path, width, STUDENT_POS, lambda: talkToStudent(room))})
    return masks


def buildButtons(room):
    return {
        "corridor": u.Button(1250, 650, 170, 50, "corridor", lambda: corridor(room)),
        "plate": u.Button(820, 650, 200, 50, "to the plate", lambda: toTable(room)),
        "room": u.Button(820, 650, 200, 50, "back to the room", lambda: toRoom(room)),
    }


def progress(room): # just points to specific room equinox from completion
    return room.player.getCompletion("EquinoxRoom")


def has(room, event): # easy check to see if something already happened.
    return event in progress(room)["all"]


def add(room, event):
    room.player.addCompletion("EquinoxRoom", event, "")


def getStep(room):
    return len([e for e in progress(room)["all"] if e.startswith("equin.placed.")])


def getMistakes(room):
    return progress(room)["all"].count("equin.mistake")


def resetProgress(room):
    progress(room)["all"].clear()
    progress(room)["current"] = ""
    progress(room)["msg"] = ""


def say(room, who, messageID, **values):
    text = room.fui.db.chatMessage(DB_TABLE, messageID).format(**values)
    room.fui.chat.say(f"{who} > {text}" if who else text)


def sayAll(room, lines):
    for who, messageID in lines:
        say(room, who, messageID)


def intro(room):
    if has(room, "equin.sandwich") and not has(room, "equin.lookaway"):
        add(room, "equin.lookaway")

    if has(room, "equin.stone"):
        say(room, None, "intro_empty")
    elif has(room, "equin.lookaway"):
        say(room, None, "intro_gone")
    elif has(room, "equin.talked"):
        say(room, None, "intro_waiting")
    else:
        sayAll(room, INTRO)


def getElements(room): # basically the logic
    pictures, masks, buttons = [], [], [room.btn["corridor"]]

    if room.view == "room":
        pictures.append((room.roomImage, (u.startX, 0)))
    else:
        pictures.append((room.tableImage, (u.startX, 0)))
        for i in range(getStep(room)):
            centre = (PLATE_CENTRE[0] + u.startX, PLATE_CENTRE[1] - i * LAYER_STEP)
            pictures.append((room.layers[i], room.layers[i].get_rect(center=centre).topleft))

    if room.failing:
        return pictures, [], []

    if has(room, "equin.stone") or has(room, "equin.lookaway"): # the stone and the badge lie on the table until you take them
        masks += [m["mask"] for m in room.allMasks if (m["view"] == "stone" and not has(room, "equin.stone"))
                  or (m["view"] == "shape" and not has(room, "equin.shape"))]
    elif has(room, "equin.sandwich"):
        pass # nothing to click, the demon blinks away by itself (see blink)
    elif has(room, "equin.talked") and room.view == "table":
        buttons.append(room.btn["room"])
        masks += [m["mask"] for m in room.allMasks if m["view"] == "table"
                  and has(room, "equin.got." + m["file"]) and not has(room, "equin.placed." + m["file"])]
    else: # in the room: the student is a mask, he says the recipe once you talked to him
        if has(room, "equin.talked"):
            buttons.append(room.btn["plate"])
        masks += [m["mask"] for m in room.allMasks
                  if m["view"] == "room" and not has(room, "equin.got." + m["file"])]
        masks += [m["mask"] for m in room.allMasks if m["view"] == "student" and m["name"] == studentState(room)]
    return pictures, masks, buttons


def corridor(room):
    room.next_room = "corridor"


def toTable(room):
    room.view = "table"


def toRoom(room):
    room.view = "room"


def studentState(room): # he gets angrier with every mistake
    return ("regular", "angry1", "angry2")[min(getMistakes(room), 2)]


def talkToStudent(room): # clicking the student: talk first, the recipe after
    if has(room, "equin.talked"):
        recipe(room)
    else:
        talk(room)


def talk(room):
    add(room, "equin.talked")
    sayAll(room, TALK)
    recipe(room)
    say(room, "Student", "talk_4")


def recipe(room):
    order = ". ".join(name.capitalize() for name, path, width in RECIPE) + "."
    say(room, "Student", "recipe", order=order)
    if getStep(room) > 0:
        say(room, None, "recipe_layers", step=getStep(room), total=len(RECIPE))


def lookAway(room):
    add(room, "equin.lookaway")
    sayAll(room, LOOK_AWAY)


def takeStone(room):
    room.player.add_item("Stones", "Yellow", STONE_PATH)
    add(room, "equin.stone")
    say(room, None, "stone")


def takeShape(room): # the project room needs this badge
    room.player.add_item("Items", SHAPE_NAME, SHAPE_PATH)
    add(room, "equin.shape") # after add_item, so a failed pickup doesn't count as taken. It is only given once, even after the project room used it
    say(room, None, "shape")


def collect(room, item):
    add(room, "equin.got." + item["file"])
    say(room, None, "collect", name=item["name"])


def place(room, item):
    if item["name"] != RECIPE[getStep(room)][0]:
        mistake(room, item)
        return
    add(room, "equin.placed." + item["file"])
    say(room, None, "place", name=item["name"])
    if getStep(room) == len(RECIPE):
        complete(room)


def mistake(room, item):
    add(room, "equin.mistake")
    say(room, "Student", "mistake_item", name=item["name"].capitalize())

    if getMistakes(room) > MAX_MISTAKES:
        fail(room)
    elif getMistakes(room) == MAX_MISTAKES:
        say(room, "Student", "mistake_2")
    else:
        say(room, "Student", "mistake_1")


def fail(room):
    resetProgress(room)
    room.failing = True
    room.fadeStart = pygame.time.get_ticks()
    sayAll(room, FAIL)


def complete(room):
    add(room, "equin.sandwich")
    room.transformStart = pygame.time.get_ticks()
    room.view = "room"
    sayAll(room, COMPLETE)


def drawDemon(room): # the sandwich is done: he transforms, then the demon stays until you look away
    if room.view != "room" or not has(room, "equin.sandwich") or has(room, "equin.lookaway"):
        return
    state = "demonTrans" if pygame.time.get_ticks() - room.transformStart < TRANSFORM_TIME else "demon"
    image = room.demon[state]
    room.screen.blit(image, image.get_rect(center=(STUDENT_POS[0] + u.startX, STUDENT_POS[1])))


def drawInfo(room):
    if has(room, "equin.talked") and not has(room, "equin.sandwich") and not room.failing:
        left = MAX_MISTAKES - getMistakes(room)
        room.screen.blit(room.font.render(f"Mistakes left: {left}", True, (222, 222, 214)), (320, 60))


def blink(room): # sandwich done: the demon stands there, the screen fades to black, he is gone, the screen fades back
    if has(room, "equin.sandwich") and not has(room, "equin.lookaway"):
        room.fadeAlpha = u.storyImageAnim(room.transformStart + TRANSFORM_TIME + DEMON_TIME, room.fadeAlpha, BLINK_FRAMES)
        if room.fadeAlpha >= 255:
            lookAway(room) # in the dark: he is gone and the stone lies there
            room.getElements()
    else:
        room.fadeAlpha = max(room.fadeAlpha - 255 / BLINK_FRAMES, 0)
    if room.fadeAlpha > 0:
        room.fade.set_alpha(int(room.fadeAlpha))
        room.screen.blit(room.fade, (0, 0))


def drawFade(room):
    if not room.failing:
        blink(room)
        return
    room.fadeAlpha = u.storyImageAnim(room.fadeStart + FADE_DELAY, room.fadeAlpha, FADE_FRAMES)
    if room.fadeAlpha > 0:
        room.fade.set_alpha(int(room.fadeAlpha))
        room.screen.blit(room.fade, (0, 0))
    if room.fadeAlpha >= 255:
        if room.fadeEnd is None:
            room.fadeEnd = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - room.fadeEnd > FADE_HOLD:
            room.next_room = "corridor"
