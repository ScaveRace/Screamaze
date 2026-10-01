import pygame
import UI.uiElements as u
import math
pygame.init()
pygame.mixer.init()


class VampireRoom:
    def __init__(self, screen,player):
        self.screen = screen
        self.next_room = None

        #both bg before and after the vampire is dead
        self.bg_closed = u.load_image("assets/Room2015_1_win_clo.png", screen.get_size(), fallback=(35, 8, 18))
        self.bg_open = u.load_image("assets/Room2015_1_win_op.png", screen.get_size(), fallback=(120, 100, 60))
        self.image = self.bg_closed

        #Fuse box open and closed
        self.fusebox_closed_img = u.load_image("assets/fuse_box.png", screen.get_size(), fallback=(20, 20, 20))
        self.fusebox_open_img = u.load_image("assets/fuse_box2.png", screen.get_size(), fallback=(20, 20, 20))

        #this is the item (fause that we find in the room)
        self.cabinet_buttons = [
            u.Button(780, 660, 220, 50, "Go back", self.leave_image),
            u.Button(560, 300, 180, 50, "Pick the lock", self.start_lockpick),
        ]

        self.lockpick_buttons = [
            u.Button(780, 660, 220, 50, "Back to cabinet", self.back_to_cabinet)
        ]

        self.lock_targets = [40, 155, 285]  # Target angle for each ring
        self.lock_speeds = [120, 145, 170]  # Degrees per second
        self.lock_tolerance = 25  # How close counts as a hit
        self.lock_progress = 0
        self.lock_stage_started = 0
        self.lock_solved = False

        self.dialogue = [
            "Vampire > Ah... a warm little visitor, wandering into my crypt.",
            "Vampire > Those shutters have kept the sun out for centuries.",
            "Vampire > You'll never get them open without power to that old panel.",
        ]
        self.line = 0
        self.task_started = False
        self.task_done = False

        # this tracks the players inventory within the room
        self.inventory = []
        self.fuse_found = False
        self.fuse_inserted = False


        self.fuse_spot = pygame.Rect(100, 580, 56, 56)
        self.stone_spot = pygame.Rect(750, 150, 44, 44)
        self.stone_collected = False


        self.state = "room"

        self.chatbox = u.Chatbox(10, 540, 600, 150, self.fontD)

        self.room_buttons = [
            u.Button(780, 120, 220, 50, "Talk to Vampire", self.talk),
            u.Button(150, 500, 220, 50, "Inspect cabinet", self.search_corner),
            u.Button(1000, 460, 220, 50, "Inspect Fuse Box", self.open_fusebox_closeup),
            u.Button(780, 660, 220, 50, "Leave Room", self.leave),
        ]
        self.button1 =  u.Button(780, 170, 220, 50, "Collect Stone", self.collect_stone)

        self.fusebox_closed_buttons = [
            u.Button(700, 600, 150, 50, "Open", self.open_fusebox_door),
            u.Button(870, 650, 150, 50, "Close", self.close_fusebox),
        ]

        self.fusebox_open_buttons = [
            u.Button(560, 600, 150, 50, "Insert Fuse", self.insert_fuse),
            u.Button(730, 600, 150, 50, "Press Button", self.press_reset),
            u.Button(900, 600, 150, 50, "Close", self.close_fusebox),
        ]
        self.cabinet_buttons = [
            u.Button(780, 660, 220, 50, "Go back", self.leave_image),
            u.Button(560,300,150,50, "open drawer",self.open_drawer)

        ]

