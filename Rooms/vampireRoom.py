import pygame
import UI.uiElements as u

pygame.init()
pygame.mixer.init()

class VampireRoom:
    def __init__(self, screen, player,fui):
        self.screen = screen
        self.next_room = None
        self.player = player
        self.fui = fui

        self.bg_closed = u.load_image("assets/vampire/Room2015_1_win_clo.png", screen.get_size(), fallback=(35, 8, 18))
        self.bg_open = u.load_image("assets/vampire/Room2015_1_win_op.png", screen.get_size(), fallback=(120, 100, 60))
        self.cabinet_img = u.load_image("assets/vampire/vp.cabinet.closed.png", screen.get_size(), fallback=(120, 100, 60))
        self.cabinet_drawer_img = u.load_image("assets/vampire/cabinet_drawer_open.png", screen.get_size(), fallback=(120, 100, 60))
        self.fusebox_closed_img = u.load_image("assets/vampire/fuse_box.png", screen.get_size(), fallback=(20, 20, 20))
        self.fusebox_open_img = u.load_image("assets/vampire/fuse_box2.png", screen.get_size(), fallback=(20, 20, 20))
        self.fuse_on_box_img = u.load_image("assets/vampire/fuseonbox.png", screen.get_size(), fallback=(20, 20, 20))
        self.image = self.bg_closed

        self.font = pygame.font.Font(None, 28)
        self.titleFont = pygame.font.Font(None, 40)
        self.dialogue = [
            "Vampire > Ah... a warm little visitor, wandering into my crypt.",
            "Vampire > Those shutters have kept the sun out for centuries.",
            "Vampire > You'll never get them open without power to that old panel."
        ]
        self.line = 0
        self.task_started = False
        self.task_done = False
        self.inventory = []
        self.fuse_found = False
        self.fuse_inserted = False
        self.stone_collected = False
        self.state = "room"

        self.chatbox = u.Chatbox(10, 80, 600, 150, self.font)

        self.masks = [
            u.Mask("assets/vampire/masks/vampire.png", self.screen.get_size(), (0, 0), self.talk),
            u.Mask("assets/vampire/masks/cabinet.png", self.screen.get_size(), (0, 0), self.search_corner),
            u.Mask("assets/vampire/masks/fusebox.png", self.screen.get_size(), (0, 0), self.open_fusebox_closeup),
            u.Mask("assets/stones/red.png", self.screen.get_size(), (780, 170), self.collect_stone)
        ]

        self.room_buttons = [
            u.Button(780, 660, 220, 50, "Leave Room", self.leave)
        ]

        self.fusebox_closed_mask = [
            u.Mask("assets/vampire/masks/fusebox_closed.png", self.screen.get_size(), (0, 0), self.open_fusebox_door)
        ]
        self.fusebox_closed_buttons = [
            u.Button(870, 650, 150, 50, "Close", self.close_fusebox)
        ]

        self.fusebox_open_mask = [
            u.Mask("assets/vampire/masks/red_button.png", self.screen.get_size(), (0, 0), self.press_reset)
        ]
        self.fusebox_open_buttons = [
            u.Button(560, 600, 150, 50, "Insert Fuse", self.insert_fuse),
            u.Button(900, 600, 150, 50, "Close", self.close_fusebox)
        ]

        self.cabinet_closed_mask = [
            u.Mask("assets/vampire/masks/cabinet_drawer.png", self.screen.get_size(), (0, 0), self.open_drawer)
        ]
        self.cabinet_closed_buttons = [
            u.Button(900, 600, 150, 50, "Close", self.close_cabinet)
        ]

        self.fuse_mask = [
            u.Mask("assets/vampire/masks/fuse.png", self.screen.get_size(), (0, 0), self.collect_fuse)
        ]
        self.drawer_buttons = [
            u.Button(900, 600, 150, 50, "Close", self.close_drawer)
        ]

    def talk(self):
        if self.line < len(self.dialogue):
            self.chatbox.say(self.dialogue[self.line])
            self.line += 1
            if self.line == len(self.dialogue):
                self.task_started = True
        elif not self.task_done:
            self.chatbox.say("Vampire > That panel is your only way to open those shutters.")
        else:
            self.chatbox.say("Vampire > ...")

    def search_corner(self):
        self.state = "cabinet"

    def open_drawer(self):
        self.state = "drawer open"

    def close_cabinet(self):
        self.state = "room"

    def close_drawer(self):
        self.state = "cabinet"

    def collect_fuse(self):
        if self.fuse_found:
            return
        self.fuse_found = True
        self.inventory.append("fuse")
        self.chatbox.say("You > Found a spare fuse inside the cabinet.")

    def open_fusebox_closeup(self):
        self.state = "fusebox_closed"

    def open_fusebox_door(self):
        self.state = "fusebox_open"

    def close_fusebox(self):
        self.state = "room"
        if self.task_done:
            self.image = self.bg_open

    def insert_fuse(self):
        if self.fuse_inserted:
            return
        if "fuse" not in self.inventory:
            self.chatbox.say("You > I need to find a fuse first.")
            return
        self.inventory.remove("fuse")
        self.fuse_inserted = True
        self.chatbox.say("You > Slotted the last fuse into place. All three are lit now.")

    def press_reset(self):
        if self.task_done:
            return
        if not self.fuse_inserted:
            self.chatbox.say("You > All three fuses need to be in before I hit this.")
            return
        self.task_done = True
        self.chatbox.say("You > *click* — the panel hums back to life.")
        self.chatbox.say("You > Something outside screamed. I should go look.")

    def collect_stone(self):
        if not self.task_done or self.stone_collected:
            return
        self.stone_collected = True
        self.inventory.append("red_stone")
        self.chatbox.say("You > A red stone... still cold.")

    def leave(self):
        self.next_room = "corridor"

    def handle_event(self, event):
        if self.state == "room":
            if not self.task_done:
                self.masks[0].handle_event(event)
            self.masks[1].handle_event(event)
            self.masks[2].handle_event(event)
            if self.task_done and not self.stone_collected:
                self.masks[3].handle_event(event)
            for button in self.room_buttons:
                button.handle_event(event)

        elif self.state == "fusebox_closed":
            for mask in self.fusebox_closed_mask:
                mask.handle_event(event)
            for button in self.fusebox_closed_buttons:
                button.handle_event(event)

        elif self.state == "fusebox_open":
            for mask in self.fusebox_open_mask:
                mask.handle_event(event)
            for button in self.fusebox_open_buttons:
                button.handle_event(event)

        elif self.state == "cabinet":
            for mask in self.cabinet_closed_mask:
                mask.handle_event(event)
            for button in self.cabinet_closed_buttons:
                button.handle_event(event)

        elif self.state == "drawer open":
            if not self.fuse_found:
                for mask in self.fuse_mask:
                    mask.handle_event(event)
            for button in self.drawer_buttons:
                button.handle_event(event)

    def draw(self):
        if self.state == "room":
            self.screen.blit(self.image, (300, 0))
            title = self.titleFont.render("The Vampire's Crypt", True, (200, 30, 40))
            self.screen.blit(title, (60, 40))

            if not self.task_done:
                self.masks[0].draw(self.screen)
            if not self.fuse_found:
                self.masks[1].draw(self.screen)
            self.masks[2].draw(self.screen)

            if self.task_done and not self.stone_collected:
                self.masks[3].draw(self.screen)

            for button in self.room_buttons:
                button.draw2(self.screen)

        elif self.state == "fusebox_closed":
            self.screen.blit(self.fusebox_closed_img, (300, 0))
            for mask in self.fusebox_closed_mask:
                mask.draw(self.screen)
            for button in self.fusebox_closed_buttons:
                button.draw2(self.screen)

        elif self.state == "fusebox_open":
            self.screen.blit(self.fusebox_open_img, (300, 0))
            if self.fuse_inserted:
                self.screen.blit(self.fuse_on_box_img, (300, 0))
            for mask in self.fusebox_open_mask:
                mask.draw(self.screen)
            for button in self.fusebox_open_buttons:
                button.draw2(self.screen)

        elif self.state == "cabinet":
            self.screen.blit(self.cabinet_img, (300, 0))
            for mask in self.cabinet_closed_mask:
                mask.draw(self.screen)
            for button in self.cabinet_closed_buttons:
                button.draw2(self.screen)

        elif self.state == "drawer open":
            self.screen.blit(self.cabinet_drawer_img, (300, 0))
            if not self.fuse_found:
                for mask in self.fuse_mask:
                    mask.draw(self.screen)
            for button in self.drawer_buttons:
                button.draw2(self.screen)
