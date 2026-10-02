import pygame
import UI.uiElements as u

class InventoryMenu:
    def __init__(self,screen,player):
        self.screen = screen
        self.p = player
        self.open = False
        self.panel =  pygame.Rect(440,140,400,440)
        self.images = {}
        self.font = pygame.font.Font(None,36)
        self.small_font = pygame.font.Font(None, 28)

        self.openButton = u.Button(1270,20,90,36,"Inventory",self.toggle)
        self.closeButton = u.Button(570,520,140,44,"Close",self.toggle)

    def toggle(self):
        self.open = not self.open

    def handle_event(self, event):
        if self.open:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.toggle()
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

    def draw(self):
        if not self.open:
            self.openButton.draw2(self.screen)
            return

        pygame.draw.rect(self.screen, (0, 0, 0), self.panel)
        pygame.draw.rect(self.screen, (255, 255, 255), self.panel, 1)
        title = self.font.render("INVENTORY", True, (255, 255, 255))
        self.screen.blit(title, title.get_rect(center=(640, 175)))

        y = self.panel.y + 70
        items = self.p.inventory["Items"]

        if not items:  # no items yet
            empty = self.small_font.render("Nothing here yet.", True, (150, 150, 142))
            self.screen.blit(empty, empty.get_rect(center=(640, y + 20)))

        for entry in items:  # entry = {"Fuse": "assets/fuse_item.png"}
            for name, path in entry.items():  # one dict = one item
                self.screen.blit(self.get_image(path), (self.panel.x + 40, y))
                self.screen.blit(self.small_font.render(name, True, (222, 222, 214)),
                                 (self.panel.x + 85, y + 8))
                y += 40

        self.closeButton.draw2(self.screen)