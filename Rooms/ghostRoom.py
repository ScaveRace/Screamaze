
import pygame
import UI.uiElements as u

pygame.init()
pygame.mixer.init()

CABINET_CODE = "4537"


class GhostRoom:
    def __init__(self, screen):
        self.screensize = screen.get_size()
        self.screen = screen
        self.conversation = 0
        self.next_room = None

        self.room_image = u.load_image("assets/gr.ghostRoom.png", self.screensize)
        self.room_empty = u.load_image("assets/gr.ghostRoom.no.teacher.png", self.screensize)
        self.current_image = self.room_image

        self.teacher_image = u.load_image("assets/gr.teacher.png", self.screensize)
        self.no_teacher_image = u.load_image("assets/gr.bureau.no.teacher.png", self.screensize)

        self.whiteboard_image = u.load_image("assets/gr.whiteboard.4537.png", self.screensize)

        self.cabinet_locked_image = u.load_image("assets/gr.cabinet.homework.png", self.screensize)
        self.cabinet_open_image = u.load_image("assets/gr.cabinet.open.png", self.screensize)

        self.font = pygame.font.Font(None, 28)
        self.chatbox = u.Chatbox(10,10,500, 90,self.font) #change width and height of chatbox

        self.dialogue = [
            "Ghost > Ohh a student has finally come to class.",
            "Ghost > I have been waiting for the homework since I died.",
            "Ghost > Only by handing in your homework can you leave.",
        ]
        self.line_count = 0

        self.inventory = [] # how to link to player inventory?
        self.homework_taken = False #so you can't take the homework

        self.task_done = False #memory for has the homework been handed in

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
            self.current_buttons = self.returnr_buttons # nobody to talk to so only return
            self.chatbox.say("You > The classroom is empty. He is really gone")
        else:
            self.current_image = self.teacher_image
            self.current_buttons = self.teacher_buttons
            self.talk() #line appears moment you walk up, talk button advances it afterwars


    def cabinet(self):
        self.current_image = u.load_image("assets/gr.cabinet.homework.png", self.screensize) #closed or open picture?
        self.current_buttons = self.cabinet_buttons

    def take_homework(self):
        if self.homework_taken:
            self.chatbox.say("You > The cabinet is empty now")
            return
        self.homework_taken = True
        self.inventory.append("homework")
        self.chatbox.say("You > Old homework covered in dust, this must be it")

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
        self.current_buttons = self.returnr_buttons


    def whiteboard(self):
        self.current_image = u.load_image("assets/gr.whiteboard.4537.png", self.screensize)
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


    def draw(self):
        self.screen.blit(self.current_image, (0, 0))
        for b in self.current_buttons:
            b.draw2(self.screen)

        self.chatbox.draw(self.screen)

