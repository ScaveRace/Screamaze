import os
import pygame
import UI.uiElements as u

# the briefcase of the phone is the button that opens the inventory, in the bottom right corner of the game
ICON = "assets/phoneIm/apps/briefcase.png"
ICON_SIZE = 64
PADDING = 20

# items you can press in the inventory to look at them: item name -> (close-up picture, id of its text in the language files, under NewRooms)
# an item without its close-up picture yet only shows its text
ITEM_VIEWS = {
    "Small brass key": ("assets/items/small_brass_key/closeup.png", "items.brass_key"),
    "Small silver key": ("assets/items/small_silver_key/closeup.png", "items.silver_key"),
    "Marsh's diary": ("assets/items/marsh_diary/closeup.png", "items.diary"),
    "Pin": ("assets/items/pin/closeup.png", "items.pin"),
    "Biology flyer": ("assets/items/biology_flyer/closeup.png", "items.flyer"),
}
ITEM_TABLE = "NewRooms"
CLOSEUP_SIZE = (704, 396)
CLOSEUP_POS = (538, 140)

class InventoryMenu:
    def __init__(self,screen,player):
        self.screen = screen
        self.p = player
        self.open = False
        self.panel =  pygame.Rect(740,140,400,440)
        self.images = {}
        self.font = pygame.font.Font(None,36)
        self.small_font = pygame.font.Font(None, 28)

        self.icon = u.load_alpha_image(ICON, (ICON_SIZE, ICON_SIZE))
        self.openRect = self.icon.get_rect(bottomright=(screen.get_width() - PADDING, screen.get_height() - PADDING))
        self.closeButton = u.Button(870,520,140,44,"Close",self.toggle)
        self.backButton = u.Button(870,550,140,44,"Back",self.hide)
        self.say = None         # set by the front UI: sends a text to the chat
        self.closeup = None     # the picture of the item you are looking at, None when no close-up is showing

    def toggle(self):
        self.open = not self.open
        self.closeup = None

    def hide(self):
        self.closeup = None

    def rows(self):
        # (name, path, place on screen) of every item in the list, the same for drawing and pressing
        rows = []
        y = self.panel.y + 70
        for entry in self.p.inventory["Items"] + self.p.inventory["Stones"]:   # entry = {"Fuse": "assets/fuse_item.png"}
            for name, path in entry.items():  # one dict = one item
                rows.append((name, path, pygame.Rect(self.panel.x + 40, y, 320, 36)))
                y += 40
        return rows

    # pressing an item with a close-up shows its picture (when it was made already) and tells its text
    def show(self, name):
        path, textId = ITEM_VIEWS[name]
        if os.path.exists(path):
            self.closeup = u.load_alpha_image(path, CLOSEUP_SIZE)
        if self.say:
            self.say("You", ITEM_TABLE, textId)

    def handle_event(self, event):
        if self.open:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.toggle()
                return True
            if self.closeup:
                self.backButton.handle_event(event)
                return True
            self.closeButton.handle_event(event)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                for name, path, rect in self.rows():
                    if name in ITEM_VIEWS and rect.collidepoint(event.pos):
                        self.show(name)
            return True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.openRect.collidepoint(event.pos):
            self.toggle()
        return self.open

    def get_image(self, path):
        if path not in self.images:  # only load each file once
            file = path if path else ""  # unknown items have path None
            self.images[path] = u.load_alpha_image(file, (32, 32))
        return self.images[path]

    def draw(self):
        if not self.open:
            if self.openRect.collidepoint(pygame.mouse.get_pos()):    # grey behind the icon when you hover it, like the buttons
                pygame.draw.rect(self.screen, (128, 128, 128), self.openRect.inflate(8, 8), border_radius=6)
            self.screen.blit(self.icon, self.openRect)
            return

        if self.closeup:
            self.screen.blit(self.closeup, CLOSEUP_POS)
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(CLOSEUP_POS, CLOSEUP_SIZE), 1)
            self.backButton.draw2(self.screen)
            return

        pygame.draw.rect(self.screen, (0, 0, 0), self.panel)
        pygame.draw.rect(self.screen, (255, 255, 255), self.panel, 1)
        title = self.font.render("INVENTORY", True, (255, 255, 255))
        self.screen.blit(title, title.get_rect(center=(940, 175)))

        rows = self.rows()
        if not rows:  # no items yet
            empty = self.small_font.render("Nothing here yet.", True, (150, 150, 142))
            self.screen.blit(empty, empty.get_rect(center=(940, self.panel.y + 90)))

        for name, path, rect in rows:
            if name in ITEM_VIEWS and rect.collidepoint(pygame.mouse.get_pos()):    # grey behind an item you can look at, like the buttons
                pygame.draw.rect(self.screen, (60, 60, 60), rect, border_radius=4)
            self.screen.blit(self.get_image(path), rect.topleft)
            self.screen.blit(self.small_font.render(name, True, (222, 222, 214)), (rect.x + 45, rect.y + 8))

        self.closeButton.draw2(self.screen)