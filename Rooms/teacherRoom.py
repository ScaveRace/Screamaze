import pygame
import UI.uiElements as u
from player import Player
import UI.frontUI as Fui
import functions.leaderboard as lb

pygame.init()
pygame.mixer.init()

# ----------------------------------------------------------------------
# THE FIVE STONES
# ----------------------------------------------------------------------

# The five stones that have to go into the chest, in the order of the holes.
# These names must match exactly what the other rooms put in the inventory,
# for example GhostRoom does: player.add_item("Stones", "White", ...)
REQUIRED_STONES = ["White", "Red", "Green", "Purple", "Yellow"]

# The picture that belongs to every stone. ## placeholder folder
STONE_IMAGES = {
    "White":  "assets/stones/white.png",
    "Red":    "assets/stones/red.png",
    "Green":  "assets/stones/green.png",
    "Purple": "assets/stones/purple.png",
    "Yellow": "assets/stones/yellow.png",
}

# Fallback colours, only used when a picture above cannot be loaded.
STONE_COLOURS = {
    "White":  (235, 230, 225),
    "Red":    (170, 35, 35),
    "Green":  (45, 150, 85),
    "Purple": (150, 90, 210),
    "Yellow": (225, 180, 45),
}

# TESTING ONLY: set to True and the player gets all five stones the moment
# the teacher room is entered, so every hole can be checked without playing
# the other rooms. Set it back to False before the real game!
DEBUG_GIVE_ALL_STONES = False

# Dialogue ids, so the numbers below stay readable.
# One "stone placed" line per stone, in the order of REQUIRED_STONES.
STONE_LINE_FIRST = 15        # White = 15, Red = 16, Green = 17, Purple = 18, Yellow = 19
# One "x stones are still missing" line per possible amount.
# line id = MISSING_LINE_BASE - missing  ->  5 missing = 10, 1 missing = 14
MISSING_LINE_BASE = 15

# ----------------------------------------------------------------------
# THE FIVE HOLES ON THE LID (left to right, like the picture)
# ----------------------------------------------------------------------
# Every hole belongs to ONE stone colour and has its own mask picture.
# "centre" is where the middle of the hole is on the ORIGINAL 1024 x 572
# chest picture, the code scales it to your screen by itself.
CHEST_PICTURE_SIZE = (1024, 572)

STONE_HOLES = [
    {"colour": "Green",  "mask": "assets/teacherRoom/tr_cutout_2_stone_1_left.png",   "centre": (379, 250)},
    {"colour": "Purple", "mask": "assets/teacherRoom/tr_cutout_3_stone_2.png",        "centre": (455, 250)},
    {"colour": "Red",    "mask": "assets/teacherRoom/tr_cutout_4_stone_3_middle.png", "centre": (514, 247)},
    {"colour": "White",  "mask": "assets/teacherRoom/tr_cutout_5_stone_4.png",        "centre": (572, 248)},
    {"colour": "Yellow", "mask": "assets/teacherRoom/tr_cutout_6_stone_5_right.png",  "centre": (651, 249)},
]

# Height of a stone when it sits in its hole, on the ORIGINAL 572 high picture.
STONE_HEIGHT = 50

# Where the "3 / 5" counter is drawn on the chest close up.
COUNTER_POS = (615, 205)

# The room picture is drawn this far from the left edge of the window.
IMAGE_OFFSET_X = 300


# Loads one stone picture and scales it to the given height.
# The stones are tall and thin, so scaling on height keeps them from squashing.
def load_stone(path, height):
    try:
        image = pygame.image.load(path).convert_alpha()
    except (pygame.error, FileNotFoundError):
        return None  # picture missing -> the circle fallback is drawn instead
    w, h = image.get_size()
    width = max(1, round(w * height / h))  # same shape, new size
    return pygame.transform.smoothscale(image, (width, height))


