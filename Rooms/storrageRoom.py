import pygame
import UI.uiElements as u

pygame.init()
pygame.mixer.init()

# (question, answers, index of the correct answer)
QUESTIONS = [
    ("What planet is closest to the Sun?", ["Venus", "Mercury", "Mars"], 1),
    ("What gas do plants take in?", ["Oxygen", "Nitrogen", "Carbon dioxide"], 2),
    ("What is H2O?", ["Water", "Salt", "Hydrogen"], 0),
]

stone_spot = pygame.Rect(300,500,44,44)
stone_colour = (60,200,90)

chatbox_size = (500,90)
chatbox_margin = 10


class view:
    st_room = "room"
    desk = "desk"
    quiz = "quiz"
    dr_full = "drawer_full"
    dr_empty = "drawer_empty"

class Quiz:
    def __init__(self, questions):
        self.questions = questions
        self.index = 0
        self.completed = False

    def current_question(self):
        return self.questions[self.index]

    def answer(self, choice):
        _, _, correct = self.current_question()
        if correct != correct:
            return False, False
        self.index += 1
        if self.index >= len(self.questions):
            self.completed = True
            return True, True
        return True, False


class StorrageRoom:
    def __init__(self, screen, player):
        self.screensize = screen.get_size()
        self.screen = screen
        self.next_room = None

        self.room_image = u.load_image("assets/storrageRoom/storage_room_bigger.png", self.screensize)
        self.desk_image = u.load_image("assets/storrageRoom/.png", self.screensize)
        self.quiz_paper = u.load_image("assets/storrageRoom/quizPaper.png", self.screensize)
        self.desk_open = u.load_image("assets/storrageRoom/storrageDeskOpen.png", self.screensize)
        self.current_image = self.room_image

        self.font = pygame.font.Font(None, 28)
        # chatbox along the bottom of the screen (1280x720)
        self.chatbox = u.Chatbox(10, self.screensize[1] - 90 - 10, 500, 90, self.font)

        self.inventory = []  # global player inventory will be used later

        # quiz memory
        self.quizCompleted = False
        self.q_index = 0

        # green stone in the drawer
        self.stone_collected = False
        self.stone_spot = pygame.Rect(300, 500, 44, 44)  # position of the stone in the drawer

        self.fieldoftext = u.TextField(1100, 600, 100, 60)

        # main room buttons
        self.buttons = [
            u.Button(580, 650, 140, 30, "Leave Room", self.leave),
            u.Button(150, 250, 140, 30, "Look at desk", self.desk),
        ]
        self.current_buttons = self.buttons

        self.returnr_buttons = [
            u.Button(1000, 520, 140, 50, "return", self.returnr)]
        # desk view: open the drawer (quiz) or go back to the room
        self.desk_buttons = [
            u.Button(350, 500, 180, 50, "Open drawer", self.drawer)
        ] + self.returnr_buttons
        # inside the drawer / quiz: go back to the desk
        self.back_buttons = [
            u.Button(1000, 520, 140, 50, "Back", self.desk)]
        self.stone_buttons = [
            u.Button(1000, 600, 180, 50, "Take stone", self.collect_stone)
        ] + self.back_buttons
        self.quiz_buttons = []  # rebuilt for every question

    # ---------- room ----------
    def leave(self):
        self.next_room = "corridor"

    def desk(self):
        # first step: just look at the desk
        self.current_image = self.desk_image
        self.current_buttons = self.desk_buttons
        if self.quizCompleted:
            self.chatbox.say("You > The drawer is unlocked")
        else:
            self.chatbox.say("You > The drawer is locked, there is a quiz on the desk")

    def drawer(self):
        # second step: open the drawer -> quiz, or the stone once it is solved
        if not self.quizCompleted:
            self.show_question()
        elif self.stone_collected:
            self.current_buttons = self.back_buttons
            self.chatbox.say("You > The drawer is empty now")
        else:
            self.current_buttons = self.stone_buttons
            self.chatbox.say("You > The drawer is open, there is a green stone inside")

    # ---------- quiz ----------
    def show_question(self):
        question, answers, _ = QUESTIONS[self.q_index]
        self.chatbox.say("Desk > " + question)

        # i=i locks in the number for each button
        self.quiz_buttons = [
            u.Button(500, 300 + i * 60, 280, 50, text, lambda i=i: self.check_answer(i))
            for i, text in enumerate(answers)
        ] + self.back_buttons
        self.current_buttons = self.quiz_buttons

    def check_answer(self, choice):
        if choice != QUESTIONS[self.q_index][2]:
            self.chatbox.say("You > Wrong, try again :)")
            return

        self.q_index += 1
        if self.q_index >= len(QUESTIONS):
            self.quizCompleted = True
            self.chatbox.say("You > 'click' the drawer unlocked")
            self.current_buttons = self.stone_buttons
        else:
            self.chatbox.say("You > Correct!")
            self.show_question()

    # ---------- stone ----------
    def collect_stone(self):
        if self.stone_collected:
            self.chatbox.say("You > I already have the green stone")
        else:
            self.stone_collected = True
            self.inventory.append("green stone")
            self.chatbox.say("You > A green stone... one step closer")
            self.current_buttons = self.back_buttons

    def returnr(self):
        self.current_image = self.room_image
        self.current_buttons = self.buttons

    # ---------- main loop ----------
    def handle_event(self, event):
        for b in self.current_buttons:
            b.handle_event(event)
        if self.current_buttons is self.buttons:
            self.fieldoftext.handle_event(event)

    def draw(self):
        self.screen.blit(self.current_image, (0, 0))

        # show the stone while the drawer is open and it hasn't been taken
        if self.quizCompleted and not self.stone_collected and self.current_image is self.desk_image:
            if self.current_buttons is self.stone_buttons:
                pygame.draw.circle(self.screen, (60, 200, 90), self.stone_spot.center, self.stone_spot.w // 2)

        for b in self.current_buttons:
            b.draw2(self.screen)

        if self.current_buttons is self.buttons:
            self.fieldoftext.draw(self.screen)

        self.chatbox.draw(self.screen)