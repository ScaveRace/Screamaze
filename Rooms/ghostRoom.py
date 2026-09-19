import pygame
import UI.uiElements as u

pygame.init()
pygame.mixer.init()

CABINET_CODE = "4537"

# where the typed digits get drawn on top of gr.cabinet.homework.png -> tune to your art
CODE_DISPLAY_POS = (615, 205)

class GhostRoom:
    def __init__(self, screen):
        self.screensize = screen.get_size()
        self.screen = screen
        self.next_room = None

        self.room_image = u.load_image("assets/gr.ghostRoom.png", self.screensize)
        self.room_empty = u.load_image("assets/gr.ghostRoom.no.teacher.png", self.screensize)
        self.current_image = self.room_image

        self.teacher_image = u.load_image("assets/gr.teacher.png", self.screensize)
        self.no_teacher_image = u.load_image("assets/gr.bureau.no.teacher.png", self.screensize)

        self.whiteboard_image = u.load_image("assets/gr.whiteboard.4537.png", self.screensize)

        self.cabinet_locked_image = u.load_image("assets/gr.cabinet.homework.png", self.screensize)
        self.cabinet_open_image = u.load_image("assets/gr.cabinet.open.keypad.png", self.screensize)

        self.font = pygame.font.Font(None, 28)
        self.chatbox = u.Chatbox(10,10,500, 90,self.font) #change width and height of chatbox
        self.codeFont = pygame.font.Font(None, 56)

        self.dialogue = [
            "Ghost > Ohh a student has finally come to class.",
            "Ghost > I have been waiting for the homework since I died.",
            "Ghost > Only by handing in your homework can you leave.",
        ]
        self.line_count = 0

        self.inventory = [] # how to link to player inventory?
        self.homework_taken = False #so you can't take the homework
        self.homework_spot = pygame.Rect(600, 400, 56, 56)

        self.task_done = False #memory for has the homework been handed in

        self.stone_collected = False
        self.stone_spot = pygame.Rect(750, 400, 44, 44) # position stone on empty desk

        self.cabinet_unlocked = False
        self.code_entry = "" #string that grows as you type
        self.keypad_open  = False

        self.buttons = [
            u.Button(930, 350, 140, 50, "Search", self.teacher),
            u.Button(580, 50, 140, 50, "Search", self.whiteboard),
            u.Button(140, 500, 140, 50, "Search", self.cabinet),
            u.Button(560, 650, 140, 50, "Return", self.returnc),
        ]
        self.current_buttons = self.buttons
        self.returnr_buttons = [
            u.Button(1000, 520, 140, 50, "return", self.returnr)]
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
        self.keypad_buttons = [
            u.Button(1000,520,140,50, "Back", self.close_keypad)
        ]



    def talk(self):
        if self.task_done:
            self.chatbox.say("...") # feels unnecessary
        elif self.line_count < len(self.dialogue):
            self.chatbox.say(self.dialogue[self.line_count])
            self.line_count += 1
        elif "homework" in self.inventory:
            self.chatbox.say("Ghost . Is that my homework? HAND IT OVER")
        else:
            self.chatbox.say("Ghost > No homework, no leaving. Search the room")


    def teacher(self):
        if self.task_done:
            self.current_image= self.no_teacher_image
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

    def collect_stone(self):
        if self.stone_collected:
            self.chatbox.say("You > I already collected the stone in my inventory")
            return
        self.stone_collected = True
        self.inventory.append("white stone")
        self.chatbox.say("You > A white stone... one step closer to freedom")
        self.current_buttons = self.returnr_buttons


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

    def open_keypad(self):
        self.keypad_open = True
        self.code_entry = ""
        self.current_buttons = self.keypad_buttons
        self.chatbox.say("You > Type the four digit code into the keyboard")

    def close_keypad(self):
        self.keypad_open = False
        self.code_entry = ""
        self.current_buttons = self.cabinet_locked_buttons

    def press_digit(self, digit):
        if len(self.code_entry) >= 4:
            return # already full
        self.code_entry = self.code_entry + digit
        if len(self.code_entry) == 4:
            self.check_code() #check by itself once four digits are in

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


    def take_homework(self):
        if self.homework_taken:
            self.chatbox.say("You > The cabinet is empty now")
            return
        self.homework_taken = True
        self.inventory.append("homework")
        self.chatbox.say("You > Old homework covered in dust, this must be it")
        self.current_buttons = self.returnr_buttons

    def give_homework(self):
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
        self.current_image = self.no_teacher_image
        self.current_buttons = self.stone_buttons


    def whiteboard(self):
        self.current_image = self.whiteboard_image
        self.current_buttons = self.returnr_buttons

    def returnc(self):
        self.next_room = "corridor"


    def returnr(self):
        if self.task_done:
            self.current_image = self.room_empty
        else:
            self.current_image = self.room_image
        self.current_buttons = self.buttons


    def handle_event(self, event):
        for b in self.current_buttons:
            b.handle_event(event)

        if self.keypad_open and event.type == pygame.KEYDOWN:
            if event.unicode.isdigit():
                self.press_digit(event.unicode)
            elif event.key == pygame.K_BACKSPACE:
                self.code_entry = self.code_entry[:-1] #everything except the last letter
            elif event.key == pygame.K_RETURN:
                self.check_code()



    def draw(self):
        self.screen.blit(self.current_image, (0, 0))
        if self.current_image is self.no_teacher_image and not self.stone_collected:
            pygame.draw.circle(self.screen, (245,245,245), self.stone_spot.center, self.stone_spot.w // 2)

        if self.current_image is self.cabinet_open_image and not self.homework_taken:
            pygame.draw.rect(self.screen, (235,235,235),  self.homework_spot )

        if self.keypad_open:
            shown = self.code_entry.ljust(4, "-") # "" -> "----", "45" -> "45--"
            text = self.codeFont.render(shown, True, (0, 255,120))
            self.screen.blit(text, CODE_DISPLAY_POS)

        for b in self.current_buttons:
            b.draw2(self.screen)

        self.chatbox.draw(self.screen)

