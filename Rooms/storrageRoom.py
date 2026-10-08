import pygame
import UI.uiElements as u
from functions import uiFunc as uF

pygame.init()
pygame.mixer.init()

# (question, answers, index of the correct answer)
QUESTIONS = [
    ("What planet is closest to the Sun?", ["Venus", "Mercury", "Mars"], 1),
    ("What gas do plants take in?", ["Oxygen", "Nitrogen", "Carbon dioxide"], 2),
    ("What is H2O?", ["Water", "Salt", "Hydrogen"], 0),
]

# green stone lying in the open drawer: centre on screen + size (tune to move / resize it)
STONE_IMAGE = "assets/stones/green.png"
STONE_CENTER = (1267, 555)
STONE_SIZE = (48, 64)

QUESTION_COLOUR = (30, 25, 20)  # text colour of the question on the quiz paper

# mask images, same idea as assets/vampire/masks/...  -> make these PNGs (full room size, transparent
# except for the clickable area) and put them in this folder, or change the paths here
MASK_DIR = "assets/storrageRoom/masks/"
FUSE_ICON = "assets/fuse_item.png"
RACK_IMAGE = "assets/storrageRoom/storrageRack.png"


class View:
    ROOM = "room"
    DESK = "desk"
    QUIZ = "quiz"
    DRAWER = "drawer"  # covers both "stone inside" and "empty" - draw() decides which to show
    RACK = "rack"


class Quiz:
    def __init__(self, questions):
        self.questions = questions
        self.index = 0
        self.completed = False

    def current_question(self):
        return self.questions[self.index]

    def answer(self, choice):
        _, _, correct = self.current_question()
        if choice != correct:
            return False, False

        self.index += 1
        if self.index >= len(self.questions):
            self.completed = True
            return True, True
        return True, False


