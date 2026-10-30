import pygame
import UI.uiElements as u
import functions.leaderboard as lb


# these names must match what the other rooms put in the inventory
REQUIRED_STONES = ["White", "Red", "Green", "Purple", "Yellow"]

STONE_IMAGES = {
    "White":  "assets/stones/white.png",
    "Red":    "assets/stones/red.png",
    "Green":  "assets/stones/green.png",
    "Purple": "assets/stones/purple.png",
    "Yellow": "assets/stones/yellow.png",
}

STONE_COLOURS = {
    "White":  (235, 230, 225),
    "Red":    (170, 35, 35),
    "Green":  (45, 150, 85),
    "Purple": (150, 90, 210),
    "Yellow": (225, 180, 45),
}

# testing only: True gives the player all five stones when the room is created
TEST_GIVE_ALL_STONES = False

# dialogue ids: stone placed = STONE_LINE_FIRST + its place in REQUIRED_STONES,
# x stones missing = MISSING_LINE_BASE - missing
STONE_LINE_FIRST = 15
MISSING_LINE_BASE = 15

# one mask per hole, centre is measured on the original 1024 x 572 chest picture
CHEST_PICTURE_SIZE = (1024, 572)

STONE_HOLES = [
    {"colour": "Green",  "mask": "assets/teacherRoom/tr_cutout_2_stone_1_left.png",   "centre": (379, 250)},
    {"colour": "Purple", "mask": "assets/teacherRoom/tr_cutout_3_stone_2.png",        "centre": (455, 250)},
    {"colour": "Red",    "mask": "assets/teacherRoom/tr_cutout_4_stone_3_middle.png", "centre": (514, 247)},
    {"colour": "White",  "mask": "assets/teacherRoom/tr_cutout_5_stone_4.png",        "centre": (572, 248)},
    {"colour": "Yellow", "mask": "assets/teacherRoom/tr_cutout_6_stone_5_right.png",  "centre": (651, 249)},
]

STONE_HEIGHT = 50

NECKLACE_MASK = "assets/teacherRoom/tr_necklace_in_chest.png"
# box around the thin necklace that also counts as a click, on the 1024 x 572 picture
NECKLACE_AREA = (404, 224, 221, 117)
NECKLACE_ICON = NECKLACE_MASK

COUNTER_POS = (615, 205)

IMAGE_OFFSET_X = 300


def load_stone(path, height):
    try:
        image = pygame.image.load(path).convert_alpha()
    except (pygame.error, FileNotFoundError):
        return None
    w, h = image.get_size()
    width = max(1, round(w * height / h))
    return pygame.transform.smoothscale(image, (width, height))


