import pygame
import UI.uiElements as u

# items you can press in the inventory to look at them: item name -> (close-up picture, id of its text in the language files, under NewRooms)
ITEM_VIEWS = {
    "Small brass key": ("assets/items/brass_key_closeup.png", "items.brass_key"),
    "Small silver key": ("assets/items/silver_key_closeup.png", "items.silver_key"),
    "Torn diary": ("assets/items/diary_closeup.png", "items.diary"),
}
ITEM_TABLE = "NewRooms"
CLOSEUP_SIZE = (704, 396)
CLOSEUP_POS = (538, 162)

class InventoryMenu:
    def __init__(self,screen,player):
        self.screen = screen
        self.p = player
        self.open = False
        self.panel =  pygame.Rect(740,140,400,440)
        self.images = {}
        self.font = pygame.font.Font(None,36)
        self.small_font = pygame.font.Font(None, 28)
        self.say = None         # set by the front UI: sends a text to the chat
        self.closeup = None     # the item you are looking at, None when no close-up is showing

        self.openButton = u.Button(1270,20,90,36,"Inventory",self.toggle)
        self.closeButton = u.Button(870,520,140,44,"Close",self.toggle)

    def toggle(self):
        self.open = not self.open
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

    def show(self, name):
        self.closeup = name
        if self.say:
            self.say("You", ITEM_TABLE, ITEM_VIEWS[name][1])

    def handle_event(self, event):
        if self.open:
            if self.closeup:    # any click or Esc puts the close-up away
                if (event.type == pygame.MOUSEBUTTONUP and event.button == 1) or \
                        (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.closeup = None
                return True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.toggle()
                return True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                for name, path, rect in self.rows():
                    if name in ITEM_VIEWS and rect.collidepoint(event.pos):
                        self.show(name)
                        return True
            self.closeButton.handle_event(event)
            return True
        self.openButton.handle_event(event)
        return self.open

    def get_image(self, path):
        if path not in self.images:  # only load each file once
            file = path if path else ""  # unknown items have path None
            self.images[path] = u.load_alpha_image(file, (32, 32))
        return self.images[path]

    def get_closeup(self, name):
        path = ITEM_VIEWS[name][0]
        if path not in self.images:
            self.images[path] = u.load_alpha_image(path, CLOSEUP_SIZE)
        return self.images[path]

    def draw(self):
        if not self.open:
            self.openButton.draw2(self.screen)
            return

        pygame.draw.rect(self.screen, (0, 0, 0), self.panel)
        pygame.draw.rect(self.screen, (255, 255, 255), self.panel, 1)
        title = self.font.render("INVENTORY", True, (255, 255, 255))
        self.screen.blit(title, title.get_rect(center=(940, 175)))

        y = self.panel.y + 70
        rows = self.rows()

        if not rows:  # no items yet
            empty = self.small_font.render("Nothing here yet.", True, (150, 150, 142))
            self.screen.blit(empty, empty.get_rect(center=(940, y + 20)))

        for name, path, rect in rows:
            self.screen.blit(self.get_image(path), (rect.x, rect.y))
            self.screen.blit(self.small_font.render(name, True, (222, 222, 214)),
                             (rect.x + 45, rect.y + 8))

        self.closeButton.draw2(self.screen)

        if self.closeup:
            self.screen.blit(self.get_closeup(self.closeup), CLOSEUP_POS)
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(CLOSEUP_POS, CLOSEUP_SIZE), 1)
