import pygame
import UI.uiElements as u
import os

pygame.init()
pygame.mixer.init()

# (question, answers, index of the correct answer)
QUESTIONS = [
    ("What planet is closest to the Sun?", ["Venus", "Mercury", "Mars"], 1),
    ("What gas do plants take in?", ["Oxygen", "Nitrogen", "Carbon dioxide"], 2),
    ("What is H2O?", ["Water", "Salt", "Hydrogen"], 0),
]

STONE_SPOT = pygame.Rect(300, 500, 44, 44)
STONE_COLOUR = (60, 200, 90)

CHATBOX_SIZE = (500, 90)
CHATBOX_MARGIN = 10


class View:
    ROOM = "room"
    DESK = "desk"
    QUIZ = "quiz"
    DRAWER = "drawer"  # covers both "stone inside" and "empty" - draw() decides which to show


class Quiz:
    def __init__(self, questions):
        self.questions = questions
        self.index = 0
        self.completed = False

    def current_question(self):
        return self.questions[self.index]

    def answer(self, choice):
        """Returns (was_correct, just_completed)."""
        _, _, correct = self.current_question()
        if choice != correct:
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
        self.player = player
        self.next_room = None

        # NOTE: fill in the real filename here once you have the art -
        # this is the desk close-up with the drawer shut and the quiz sitting on top.
        self.room_image = u.load_image("assets/storrageRoom/storage_room_bigger.png", self.screensize)
        self.desk_image = u.load_image("assets/storrageRoom/storrageDeskClosed.png", self.screensize)
        self.quiz_paper = u.load_image("assets/storrageRoom/quizPaper.png", self.screensize)
        self.desk_open = u.load_image("assets/storrageRoom/storrageDeskOpen.png", self.screensize)

        self.font = pygame.font.Font(None, 28)
        self.chatbox = u.Chatbox(
            CHATBOX_MARGIN,
            self.screensize[1] - CHATBOX_SIZE[1] - CHATBOX_MARGIN,
            *CHATBOX_SIZE,
            self.font,
        )

        self.quiz = Quiz(QUESTIONS)
        self.stone_collected = False
        self.fieldoftext = u.TextField(1100, 600, 100, 60)

        # static button sets, built once
        self.buttons = [
            u.Button(580, 650, 140, 30, "Leave Room", self.leave),
            u.Button(150, 250, 140, 30, "Look at desk", self.goto_desk),
        ]
        self.return_buttons = [
            u.Button(1000, 520, 140, 50, "return", self.goto_room)
        ]
        self.desk_buttons = [
            u.Button(350, 500, 180, 50, "Open drawer", self.open_drawer)
        ] + self.return_buttons
        self.back_buttons = [
            u.Button(1000, 520, 140, 50, "Back", self.goto_desk)
        ]
        self.stone_buttons = [
            u.Button(1000, 600, 180, 50, "Take stone", self.collect_stone)
        ] + self.back_buttons

        self.view = View.ROOM
        self.current_buttons = self.buttons
        self.current_image = self.room_image

    # ---------- view transitions ----------
    def _set_view(self, view, message=None):
        self.view = view
        self.current_image = {
            View.ROOM: self.room_image,
            View.DESK: self.desk_image,
            View.QUIZ: self.quiz_paper,
            View.DRAWER: self.desk_open,
        }[view]

        if view == View.QUIZ:
            self.current_buttons = self.quiz_buttons_for_current_question()
        elif view == View.DRAWER:
            self.current_buttons = self.back_buttons if self.stone_collected else self.stone_buttons
        else:
            self.current_buttons = {View.ROOM: self.buttons, View.DESK: self.desk_buttons}[view]

        if message:
            self.chatbox.say(message)

    def quiz_buttons_for_current_question(self):
        _, answers, _ = self.quiz.current_question()
        # i=i locks in the number for each button (avoids late-binding bug)
        return [
            u.Button(500, 300 + i * 60, 280, 50, text, lambda i=i: self.check_answer(i))
            for i, text in enumerate(answers)
        ] + self.back_buttons

    # ---------- room ----------
    def leave(self):
        self.next_room = "corridor"

    def goto_room(self):
        self._set_view(View.ROOM)

    def goto_desk(self):
        msg = "You > The drawer is unlocked" if self.quiz.completed \
            else "You > The drawer is locked, there is a quiz on the desk"
        self._set_view(View.DESK, msg)

    def open_drawer(self):
        if not self.quiz.completed:
            self._set_view(View.QUIZ, "Desk > " + self.quiz.current_question()[0])
        elif self.stone_collected:
            self._set_view(View.DRAWER, "You > The drawer is empty now")
        else:
            self._set_view(View.DRAWER, "You > The drawer is open, there is a green stone inside")

    # ---------- quiz ----------
    def check_answer(self, choice):
        correct, just_completed = self.quiz.answer(choice)

        if not correct:
            self.chatbox.say("You > Wrong, try again :)")
            return

        if just_completed:
            self._set_view(View.DRAWER, "You > 'click' the drawer unlocked")
        else:
            self._set_view(View.QUIZ, "Desk > " + self.quiz.current_question()[0])

    # ---------- stone ----------
    def collect_stone(self):
        if self.stone_collected:
            self.chatbox.say("You > I already have the green stone")
            return
        self.stone_collected = True
        self.player.add_item("Stones", "Green", "assets/storrageRoom/storage_room_bigger.png")
        self.chatbox.say("You > A green stone... one step closer")
        self._set_view(View.DRAWER)

    # ---------- main loop ----------
    def handle_event(self, event):
        for b in self.current_buttons:
            b.handle_event(event)
        if self.view == View.ROOM:
            self.fieldoftext.handle_event(event)

    def draw(self):
        self.screen.blit(self.current_image, (0, 0))

        if self.view == View.DRAWER and not self.stone_collected:
            pygame.draw.circle(self.screen, STONE_COLOUR, STONE_SPOT.center, STONE_SPOT.w // 2)

        for b in self.current_buttons:
            b.draw2(self.screen)

        if self.view == View.ROOM:
            self.fieldoftext.draw(self.screen)

        self.chatbox.draw(self.screen)