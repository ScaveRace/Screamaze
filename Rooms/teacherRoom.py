import pygame
import UI.uiElements as u
from player import Player
import UI.frontUI as Fui


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

# Where the five stone slots are drawn on the chest close up.
SLOT_ORIGIN = (520, 430)   # centre of the first (left) slot
SLOT_SIZE = 70             # height of one stone, the width follows the picture
SLOT_GAP = 26              # space between two slots

# Where the "3 / 5" counter is drawn on the chest close up.
COUNTER_POS = (615, 205)


# Loads one stone picture and scales it to the height of a slot.
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

        # Load the different images used throughout the room. ## placeholder paths
        self.room_image = u.load_image("assets/teacherRoom/tr.room.chest.png", self.screensize)
        self.room_opened = u.load_image("assets/teacherRoom/tr.room.chest.open.png", self.screensize)
        self.current_image = self.room_image

        self.chest_closed_image = u.load_image("assets/teacherRoom/tr.chest.closed.png", self.screensize)
        self.chest_open_image = u.load_image("assets/teacherRoom/tr.chest.open.png", self.screensize)
        self.chest_empty_image = u.load_image("assets/teacherRoom/tr.chest.empty.png", self.screensize)

        # The five stone pictures, loaded once and kept at slot size.
        self.stone_icons = {}
        for name in REQUIRED_STONES:
            self.stone_icons[name] = load_stone(STONE_IMAGES[name], SLOT_SIZE)

        # Fonts and the dialogue box used for messages.
        self.font = pygame.font.Font(None, 28)
        self.chatbox = u.Chatbox(10, 10, 500, 90, self.font)
        self.slotFont = pygame.font.Font(None, 56)

        # Game state: which stones are already inside the chest.
        self.stones_placed = []          # grows with "White", "Red", ...
        self.chest_unlocked = False      # True the moment all five are in
        self.reward_taken = False        # so you can't take the reward twice

        self.reward_spot = pygame.Rect(600, 330, 56, 56)  # placeholder for the thing inside

        # MASKS - the chest only, clicking it walks up to it
        self.masks = [
            u.Mask("assets/teacherRoom/tr_room_chest.png", self.screensize, (0, 0), self.chest, "Chest"),
        ]

        # the lid in the close up -> clicking it tries to open the chest
        self.chest_masks = [
            u.Mask("assets/teacherRoom/tr_chest_lid.png", self.screensize, (0, 0), self.try_open, "Chest lid"),
        ]

        self.no_masks = []
        self.current_masks = self.masks

        # BUTTONS - only the things that have no shape on screen
        self.buttons = [
            u.Button(560, 650, 140, 50, "Return", self.returnc),
        ]
        self.current_buttons = self.buttons

        self.returnr_buttons = [
            u.Button(1000, 520, 140, 50, "Return", self.returnr)]

        self.chest_buttons = [
                                 u.Button(550, 600, 180, 50, "Place stone", self.place_stone),
                             ] + self.returnr_buttons

        self.reward_buttons = [
                                  u.Button(830, 600, 180, 50, "Take reward", self.take_reward),
                              ] + self.returnr_buttons

    # ------------------------------------------------------------------
    # chest
    # ------------------------------------------------------------------

    # Walks up to the chest and shows the right picture for the situation.
    def chest(self):
        if self.chest_unlocked:
            if self.reward_taken:
                self.current_image = self.chest_empty_image
                self.current_masks = self.no_masks
                self.current_buttons = self.returnr_buttons
                self.chatbox.say("You > The chest is empty now")
            else:
                self.current_image = self.chest_open_image
                self.current_masks = self.no_masks
                self.current_buttons = self.reward_buttons
                self.chatbox.say("You > There is something lying inside")
        else:
            self.current_image = self.chest_closed_image
            self.current_masks = self.chest_masks
            self.current_buttons = self.chest_buttons
            self.chatbox.say("You > Five holes in the lid... five stones")

    # Clicking the lid itself, only works when every stone is in place.
    def try_open(self):
        if len(self.stones_placed) < len(REQUIRED_STONES):
            missing = len(REQUIRED_STONES) - len(self.stones_placed)
            self.chatbox.say("You > It will not budge, " + str(missing) + " stones are still missing")
        else:
            self.unlock()

    # Puts one stone from the inventory into the next free hole.
    def place_stone(self):
        if self.chest_unlocked:
            self.chatbox.say("You > The chest is already open")
            return

        for stone in REQUIRED_STONES:
            if stone in self.stones_placed:
                continue  # that hole is already filled
            if self.player.has_item("Stones", stone):
                self.player.remove_item("Stones", stone)
                self.stones_placed.append(stone)
                self.chatbox.say("You > The " + stone.lower() + " stone clicks into the lid")
                # The fifth stone opens the chest by itself.
                if len(self.stones_placed) == len(REQUIRED_STONES):
                    self.unlock()
                return  # one stone per click

        self.chatbox.say("You > I have no stone that fits, search the other rooms")

    # Everything that happens the moment the last stone goes in.
    def unlock(self):
        self.chest_unlocked = True
        self.current_image = self.chest_open_image
        self.current_masks = self.no_masks
        self.current_buttons = self.reward_buttons
        self.chatbox.say("You > 'clunk' the lid swings open")

    # Takes whatever is inside and adds it to the inventory.
    def take_reward(self):
        if self.reward_taken:
            self.chatbox.say("You > The chest is empty now")
            return
        self.reward_taken = True
        # change the picture of the item ## placeholder path
        self.player.add_item("Items", "Key", "assets/teacherRoom/tr.key.png")
        self.chatbox.say("You > A rusty key... this has to be the way out")
        self.current_image = self.chest_empty_image
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
        else:
            self.current_image = self.room_image
        self.current_masks = self.masks
        self.current_buttons = self.buttons

    # ------------------------------------------------------------------
    # events and drawing
    # ------------------------------------------------------------------

    # Sends mouse events to the active masks and buttons.
    def handle_event(self, event):
        for m in self.current_masks:
            m.handle_event(event)

        for b in self.current_buttons:
            b.handle_event(event)

    # Gives back the middle point of hole number i, left to right.
    def slot_center(self, i):
        x0, y0 = SLOT_ORIGIN
        step = SLOT_SIZE + SLOT_GAP  # one slot plus one gap
        return (x0 + i * step, y0)

    # Draws the five holes, filled ones get their stone picture.
    def draw_slots(self):
        for i in range(len(REQUIRED_STONES)):
            name = REQUIRED_STONES[i]
            cx, cy = self.slot_center(i)

            if name in self.stones_placed:
                icon = self.stone_icons[name]
                if icon is not None:
                    # put the middle of the picture on the middle of the hole
                    rect = icon.get_rect(center=(cx, cy))
                    self.screen.blit(icon, rect)
                else:
                    # picture missing -> fall back to a coloured circle
                    pygame.draw.circle(self.screen, STONE_COLOURS[name], (cx, cy), SLOT_SIZE // 2)
            else:
                # empty hole, just a dark ring
                pygame.draw.circle(self.screen, (60, 50, 40), (cx, cy), SLOT_SIZE // 2, 3)

    # Draws the current room, the slots, the counter, buttons and chatbox.
    def draw(self):
        self.screen.blit(self.current_image, (300, 0))

        # The holes and the counter only exist on the closed chest screen.
        if self.current_image is self.chest_closed_image:
            self.draw_slots()
            shown = str(len(self.stones_placed)) + " / " + str(len(REQUIRED_STONES))
            text = self.slotFont.render(shown, True, (0, 255, 120))
            self.screen.blit(text, COUNTER_POS)

        # Draw the reward inside the open chest until the player takes it.
        if self.current_image is self.chest_open_image and not self.reward_taken:
            pygame.draw.rect(self.screen, (220, 200, 120), self.reward_spot)

        # masks now get drawn,
        for m in self.current_masks:
            m.draw(self.screen)

        # Draw the buttons currently available to the player.
        for b in self.current_buttons:
            b.draw2(self.screen)

        # Draw the dialogue box last so it appears on top of the room.
        self.chatbox.draw(self.screen)