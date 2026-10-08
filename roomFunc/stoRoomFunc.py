import pygame
import UI.uiElements as u

########## constants ##########
# (question, answers, index of the correct answer)
QUESTIONS = [
    ("What planet is closest to the Sun?", ["Venus", "Mercury", "Mars"], 1),
    ("What gas do plants take in?", ["Oxygen", "Nitrogen", "Carbon dioxide"], 2),
    ("What is H2O?", ["Water", "Salt", "Hydrogen"], 0),
]

# mask images: full picture size, transparent except for the clickable area
MASK_DIR = "assets/storrageRoom/masks/"

# icons used in the inventory
STONE_IMAGE = "assets/stones/green.png"
FUSE_ICON = "assets/fuse_item.png"


class View:
    ROOM = "room"
    DESK = "desk"
    RACK = "rack"      # close-up of the rack with the box of fuses
    QUIZ = "quiz"
    DRAWER = "drawer"  # covers both "stone inside" and "empty" - the stone mask decides


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


########## room state ##########
images = {}     # view -> background picture
buttons = {}    # view -> list of buttons
masks = {}      # name -> Mask
next_room = None

player = None
fui = None
view = View.ROOM
quiz = None
stone_collected = False
fuse_collected = False
centerX = 0     # horizontal centre of the room picture (the chat takes the left 300px)


def getElements(p, f, screen):
    start(p, f, screen)
    current()
    return images, buttons, masks


########## load the images, masks and reset the puzzle ##########
def start(p, f, screen):
    global images, masks, player, fui, view, quiz, stone_collected, fuse_collected, centerX, next_room
    player = p
    fui = f
    size = screen.get_size()

    images = {
        View.ROOM: u.load_image("assets/storrageRoom/storage_room_bigger.png", size),
        View.DESK: u.load_image("assets/storrageRoom/storrageDesk.png", size),
        View.RACK: u.load_image("assets/storrageRoom/storrageRack.png", size),
        View.QUIZ: u.load_image("assets/storrageRoom/quizPaper.png", size),
        View.DRAWER: u.load_image("assets/storrageRoom/storrageDeskOpen.png", size),
    }

    masks = {
        "desk": u.Mask(MASK_DIR + "desk.png", size, (0, 0), gotoDesk),
        "rack": u.Mask(MASK_DIR + "rack.png", size, (0, 0), openRack),
        "fuse": u.Mask(MASK_DIR + "fuse.png", size, (0, 0), takeFuse),
        "stone": u.Mask(MASK_DIR + "stone.png", size, (0, 0), collectStone),
        "quiz": u.Mask(MASK_DIR + "quiz.png", size, (0, 0), openQuiz),
        "drawer": u.Mask(MASK_DIR + "drawer.png", size, (0, 0), openDrawer),
    }

    quiz = Quiz(QUESTIONS)
    stone_collected = False
    fuse_collected = False
    view = View.ROOM
    next_room = None
    # the room pictures are drawn at x=300, so the picture's centre is here
    centerX = 300 + (size[0] - 300) // 2


def current():
    global buttons
    buttons = {
        View.ROOM: [u.Button(580, 650, 140, 30, "Leave Room", leave)],
        View.DESK: [u.Button(1000, 520, 140, 50, "return", gotoRoom)],      # quiz + drawer are masks
        View.RACK: [u.Button(1000, 520, 140, 50, "return", gotoRoom)],      # fuse is a mask
        View.DRAWER: [u.Button(1000, 520, 140, 50, "Back", gotoDesk)],      # stone is a mask
        View.QUIZ: [],                                                     # rebuilt for every question
    }


########## helpers ##########
def say(text):
    fui.chat.say(text)


def currentButtons():
    return buttons[view]


def activeMasks():
    # which masks can be seen / clicked in the current view
    if view == View.ROOM:
        return [masks["desk"], masks["rack"]]
    if view == View.RACK:
        return [] if fuse_collected else [masks["fuse"]]
    if view == View.DESK:
        active = [masks["drawer"]]
        if not quiz.completed:
            active.append(masks["quiz"])
        return active
    if view == View.DRAWER:
        return [] if stone_collected else [masks["stone"]]
    return []


########## view transitions ##########
def setView(newView, message=None):
    global view
    view = newView

    if view == View.QUIZ:
        buttons[View.QUIZ] = quizButtons()

    #if message:
        #say(message)


def quizButtons():
    _, answers, _ = quiz.current_question()
    w = 280
    # i=i locks in the number for each button (avoids late-binding bug)
    return [
        u.Button(centerX - w // 2, 300 + i * 60, w, 50, text, lambda i=i: checkAnswer(i))
        for i, text in enumerate(answers)
    ] + [u.Button(1000, 520, 140, 50, "Back", gotoDesk)]


########## room ##########
def leave():
    global next_room
    next_room = "corridor"


def gotoRoom():
    setView(View.ROOM)


def gotoDesk():
    msg = "You > The drawer is unlocked" if quiz.completed \
        else "You > The drawer is locked, there is a quiz on the desk"
    setView(View.DESK, msg)


########## storage rack ##########
def openRack():
    setView(View.RACK)
    if not fuse_collected:
        say("You > A box of fuses... one slot is empty")


def takeFuse():
    global fuse_collected
    if fuse_collected:
        return
    fuse_collected = True
    # add_item(category, name, icon path)
    player.add_item("Items", "Fuse", FUSE_ICON)
    say("You > A spare fuse. This could come in handy")


########## desk ##########
def openQuiz():
    if quiz.completed:
        return
    setView(View.QUIZ, "Desk > " + quiz.current_question()[0])


def openDrawer():
    if not quiz.completed:
        say("You > The drawer is locked, maybe the quiz on the desk opens it")
    elif stone_collected:
        setView(View.DRAWER, "You > The drawer is empty now")
    else:
        setView(View.DRAWER, "You > The drawer is open, there is a green stone inside")


########## quiz ##########
def checkAnswer(choice):
    correct, justCompleted = quiz.answer(choice)

    if not correct:
        #say("You > Wrong, try again :)")
        return

    if justCompleted:
        # quiz done: back to the desk, the drawer is unlocked but you still have to open it
        say("You > 'click' the drawer unlocked")
        setView(View.DESK)
    else:
        setView(View.QUIZ, "Desk > " + quiz.current_question()[0])


########## stone ##########
def collectStone():
    global stone_collected
    if stone_collected:
        return
    stone_collected = True
    player.add_item("Stones", "Green", STONE_IMAGE)
    #say("You > A green stone... one step closer")
    setView(View.DRAWER)