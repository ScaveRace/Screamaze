import pygame
import UI.uiElements as u

pygame.init()
pygame.mixer.init()

# The correct 4-digit code for the cabinet.
CABINET_CODE = "4537"   ## a string to avoid strange behaviour

# Position where the entered code will be displayed on the cabinet keypad.
# where the typed digits get drawn on top of gr.cabinet.homework.png -> tune to your art
CODE_DISPLAY_POS = (615, 205)

# keypad grid -> tune these three numbers to your art
KEYPAD_ORIGIN = (500, 300)   # top left corner of the "1" key
KEYPAD_SIZE = 70             # width and height of one key
KEYPAD_GAP = 10              # space between keys


# Controls everything that happens inside the ghost classroom.
class GhostRoom:
    def __init__(self, screen):
        self.screensize = screen.get_size()
        self.screen = screen
        self.next_room = None

        # Load the different images used throughout the room.
        self.room_image = u.load_image("assets/gr.room.teacher.jpg", self.screensize)
        self.room_empty = u.load_image("assets/gr.ghostRoom.no.teacher.png", self.screensize)
        self.current_image = self.room_image

        self.teacher_image = u.load_image("assets/gr.teacher.png", self.screensize)
        self.no_teacher_image = u.load_image("assets/gr.bureau.no.teacher.png", self.screensize)

        self.whiteboard_image = u.load_image("assets/gr.whiteboard.4537.png", self.screensize)

        self.cabinet_locked_image = u.load_image("assets/gr.cabinet.homework.png", self.screensize)
        self.cabinet_open_image = u.load_image("assets/gr.cabinet.open.keypad.png", self.screensize)

        # Fonts and the dialogue box used for messages.
        self.font = pygame.font.Font(None, 28)
        self.chatbox = u.Chatbox(10,10,500, 90,self.font) #change width and height of chatbox
        self.codeFont = pygame.font.Font(None, 56)

        # Dialogue shown when the player first talks to the ghost.
        self.dialogue = [
            "Ghost > Ohh a student has finally come to class.",
            "Ghost > I have been waiting for the homework since I died.",
            "Ghost > Only by handing in your homework can you leave.",
        ]
        self.line_count = 0

        # Game state: inventory and whether important objects/tasks are completed.
        self.inventory = [] ### global player inventory will be used later
        self.homework_taken = False #so you can't take the homework
        self.homework_spot = pygame.Rect(600, 400, 56, 56)

        self.task_done = False #memory for has the homework been handed in

        self.stone_collected = False
        self.stone_spot = pygame.Rect(750, 400, 44, 44) # position stone on empty desk

        # Cabinet/keypad state.
        self.cabinet_unlocked = False
        self.code_entry = "" #string that grows as you type
        self.keypad_open  = False

        # Each group of buttons is used in a different part of the room.
        self.buttons = [
            u.Button(930, 350, 140, 50, "Search", self.teacher),
            u.Button(580, 50, 140, 50, "Search", self.whiteboard),
            u.Button(140, 500, 140, 50, "Search", self.cabinet),
            u.Button(560, 650, 140, 50, "Return", self.returnc),
        ]
        self.current_buttons = self.buttons
        self.returnr_buttons = [
            u.Button(1000, 520, 140, 50, "Return", self.returnr)]
        self.teacher_buttons = [
             u.Button(830, 600, 140, 50, "Talk", self.talk),
             u.Button(830, 660, 140, 50, "Give", self.give_homework),
                               ] + self.returnr_buttons
        self.cabinet_buttons = [
            u.Button(550 ,600, 180, 50, "Take Homework", self.take_homework),
        ] + self.returnr_buttons
        self.stone_buttons = [
            u.Button(830,600,180,50, "Take stone", self.collect_stone)
        ] + self.returnr_buttons
        self.cabinet_locked_buttons = [
            u.Button(550,600,180,50,"Enter Code",self.open_keypad)
        ] + self.returnr_buttons
        self.keypad_buttons = self.build_keypad()


    def build_keypad(self):
        keys = []
        labels = ["1", "2", "3",
                  "4", "5", "6",
                  "7", "8", "9",
                  "C", "0", "E"]
        x0, y0 = KEYPAD_ORIGIN
        step = KEYPAD_SIZE + KEYPAD_GAP # one key plus one gap

        for i in range(len(labels)):
            label = labels[i]
            column = i % 3  #remainder -> 0,1,2, 0,1,2, ... left to right
            row = i // 3  #whole division -> 0,0,0, 1,1,1, ... top to bottom
            x = x0 + column * step
            y = y0 + row * step

            if label == "C":
                action = self.clear_code
            elif label == "E":
                action = self.check_code
            else:
                # d=label freezes this label, otherwise every key would type "E"
                action = lambda d=label: self.press_digit(d)

            keys.append(u.Button(x, y, KEYPAD_SIZE, KEYPAD_SIZE, label, action))

        keys.append(u.Button(1000, 520, 140, 50, "Back", self.close_keypad))
        return keys


    # Controls the ghost's dialogue and checks whether the player has the homework.
    def talk(self):
        if self.task_done:
            self.chatbox.say("...") # feels unnecessary
        elif self.line_count < len(self.dialogue):
            self.chatbox.say(self.dialogue[self.line_count])
            self.line_count += 1
        elif "homework" in self.inventory:
            self.chatbox.say("Ghost . Is that my homework? HAND IT OVER😈")
        else:
            self.chatbox.say("Ghost > No homework, no leaving. Search the room")


    # Changes what the player sees when searching the teacher's area.
    def teacher(self):
        if self.task_done:
            self.current_image= self.no_teacher_image
            # Once the teacher leaves, the stone becomes available.
            if self.stone_collected:
                self.current_buttons = self.returnr_buttons # nobody to talk to so only return
                self.chatbox.say("You > The classroom is empty. He is really gone")
            else:
                self.current_buttons = self.stone_buttons
                self.chatbox.say("You > He left something behind on the desk              ")
        else:
            self.current_image = self.teacher_image
            self.current_buttons = self.teacher_buttons
            self.talk() #line appears moment you walk up, talk button advances it after wards

    # Adds the stone to the player's inventory if it has not already been collected.
    def collect_stone(self):
        if self.stone_collected:
            self.chatbox.say("You > I already collected the stone in my inventory")
        else:
            self.stone_collected = True
            self.inventory.append("white stone")
            self.chatbox.say("You > A white stone... one step closer to freedom")
            self.current_buttons = self.returnr_buttons


    # Opens the cabinet. The player needs to enter the code first if it is locked.
    def cabinet(self):
        self.keypad_open = False #always start on the plain cabinet screen
        if self.cabinet_unlocked:
            self.current_image = self.cabinet_open_image #closed or open picture?
            if self.homework_taken:
                self.current_buttons = self.returnr_buttons
            else:
                self.current_buttons = self.cabinet_buttons
        else:
            self.current_image = self.cabinet_locked_image
            self.current_buttons = self.cabinet_locked_buttons
            self.chatbox.say("You > It is locked there is a keypad on the front")

    # Opens the keypad and clears any previously entered code.
    def open_keypad(self):
        self.keypad_open = True
        self.code_entry = ""
        self.current_buttons = self.keypad_buttons
        self.chatbox.say("You > Type the four digit code into the keyboard")

    # Closes the keypad and returns to the locked cabinet.
    def close_keypad(self):
        self.keypad_open = False
        self.code_entry = ""
        self.current_buttons = self.cabinet_locked_buttons

    # Adds a digit to the code and automatically checks it after 4 digits.
    def press_digit(self, digit):
        if len(self.code_entry) >= 4:
            return # already full
        self.code_entry = self.code_entry + digit
        if len(self.code_entry) == 4:
            self.check_code() #check by itself once four digits are in

    # Checks the entered code against the correct cabinet code.
    def check_code(self):
        if self.code_entry == CABINET_CODE:
            self.cabinet_unlocked = True
            self.keypad_open = False
            self.current_image = self.cabinet_open_image
            self.current_buttons = self.cabinet_buttons
            self.chatbox.say("You > 'clunk' the cabinet swings open")
        else:
            self.code_entry = ""
            self.chatbox.say("You > Wrong code, try again :)")

    def clear_code(self):
        self.code_entry = ""


    # Takes the homework from the cabinet and adds it to the inventory.
    def take_homework(self):  ## don't try at home
        if self.homework_taken:
            self.chatbox.say("You > The cabinet is empty now")
            return
        self.homework_taken = True
        self.inventory.append("homework")
        self.chatbox.say("You > Old homework covered in dust, this must be it")
        self.current_buttons = self.returnr_buttons

    # Gives the homework to the ghost and completes the main task.
    def give_homework(self):  ##🥲
        if self.task_done:
            self.chatbox.say("You > I already gave it to the teacher")
            return
        if "homework" not in self.inventory:
            self.chatbox.say("You > I don't have the homework yet")
            return
        self.inventory.remove("homework")
        self.task_done = True
        self.chatbox.say("You > Here is your homework")
        self.chatbox.say("Ghost . At last... class dismissed")
        # After the homework is delivered, the teacher disappears.
        self.current_image = self.no_teacher_image
        self.current_buttons = self.stone_buttons


    # Shows the whiteboard and only gives the player a way to return.
    def whiteboard(self):
        self.current_image = self.whiteboard_image
        self.current_buttons = self.returnr_buttons

    # Tells the main game that the player wants to move to the corridor.
    def returnc(self):
        self.next_room = "corridor"


    # Returns from a searched area to the main classroom.
    def returnr(self):
        if self.task_done:
            self.current_image = self.room_empty
        else:
            self.current_image = self.room_image
        self.current_buttons = self.buttons


    # Sends mouse/keyboard events to the active buttons and keypad.
    def handle_event(self, event):
        for b in self.current_buttons:
            b.handle_event(event)

        # Keyboard input only matters when the keypad is open.
        # keyboard still works next to the 12 keys, both call the same press_digit
        if self.keypad_open and event.type == pygame.KEYDOWN:
            if event.unicode.isdigit():
                self.press_digit(event.unicode)
            elif event.key == pygame.K_BACKSPACE:
                self.code_entry = self.code_entry[:-1] #everything except the last letter
            elif event.key == pygame.K_RETURN:
                self.check_code()


    # Draws the current room, objects, keypad code, buttons and chatbox.
    def draw(self):
        self.screen.blit(self.current_image, (0, 0))
        # Draw the stone only after the teacher has left and before it is collected.
        if self.current_image is self.no_teacher_image and not self.stone_collected:
            pygame.draw.circle(self.screen, (245,245,245), self.stone_spot.center, self.stone_spot.w // 2)

        # Draw the homework inside the open cabinet until the player takes it.
        if self.current_image is self.cabinet_open_image and not self.homework_taken:
            pygame.draw.rect(self.screen, (235,235,235),  self.homework_spot )

        # Display the entered keypad code, using dashes for empty spaces.
        if self.keypad_open:
            shown = self.code_entry.ljust(4, "-") # "" -> "----", "45" -> "45--"
            text = self.codeFont.render(shown, True, (0, 255,120))
            self.screen.blit(text, CODE_DISPLAY_POS)

        # Draw the buttons currently available to the player.
        for b in self.current_buttons:
            b.draw2(self.screen)

        # Draw the dialogue box last so it appears on top of the room.
        self.chatbox.draw(self.screen)