#we cannot type to the chatbox yet, but it exists and we can see comments after every button is pressed
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
        self.state = "cabinet"



        # if not self.fuse_found:
        #     self.fuse_found = True
        #     self.inventory.append("fuse")
        #     self.chatbox.say("You > Found a spare fuse tucked in the corner.")




    def open_fusebox_closeup(self):
        self.state = "fusebox_closed"

    def open_fusebox_door(self):
        self.state = "fusebox_open"

    def close_fusebox(self):
        self.state = "room"
        if self.task_done and self.image is not self.bg_open:
            #here the room bg change with the dead vam
            self.image = self.bg_open
    #this will be edited in the next version to show when the fuse is actually inserted instead of the messages
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
        self.room_buttons.append(self.button1)

        self.chatbox.say("You > *click* — the panel hums back to life.")
        self.chatbox.say("You > Something outside screamed. I should go look.")

    def leave_image(self):
        print("hi")
    # stone pickup

    def collect_stone(self):

        self.stone_collected = True
        self.room_buttons.pop()
        self.inventory.append("red_stone")
        self.chatbox.say("You > A red stone... still cold.")

    def start_lockpick(self):
        if self.lock_solved:
            self.state = "open drawer"
            return

        self.lock_progress = 0
        self.lock_stage_started = pygame.time.get_ticks()
        self.state = "lockpick"

    def back_to_cabinet(self):
        self.state = "cabinet"

    def current_lock_angle(self, now=None):
        if now is None:
            now = pygame.time.get_ticks()

        elapsed_seconds = (now - self.lock_stage_started) / 1000
        speed = self.lock_speeds[self.lock_progress]
        return (elapsed_seconds * speed) % 360

    def try_lockpick(self):
        now = pygame.time.get_ticks()
        angle = self.current_lock_angle(now)
        target = self.lock_targets[self.lock_progress]

        difference = abs((angle - target + 180) % 360 - 180)

        if difference <= self.lock_tolerance:
            self.lock_progress += 1

            if self.lock_progress == len(self.lock_targets):
                self.lock_solved = True
                self.state = "open drawer"
                self.chatbox.say("You > Click! The drawer opens.")
            else:
                self.lock_stage_started = now
                self.chatbox.say(
                    f"You > Click! {self.lock_progress} of 3 pins set."
                )
        else:
            self.lock_progress = 0
            self.lock_stage_started = now
            self.chatbox.say("You > The pick slips. Try the sequence again.")

    def handle_event(self, event):
        if self.state == "lockpick":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.try_lockpick()
                elif event.key == pygame.K_ESCAPE:
                    self.back_to_cabinet()

            for button in self.lockpick_buttons:
                button.handle_event(event)
            return

        if self.state == "fusebox_closed":
            buttons = self.fusebox_closed_buttons
        elif self.state == "fusebox_open":
            buttons = self.fusebox_open_buttons
        elif self.state == "cabinet":
            buttons = self.cabinet_buttons
        elif self.state == "open drawer":
            buttons = self.cabinet_buttons[:1]  # Go back
        elif self.state == "room":
            buttons = self._visible_room_buttons()
        else:
            buttons = []

        for button in buttons:
            button.handle_event(event)

    def draw(self):
        if self.state == "fusebox_closed":
            self.screen.blit(self.fusebox_closed_img, (0, 0))
            for button in self.fusebox_closed_buttons:
                button.draw2(self.screen)

        elif self.state == "fusebox_open":
            self.screen.blit(self.fusebox_open_img, (0, 0))
            for button in self.fusebox_open_buttons:
                button.draw2(self.screen)

        elif self.state == "cabinet":
            self.screen.blit(self.cabinet, (0, 0))
            for button in self.cabinet_buttons:
                button.draw2(self.screen)

        elif self.state == "lockpick":
            self.screen.blit(self.cabinet, (0, 0))

            center_x = self.screen.get_width() // 2
            center_y = self.screen.get_height() // 2 - 40
            radii = [65, 115, 165]

            title = self.titleFont.render("Pick the lock", True, (255, 255, 255))
            self.screen.blit(title, title.get_rect(center=(center_x, 55)))

            instructions = self.font.render(
                "Press SPACE when the pointer reaches the gold mark",
                True,
                (255, 255, 255),
            )
            self.screen.blit(instructions, instructions.get_rect(center=(center_x, 95)))

            for i, radius in enumerate(radii):
                if i < self.lock_progress:
                    color = (70, 210, 100)  # Completed ring
                elif i == self.lock_progress:
                    color = (240, 190, 50)  # Active ring
                else:
                    color = (150, 150, 150)  # Rings still to come

                pygame.draw.circle(
                    self.screen, color, (center_x, center_y), radius, 5
                )

                target_angle = math.radians(self.lock_targets[i])
                target_x = center_x + int(math.cos(target_angle) * radius)
                target_y = center_y + int(math.sin(target_angle) * radius)
                pygame.draw.circle(self.screen, color, (target_x, target_y), 10)

            angle = math.radians(self.current_lock_angle())
            active_radius = radii[self.lock_progress]
            pointer_x = center_x + int(math.cos(angle) * active_radius)
            pointer_y = center_y + int(math.sin(angle) * active_radius)

            pygame.draw.line(
                self.screen,
                (255, 255, 255),
                (center_x, center_y),
                (pointer_x, pointer_y),
                5,
            )
            pygame.draw.circle(
                self.screen, (255, 255, 255), (pointer_x, pointer_y), 8
            )

            for button in self.lockpick_buttons:
                button.draw2(self.screen)

        elif self.state == "open drawer":
            self.screen.blit(self.cabinet_open, (0, 0))
            self.cabinet_buttons[0].draw2(self.screen)

        else:  # room
            self.screen.blit(self.image, (0, 0))
            title = self.titleFont.render(
                "The Vampire's Crypt", True, (200, 30, 40)
            )
            self.screen.blit(title, (60, 40))

            if self.task_done and not self.stone_collected:
                pygame.draw.circle(
                    self.screen,
                    (180, 20, 20),
                    self.stone_spot.center,
                    self.stone_spot.w // 2,
                )

            for button in self._visible_room_buttons():
                button.draw2(self.screen)

        self.chatbox.draw(self.screen)