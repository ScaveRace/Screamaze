import pygame
import UI.uiElements as u

pygame.init()
pygame.mixer.init()


class vampireRoom:
    def __init__(self, screen):
        self.screen = screen
        self.next_room = None

        #both bg before and after
        self.bg_closed = u.load_image("assets/Room2015_1_win_clo.png", screen.get_size(), fallback=(35, 8, 18))
        self.bg_open = u.load_image("assets/Room2015_1_win_op.png", screen.get_size(), fallback=(120, 100, 60))
        self.image = self.bg_closed

        #Fuse box open and closed
        self.fusebox_closed_img = u.load_image("assets/fuse_box.png", screen.get_size(), fallback=(20, 20, 20))
        self.fusebox_open_img = u.load_image("assets/fuse_box2.png", screen.get_size(), fallback=(20, 20, 20))


        self.fuse_icon = u.load_image("assets/fuse_item.png", (56, 56), fallback=(120, 90, 40))

        self.font = pygame.font.Font(None, 28)
        self.titleFont = pygame.font.Font(None, 40)

        self.dialogue = [
            "Vampire > Ah... a warm little visitor, wandering into my crypt.",
            "Vampire > Those shutters have kept the sun out for centuries.",
            "Vampire > You'll never get them open without power to that old panel.",
        ]
        self.line = 0
        self.task_started = False
        self.task_done = False   # power restored / vampire dead


        self.inventory = []
        self.fuse_found = False      # picked up from the corner yet?
        self.fuse_inserted = False   # slotted into the box yet?


        self.fuse_spot = pygame.Rect(100, 580, 56, 56)
        self.stone_spot = pygame.Rect(750, 150, 44, 44)
        self.stone_collected = False


        self.state = "room"

        self.chatbox = u.Chatbox(50, 20, 300, 200, self.font)

        self.room_buttons = [
            u.Button(780, 420, 220, 50, "Talk to Vampire", self.talk),
            u.Button(780, 480, 220, 50, "Search Corner", self.search_corner),
            u.Button(780, 540, 220, 50, "Inspect Fuse Box", self.open_fusebox_closeup),
            u.Button(780, 600, 220, 50, "Collect Stone", self.collect_stone),
            u.Button(780, 660, 220, 50, "Leave Room", self.leave),
        ]

        self.fusebox_closed_buttons = [
            u.Button(700, 600, 150, 50, "Open", self.open_fusebox_door),
            u.Button(870, 650, 150, 50, "Close", self.close_fusebox),
        ]

        self.fusebox_open_buttons = [
            u.Button(560, 600, 150, 50, "Insert Fuse", self.insert_fuse),
            u.Button(730, 600, 150, 50, "Press Button", self.press_reset),
            u.Button(900, 600, 150, 50, "Close", self.close_fusebox),
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
            self.chatbox.say("...")



    def search_corner(self):
        if not self.fuse_found:
            self.fuse_found = True
            self.inventory.append("fuse")
            self.chatbox.say("You > Found a spare fuse tucked in the corner.")
        else:
            self.chatbox.say("You > Nothing else here.")



    def open_fusebox_closeup(self):
        self.state = "fusebox_closed"

    def open_fusebox_door(self):
        self.state = "fusebox_open"

    def close_fusebox(self):
        self.state = "room"
        if self.task_done and self.image is not self.bg_open:
            #here the room bg change with the dead vam
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


    # stone pickup

    def collect_stone(self):
        if not self.task_done:
            self.chatbox.say("You > There's nothing here yet.")
            return
        if self.stone_collected:
            self.chatbox.say("You > Already got it.")
            return

        self.stone_collected = True
        self.inventory.append("red_stone")
        self.chatbox.say("You > A red stone... still cold.")


        # from player import newPlayer
        # newPlayer.addToStone("vampire_stone")



    def leave(self):
        self.next_room = "corridor"  # always allowed — task or no task



    def handle_event(self, event):
        if self.state == "fusebox_closed":
            for b in self.fusebox_closed_buttons:
                b.handle_event(event)
            return

        if self.state == "fusebox_open":
            for b in self.fusebox_open_buttons:
                b.handle_event(event)
            return

        # "room"
        for b in self.room_buttons:
            b.handle_event(event)

    def draw(self):
        if self.state == "fusebox_closed":
            self.screen.blit(self.fusebox_closed_img, (0, 0))
            for b in self.fusebox_closed_buttons:
                b.draw2(self.screen)

        elif self.state == "fusebox_open":
            self.screen.blit(self.fusebox_open_img, (0, 0))
            for b in self.fusebox_open_buttons:
                b.draw2(self.screen)

        else:  # "room"
            self.screen.blit(self.image, (0, 0))
            title = self.titleFont.render("The Vampire's Crypt", True, (200, 30, 40))
            self.screen.blit(title, (60, 40))

            if not self.fuse_found:
                self.screen.blit(self.fuse_icon, (self.fuse_spot.x, self.fuse_spot.y))

            if self.task_done and not self.stone_collected:
                # placeholder redstone
                pygame.draw.circle(self.screen, (180, 20, 20), self.stone_spot.center, self.stone_spot.w // 2)

            for b in self.room_buttons:
                b.draw2(self.screen)

        self.chatbox.draw(self.screen)