# loads the pictures, the saved progress, the masks and the buttons
def start(room):
    room.room_image = u.load_image("assets/teacherRoom/tr_room_chest.png", room.screensize)
    room.room_opened = u.load_image("assets/teacherRoom/tr_room_chest_open.jpg", room.screensize)
    room.current_image = room.room_image

    room.chest_closed_image = u.load_image("assets/teacherRoom/tr_chest_closed.jpeg", room.screensize)
    room.chest_open_image = u.load_image("assets/teacherRoom/tr_chest_open.jpeg", room.screensize)

    # how much the chest picture is stretched on this screen
    shown_w, shown_h = room.chest_closed_image.get_size()
    room.scale_x = shown_w / CHEST_PICTURE_SIZE[0]
    room.scale_y = shown_h / CHEST_PICTURE_SIZE[1]

    icon_height = max(1, round(STONE_HEIGHT * room.scale_y))
    room.stone_icons = {}
    for name in REQUIRED_STONES:
        room.stone_icons[name] = load_stone(STONE_IMAGES[name], icon_height)

    room.font = pygame.font.Font(None, 28)
    room.slotFont = pygame.font.Font(None, 56)

    # progress comes from player.completion, so it is still there after leaving or loading
    done = room.player.getCompletion("TeacherRoom")["all"]

    room.room_described = "tr.described" in done
    room.chest_described = "tr.chest_described" in done

    room.stones_placed = [s for s in REQUIRED_STONES if "tr.placed." + s in done]
    room.chest_unlocked = "tr.unlocked" in done
    room.reward_taken = "tr.necklace" in done
    if room.chest_unlocked:
        room.current_image = room.room_opened

    # True while a click is handled by a hole, so the lid behind it ignores that click
    room.hole_clicked = False

    if TEST_GIVE_ALL_STONES:
        for name in REQUIRED_STONES:
            if not room.player.has_item("Stones", name):
                room.player.add_item("Stones", name, STONE_IMAGES[name])

    room.masks = [
        u.Mask("assets/teacherRoom/tr_room_chest_mask.png", room.screensize, (0, 0), lambda: chest(room), "Chest"),
    ]

    room.chest_masks = []
    for hole in STONE_HOLES:
        colour = hole["colour"]
        # colour=colour locks in the colour for each hole
        room.chest_masks.append(
            u.Mask(hole["mask"], room.screensize, (0, 0),
                   lambda colour=colour: place_stone(room, colour),
                   colour + " stone hole")
        )

    room.chest_masks.append(
        u.Mask("assets/teacherRoom/tr_cutout_1_whole_chest.png", room.screensize, (0, 0), lambda: try_open(room), "Chest lid")
    )

    room.necklace_masks = [
        u.Mask(NECKLACE_MASK, room.screensize, (0, 0), lambda: take_reward(room), "Necklace"),
    ]

    nx, ny, nw, nh = NECKLACE_AREA
    room.necklace_rect = pygame.Rect(
        IMAGE_OFFSET_X + round(nx * room.scale_x), round(ny * room.scale_y),
        round(nw * room.scale_x), round(nh * room.scale_y))

    room.no_masks = []
    room.current_masks = room.masks

    room.buttons = [
        u.Button(560, 650, 140, 50, "Return", lambda: returnc(room)),
    ]
    room.current_buttons = room.buttons

    room.returnr_buttons = [
        u.Button(1000, 520, 140, 50, "Return", lambda: returnr(room))]

    room.chest_buttons = room.returnr_buttons


def on_enter(room):
    if room.room_described:
        return
    room.room_described = True
    add(room, "tr.described")
    room.fui.sendMessage("You", "TeacherRoom", 1)
    room.fui.sendMessage("You", "TeacherRoom", 2)
    room.fui.sendMessage("You", "TeacherRoom", 3)


def chest(room):
    if room.chest_unlocked:
        room.current_image = room.chest_open_image
        room.current_buttons = room.returnr_buttons
        if room.reward_taken:
            room.current_masks = room.no_masks
            room.fui.sendMessage("You", "TeacherRoom", 26)
        else:
            room.current_masks = room.necklace_masks
            room.fui.sendMessage("You", "TeacherRoom", 24)
    else:
        room.current_image = room.chest_closed_image
        room.current_masks = room.chest_masks
        room.current_buttons = room.chest_buttons

        if not room.chest_described:
            room.chest_described = True
            add(room, "tr.chest_described")
            room.fui.sendMessage("You", "TeacherRoom", 6)
            room.fui.sendMessage("You", "TeacherRoom", 7)
            room.fui.sendMessage("You", "TeacherRoom", 8)
        else:
            describe_slots(room)


def describe_slots(room):
    missing = len(REQUIRED_STONES) - len(room.stones_placed)
    if missing == 0:
        room.fui.sendMessage("You", "TeacherRoom", 9)
    else:
        room.fui.sendMessage("You", "TeacherRoom", MISSING_LINE_BASE - missing)


def try_open(room):
    if room.hole_clicked:
        return
    missing = len(REQUIRED_STONES) - len(room.stones_placed)
    if missing > 0:
        room.fui.sendMessage("You", "TeacherRoom", MISSING_LINE_BASE - missing)
    else:
        unlock(room)