# Controls everything that happens inside the teacher room.
class TeacherRoom:
    def __init__(self, screen, player, fui):
        self.screensize = screen.get_size()
        self.screen = screen
        self.next_room = None
        self.player = player
        self.fui = fui

        # Load the different images used throughout the room. ## placeholder paths
        self.room_image = u.load_image("assets/teacherRoom/tr_room_chest.png", self.screensize)
        self.room_opened = u.load_image("assets/teacherRoom/tr_room_chest_open.jpg", self.screensize)
        self.current_image = self.room_image

        self.chest_closed_image = u.load_image("assets/teacherRoom/tr_chest_closed.jpeg", self.screensize)
        self.chest_open_image = u.load_image("assets/teacherRoom/tr_chest_open.jpeg", self.screensize)

        # How much the 1024 x 572 chest picture is stretched on this screen.
        # Measured on the picture that is really drawn, NOT on the whole window,
        # because the window is wider than the picture (the chat panel is next to it).
        shown_w, shown_h = self.chest_closed_image.get_size()
        self.scale_x = shown_w / CHEST_PICTURE_SIZE[0]
        self.scale_y = shown_h / CHEST_PICTURE_SIZE[1]

        # The five stone pictures, loaded once and kept at hole size.
        icon_height = max(1, round(STONE_HEIGHT * self.scale_y))
        self.stone_icons = {}
        for name in REQUIRED_STONES:
            self.stone_icons[name] = load_stone(STONE_IMAGES[name], icon_height)

        # Fonts used in this room.
        self.font = pygame.font.Font(None, 28)
        self.slotFont = pygame.font.Font(None, 56)

        # What the player already did here is saved in player.completion,
        # so it is still done after leaving the room or loading a save.
        done = self.player.getCompletion("TeacherRoom")["all"]

        # Description memory, so the long descriptions only play the first time.
        self.room_described = "tr.described" in done
        self.chest_described = "tr.chest_described" in done

        # Game state: which stones are already inside the chest.
        self.stones_placed = [s for s in REQUIRED_STONES if "tr.placed." + s in done]   # grows with "White", "Red", ...
        self.chest_unlocked = "tr.unlocked" in done      # True the moment all five are in
        self.reward_taken = "tr.necklace" in done        # so you can't take the necklace twice
        if self.chest_unlocked:
            self.current_image = self.room_opened

        # Set to True while one click is being handled by a stone hole,
        # so the lid mask behind it does not react to the same click.
        self.hole_clicked = False

        self.reward_spot = pygame.Rect(600, 330, 56, 56)  # placeholder for the necklace

        # MASKS - the chest only, clicking it walks up to it
        self.masks = [
            u.Mask("assets/teacherRoom/tr_room_chest_mask.png", self.screensize, (0, 0), self.chest, "Chest"),
        ]

        # MASKS on the chest close up.
        # The five holes come FIRST, then the lid behind them.
        self.chest_masks = []
        for hole in STONE_HOLES:
            colour = hole["colour"]
            # colour=colour freezes the colour inside this one button,
            # without it every hole would place the last colour of the loop.
            self.chest_masks.append(
                u.Mask(hole["mask"], self.screensize, (0, 0),
                       lambda colour=colour: self.place_stone(colour),
                       colour + " stone hole")
            )

        # the lid in the close up -> clicking it tries to open the chest
        self.chest_masks.append(
            u.Mask("assets/teacherRoom/tr_cutout_1_whole_chest.png", self.screensize, (0, 0), self.try_open, "Chest lid")
        )

        self.no_masks = []
        self.current_masks = self.masks

        # BUTTONS - only the things that have no shape on screen
        self.buttons = [
            u.Button(560, 650, 140, 50, "Return", self.returnc),
        ]
        self.current_buttons = self.buttons

        self.returnr_buttons = [
            u.Button(1000, 520, 140, 50, "Return", self.returnr)]

        # No "Place stone" button any more, the holes are the buttons.
        self.chest_buttons = self.returnr_buttons

        self.reward_buttons = [
                                  u.Button(830, 600, 180, 50, "Take necklace", self.take_reward),
                              ] + self.returnr_buttons

    # ------------------------------------------------------------------
    # entering the room
    # ------------------------------------------------------------------

    # Called once, the first time the player sets foot in the lounge.
    # Describes the whole room so the player knows what can be clicked.
    def on_enter(self):
        if DEBUG_GIVE_ALL_STONES:
            self.give_debug_stones()

        if self.room_described:
            return
        self.room_described = True
        self.add("tr.described")
        self.fui.sendMessage("You", "TeacherRoom", 1)   # dark lounge, candles, old paper
        self.fui.sendMessage("You", "TeacherRoom", 2)   # table / couches / chalkboard layout
        self.fui.sendMessage("You", "TeacherRoom", 3)   # the glowing chest on the red rug

    # Testing helper: puts every stone that is not yet owned or placed in the inventory.
    def give_debug_stones(self):
        for name in REQUIRED_STONES:
            if name in self.stones_placed:
                continue  # already inside the chest
            if not self.player.has_item("Stones", name):
                self.player.add_item("Stones", name, STONE_IMAGES[name])

    # ------------------------------------------------------------------
    # chest
    # ------------------------------------------------------------------

    # Walks up to the chest and shows the right picture for the situation.
    def chest(self):
        if self.chest_unlocked:
            self.current_image = self.chest_open_image
            self.current_masks = self.no_masks
            if self.reward_taken:
                self.current_buttons = self.returnr_buttons
                self.fui.sendMessage("You", "TeacherRoom", 26)  # empty velvet and dust
            else:
                self.current_buttons = self.reward_buttons
                self.fui.sendMessage("You", "TeacherRoom", 24)  # the necklace on the velvet
        else:
            self.current_image = self.chest_closed_image
            self.current_masks = self.chest_masks
            self.current_buttons = self.chest_buttons

            # The long close up description only plays the first time.
            if not self.chest_described:
                self.chest_described = True
                self.add("tr.chest_described")
                self.fui.sendMessage("You", "TeacherRoom", 6)   # gold, carvings, scorched floor
                self.fui.sendMessage("You", "TeacherRoom", 7)   # five diamond shaped holes
                self.fui.sendMessage("You", "TeacherRoom", 8)   # five holes... five stones
            else:
                self.describe_slots()

    # Short status line about how full the lid is.
    def describe_slots(self):
        missing = len(REQUIRED_STONES) - len(self.stones_placed)
        if missing == 0:
            self.fui.sendMessage("You", "TeacherRoom", 9)       # all five are in
        else:
            self.fui.sendMessage("You", "TeacherRoom", MISSING_LINE_BASE - missing)

    # Clicking the lid itself, only works when every stone is in place.
    def try_open(self):
        # the click was meant for a stone hole, not for the lid behind it
        if self.hole_clicked:
            return
        missing = len(REQUIRED_STONES) - len(self.stones_placed)
        if missing > 0:
            # 5 missing -> 10, 4 -> 11, 3 -> 12, 2 -> 13, 1 -> 14
            self.fui.sendMessage("You", "TeacherRoom", MISSING_LINE_BASE - missing)
        else:
            self.unlock()

    # Called when the player clicks one hole. The hole knows its own colour.
    def place_stone(self, colour):
        self.hole_clicked = True

        if self.chest_unlocked:
            self.fui.sendMessage("You", "TeacherRoom", 21)      # the chest is already open
            return

        for i in range(len(REQUIRED_STONES)):
            stone = REQUIRED_STONES[i]
            if stone in self.stones_placed:
                continue  # that hole is already filled
            if self.player.has_item("Stones", stone):
                self.player.remove_item("Stones", stone)
                self.stones_placed.append(stone)
                self.add("tr.placed." + stone)
                # White = 15, Red = 16, Green = 17, Purple = 18, Yellow = 19
                self.fui.sendMessage("You", "TeacherRoom", STONE_LINE_FIRST + i)
                # The fifth stone opens the chest by itself.
                if len(self.stones_placed) == len(REQUIRED_STONES):
                    self.unlock()
                return  # one stone per click

        self.fui.sendMessage("You", "TeacherRoom", 20)          # no stone that fits

    # Everything that happens the moment the last stone goes in.
    def unlock(self):
        self.chest_unlocked = True
        self.add("tr.unlocked")
        self.current_image = self.chest_open_image
        self.current_masks = self.no_masks
        self.current_buttons = self.reward_buttons
        self.fui.sendMessage("You", "TeacherRoom", 22)          # clunk, the lid swings open
        self.fui.sendMessage("You", "TeacherRoom", 23)          # golden light spills out
        self.fui.sendMessage("You", "TeacherRoom", 24)          # the necklace on the velvet

    # Takes the necklace out of the chest and adds it to the inventory.
    def take_reward(self):
        if self.reward_taken:
            self.fui.sendMessage("You", "TeacherRoom", 26)      # the chest is empty now
            return
        self.reward_taken = True
        self.add("tr.necklace")
        # change the picture of the item ## placeholder path
        self.player.add_item("Items", "Necklace", "assets/teacherRoom/tr.necklace.png")
        lb.finishRun(self.player)   # the game is done, marks a saved run as finished on the leaderboard
        self.fui.sendMessage("You", "TeacherRoom", 25)          # still warm, the way out
        self.current_image = self.chest_open_image
        self.current_buttons = self.returnr_buttons

    # ------------------------------------------------------------------
    # navigation
    # ------------------------------------------------------------------

    # Tells the main game that the player wants to move to the corridor.
    def returnc(self):
        self.next_room = "corridor"

    # Returns from a searched area to the main teacher room.
    def returnr(self):
        if self.chest_unlocked:
            self.current_image = self.room_opened
            self.fui.sendMessage("You", "TeacherRoom", 5)       # chest open, glow fading
        else:
            self.current_image = self.room_image
            self.fui.sendMessage("You", "TeacherRoom", 4)       # chest still waits on the rug
        self.current_masks = self.masks
        self.current_buttons = self.buttons

    # ------------------------------------------------------------------
    # events and drawing
    # ------------------------------------------------------------------

    # Saves a step of this room in player.completion["TeacherRoom"]["all"].
    def add(self, event):
        self.player.addCompletion("TeacherRoom", event, "")

    # Sends mouse events to the active masks and buttons.
    def handle_event(self, event):
        self.hole_clicked = False   # new event, nothing clicked yet

        for m in self.current_masks:
            m.handle_event(event)

        for b in self.current_buttons:
            b.handle_event(event)

    # Gives back the screen position of the middle of hole number i, left to right.
    def hole_center(self, i):
        cx, cy = STONE_HOLES[i]["centre"]
        x = IMAGE_OFFSET_X + round(cx * self.scale_x)
        y = round(cy * self.scale_y)
        return (x, y)

    # Draws the stone of every hole that is already filled.
    # Empty holes are not drawn at all, the picture itself already shows them.
    def draw_stones(self):
        for i in range(len(STONE_HOLES)):
            colour = STONE_HOLES[i]["colour"]
            if colour not in self.stones_placed:
                continue

            cx, cy = self.hole_center(i)
            icon = self.stone_icons[colour]
            if icon is not None:
                # put the middle of the picture on the middle of the hole
                self.screen.blit(icon, icon.get_rect(center=(cx, cy)))
            else:
                # picture missing -> fall back to a coloured circle
                radius = round(STONE_HEIGHT * self.scale_y / 2)
                pygame.draw.circle(self.screen, STONE_COLOURS[colour], (cx, cy), radius)

    # Draws the current room, the stones, the counter and the buttons.
    def draw(self):
        # safety net, in case the main loop never calls on_enter
        if not self.room_described:
            self.on_enter()

        self.screen.blit(self.current_image, (IMAGE_OFFSET_X, 0))

        # Draw the necklace inside the open chest until the player takes it.
        if self.current_image is self.chest_open_image and not self.reward_taken:
            pygame.draw.rect(self.screen, (220, 220, 230), self.reward_spot)

        # masks get drawn first. The tr_cutout pictures are real pictures of the
        # chest, so anything drawn BEFORE them is hidden underneath.
        for m in self.current_masks:
            m.draw(self.screen)

        # The stones and the counter only exist on the closed chest screen.
        # They are drawn AFTER the masks, so they end up on top of the chest.
        if self.current_image is self.chest_closed_image:
            self.draw_stones()
            shown = str(len(self.stones_placed)) + " / " + str(len(REQUIRED_STONES))
            text = self.slotFont.render(shown, True, (0, 255, 120))
            self.screen.blit(text, COUNTER_POS)

        # Draw the buttons currently available to the player.
        for b in self.current_buttons:
            b.draw2(self.screen)