class StorrageRoom:
    def __init__(self, screen, player, fui):
        self.screensize = screen.get_size()
        self.screen = screen
        self.fui = fui
        self.player = player
        self.next_room = None

        self.room_image = u.load_image("assets/storrageRoom/storage_room_bigger.png", self.screensize)
        self.desk_image = u.load_image("assets/storrageRoom/storrageDesk.png", self.screensize)
        self.quiz_paper = u.load_image("assets/storrageRoom/quizPaper.png", self.screensize)
        self.desk_open = u.load_image("assets/storrageRoom/storrageDeskOpen.png", self.screensize)
        self.rack_image = u.load_image(RACK_IMAGE, self.screensize)

        self.font = pygame.font.Font(None, 28)
        self.questionFont = pygame.font.Font(None, 34)

        # the room pictures are drawn at x=300 (chat takes the left 300px), so the picture's centre is here
        self.centerX = 300 + (self.screensize[0] - 300) // 2



        self.quiz = Quiz(QUESTIONS)
        self.stone_collected = False
        self.fuse_collected = False
        self.fieldoftext = u.TextField(1100, 600, 100, 60)

        # ---------- masks ----------
        size = self.screensize
        self.stone_mask = u.Mask(MASK_DIR + "stone.png", size, (0,0), self.collect_stone)
        self.desk_mask = u.Mask(MASK_DIR + "desk.png", size, (0, 0), self.goto_desk)
        self.rack_mask = u.Mask(MASK_DIR + "rack.png", size, (0, 0), self.search_rack)
        self.fuse_mask = u.Mask(MASK_DIR + "fuse.png", size, (0, 0), self.collect_fuse)
        self.quiz_mask = u.Mask(MASK_DIR + "quiz.png", size, (0, 0), self.open_quiz)
        self.drawer_mask = u.Mask(MASK_DIR + "drawer.png", size, (0, 0), self.open_drawer)

        # static button sets, built once
        self.buttons = [
            u.Button(580, 650, 140, 30, "Leave Room", self.leave),
        ]
        self.return_buttons = [
            u.Button(1000, 520, 140, 50, "return", self.goto_room)
        ]
        self.desk_buttons = list(self.return_buttons)  # quiz + drawer are masks now
        self.back_buttons = [
            u.Button(1000, 620, 140, 50, "Back", self.goto_desk)
        ]
        self.rack_back_buttons = [
            u.Button(1000, 620, 140, 50, "Back", self.goto_room)
        ]

        self.view = View.ROOM
        self.current_buttons = self.buttons
        self.current_image = self.room_image

    # ---------- helpers ----------
    def say(self, text):
        self.fui.chat.say(text)

    def active_masks(self):
        # which masks can be seen / clicked in the current view
        if self.view == View.ROOM:
            masks = [self.desk_mask]
            if not self.fuse_collected:
                masks.append(self.rack_mask)
            return masks
        if self.view == View.RACK:
            return [] if self.fuse_collected else [self.fuse_mask]
        if self.view == View.DESK:
            masks = [self.drawer_mask]
            if not self.quiz.completed:
                masks.append(self.quiz_mask)
            return masks
        if self.view == View.DRAWER and not self.stone_collected:
            return [self.stone_mask]
        return []

    # ---------- view transitions ----------
    def _set_view(self, view, message=None):
        self.view = view
        self.current_image = {
            View.ROOM: self.room_image,
            View.DESK: self.desk_image,
            View.QUIZ: self.quiz_paper,
            View.DRAWER: self.desk_open,
            View.RACK: self.rack_image,
        }[view]

        if view == View.QUIZ:
            self.current_buttons = self.quiz_buttons_for_current_question()
        elif view == View.DRAWER:
            self.current_buttons = self.return_buttons
        elif view == View.RACK:
            self.current_buttons = self.rack_back_buttons
        else:
            self.current_buttons = {View.ROOM: self.buttons, View.DESK: self.desk_buttons}[view]

        #if message:
            #self.fui.say(message)

    def quiz_buttons_for_current_question(self):
        _, answers, _ = self.quiz.current_question()
        # i=i locks in the number for each button (avoids late-binding bug)
        w = 280
        return [
            u.Button(self.centerX - w // 2, 300 + i * 60, w, 50, text, lambda i=i: self.check_answer(i))
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

    # ---------- storage rack ----------
    def search_rack(self):
        if self.fuse_collected:
            return
        self._set_view(View.RACK, "You > You search through the rack and find something...")

    def collect_fuse(self):
        if self.fuse_collected:
            return
        self.fuse_collected = True
        # add_item(category, name, icon path)
        self.player.add_item("Items", "Fuse", FUSE_ICON)
        self.say("You > Behind some old boxes on the rack... a fuse!")

    # ---------- desk ----------
    def open_quiz(self):
        if self.quiz.completed:
            return
        self._set_view(View.QUIZ, "Desk > " + self.quiz.current_question()[0])

    def open_drawer(self):
        if not self.quiz.completed:
            self.say("You > The drawer is locked, maybe the quiz on the desk opens it")
        elif self.stone_collected:
            self._set_view(View.DRAWER, "You > The drawer is empty now")
        else:
            self._set_view(View.DRAWER, "You > The drawer is open, there is a green stone inside")

    # ---------- quiz ----------
    def check_answer(self, choice):
        correct, just_completed = self.quiz.answer(choice)

        if not correct:
            #self.chatbox.say("You > Wrong, try again :)")
            return

        if just_completed:
            # quiz done: back to the desk, the drawer is unlocked but you still have to open it
            self.say("You > 'click' the drawer unlocked")
            self._set_view(View.DESK)
        else:
            self._set_view(View.QUIZ, "Desk > " + self.quiz.current_question()[0])

    # ---------- stone ----------
    def collect_stone(self):
        if self.stone_collected:
            #self.chatbox.say("You > I already have the green stone")
            return
        self.stone_collected = True
        self.player.add_item("Stones", "Green", STONE_IMAGE)
        #self.chatbox.say("You > A green stone... one step closer")
        self._set_view(View.DRAWER)

    # ---------- main loop ----------
    def handle_event(self, event):
        # snapshot both lists first, so a click that changes the view
        # can't also click something in the new view
        masks = self.active_masks()
        buttons = list(self.current_buttons)
        view_before = self.view

        for m in masks:
            m.handle_event(event)
            if self.view != view_before:
                return

        for b in buttons:
            b.handle_event(event)
            if self.view != view_before:
                return

        if self.view == View.ROOM:
            self.fieldoftext.handle_event(event)

    def draw(self):
        self.screen.blit(self.current_image, (300, 0))

        if self.view == View.QUIZ:
            question = self.quiz.current_question()[0]
            text = uF.render_wrapped(self.questionFont, question, QUESTION_COLOUR, 600)
            self.screen.blit(text, text.get_rect(midbottom=(self.centerX, 285)))

        for m in self.active_masks():
            m.draw(self.screen)

        for b in self.current_buttons:
            b.draw2(self.screen)

        if self.view == View.ROOM:
            self.fieldoftext.draw(self.screen)