# called when the player clicks one hole
def place_stone(room, colour):
    room.hole_clicked = True

    if room.chest_unlocked:
        room.fui.sendMessage("You", "TeacherRoom", 21)
        return

    if colour in room.stones_placed:
        describe_slots(room)
        return

    if not room.player.has_item("Stones", colour):
        room.fui.sendMessage("You", "TeacherRoom", 20)
        return

    room.player.remove_item("Stones", colour)
    room.stones_placed.append(colour)
    add(room, "tr.placed." + colour)
    room.fui.sendMessage("You", "TeacherRoom", STONE_LINE_FIRST + REQUIRED_STONES.index(colour))

    if len(room.stones_placed) == len(REQUIRED_STONES):
        unlock(room)


def unlock(room):
    room.chest_unlocked = True
    add(room, "tr.unlocked")
    room.current_image = room.chest_open_image
    room.current_masks = room.necklace_masks
    room.current_buttons = room.returnr_buttons
    room.fui.sendMessage("You", "TeacherRoom", 22)
    room.fui.sendMessage("You", "TeacherRoom", 23)
    room.fui.sendMessage("You", "TeacherRoom", 24)


def take_reward(room):
    if room.reward_taken:
        return
    room.reward_taken = True
    add(room, "tr.necklace")
    room.player.add_item("Items", "Necklace", NECKLACE_ICON)
    lb.finishRun(room.player)
    room.fui.sendMessage("You", "TeacherRoom", 25)
    room.current_image = room.chest_open_image
    room.current_masks = room.no_masks
    room.current_buttons = room.returnr_buttons


def returnc(room):
    room.next_room = "corridor"


def returnr(room):
    if room.chest_unlocked:
        room.current_image = room.room_opened
        room.fui.sendMessage("You", "TeacherRoom", 5)
    else:
        room.current_image = room.room_image
        room.fui.sendMessage("You", "TeacherRoom", 4)
    room.current_masks = room.masks
    room.current_buttons = room.buttons


# saves a step of this room in player.completion
def add(room, event):
    room.player.addCompletion("TeacherRoom", event, "")


def handle_event(room, event):
    room.hole_clicked = False

    for m in room.current_masks:
        m.handle_event(event)

    for b in room.current_buttons:
        b.handle_event(event)

    # a click anywhere in the box around the necklace also counts
    if (room.current_image is room.chest_open_image
            and room.chest_unlocked and not room.reward_taken
            and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
            and room.necklace_rect.collidepoint(event.pos)):
        take_reward(room)


def hole_center(room, i):
    cx, cy = STONE_HOLES[i]["centre"]
    x = IMAGE_OFFSET_X + round(cx * room.scale_x)
    y = round(cy * room.scale_y)
    return (x, y)


def draw_stones(room):
    for i in range(len(STONE_HOLES)):
        colour = STONE_HOLES[i]["colour"]
        if colour not in room.stones_placed:
            continue

        cx, cy = hole_center(room, i)
        icon = room.stone_icons[colour]
        if icon is not None:
            room.screen.blit(icon, icon.get_rect(center=(cx, cy)))
        else:
            radius = round(STONE_HEIGHT * room.scale_y / 2)
            pygame.draw.circle(room.screen, STONE_COLOURS[colour], (cx, cy), radius)


def draw(room):
    if not room.room_described:
        on_enter(room)

    room.screen.blit(room.current_image, (IMAGE_OFFSET_X, 0))

    for m in room.current_masks:
        m.draw(room.screen)

    # drawn after the masks, so the stones and the counter end up on top of the chest
    if room.current_image is room.chest_closed_image:
        draw_stones(room)
        shown = str(len(room.stones_placed)) + " / " + str(len(REQUIRED_STONES))
        text = room.slotFont.render(shown, True, (0, 255, 120))
        room.screen.blit(text, COUNTER_POS)

    for b in room.current_buttons:
        b.draw2(room.screen)
