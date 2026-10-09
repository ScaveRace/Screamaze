import UI.uiElements as u
import functions.language as lang

########## constants ##########
TABLE = "SorrageRoom"   # (sic) the name of this room in the language files

# ids of the quiz texts in the language files: (question id, [answer ids], index of the correct answer)
QUESTION_IDS = [
    (11, [12, 13, 14], 1),
    (15, [16, 17, 18], 2),
    (19, [20, 21, 22], 0),
]

# ids of the chat messages in the language files
MSG_FUSE_BOX = 1
# ids of the chat messages in the database table
MSG_FUSE_TAKEN = 2
MSG_DRAWER_LOCKED_HINT = 5
MSG_QUIZ_DONE = 8
MSG_STONE_TAKEN = 9
MSG_WRONG = 10
MSG_LEAVE = 31

# ids of the "what is on screen" descriptions
DESC_ROOM = 23
DESC_DESK_LOCKED = 24
DESC_DESK_OPEN = 25
DESC_RACK_FUSE = 26
DESC_RACK_EMPTY = 27
DESC_DRAWER_STONE = 28
DESC_DRAWER_EMPTY = 29
DESC_QUIZ = 30      # contains {n} and {total}

texts = {}      # id -> text, filled by loadTexts()


def loadTexts():
    # read every line of this room from the language files once, when the room starts
    global texts
    texts = {int(i): lang.chatMessage(TABLE, i) for i in lang.texts["en"][TABLE]}


def T(textId):
    text = texts.get(textId)
    if text is None or text == "":
        return text if text else f"[missing text {textId}]"
    return str(text)


def buildQuestions():
    # (question, answers, index of the correct answer)
    return [(T(q), [T(a) for a in answers], correct) for q, answers, correct in QUESTION_IDS]


# mask images: full picture size, transparent except for the clickable area
MASK_DIR = "assets/storrageRoom/masks/"

# icons used in the inventory
STONE_IMAGE = "assets/stones/green.png"
FUSE_ICON = "assets/vampire/masks/fuse.png"


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
            self.index = 0          # wrong answer: back to question 1
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

    loadTexts()
    quiz = Quiz(buildQuestions())
    stone_collected = False
    fuse_collected = False
    view = View.ROOM
    next_room = None
    # the room pictures are drawn at x=300, so the picture's centre is here
    centerX = 300 + (size[0] - 300) // 2

    describe()      # say what the room looks like when it starts


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


def describe():
    # say what is on screen right now
    if view == View.ROOM:
        text = T(DESC_ROOM)
    elif view == View.DESK:
        text = T(DESC_DESK_OPEN if quiz.completed else DESC_DESK_LOCKED)
    elif view == View.RACK:
        text = T(DESC_RACK_EMPTY if fuse_collected else DESC_RACK_FUSE)
    elif view == View.DRAWER:
        text = T(DESC_DRAWER_EMPTY if stone_collected else DESC_DRAWER_STONE)
    elif view == View.QUIZ:
        text = T(DESC_QUIZ).format(n=quiz.index + 1, total=len(quiz.questions))
    else:
        return
    say("You > " + text)


########## view transitions ##########
def setView(newView):
    global view
    view = newView

    if view == View.QUIZ:
        buttons[View.QUIZ] = quizButtons()

    describe()


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
    say("You > " + T(MSG_LEAVE))
    next_room = "corridor"


def gotoRoom():
    setView(View.ROOM)


def gotoDesk():
    setView(View.DESK)


########## storage rack ##########
def openRack():
    setView(View.RACK)


def takeFuse():
    global fuse_collected
    if fuse_collected:
        return
    fuse_collected = True
    # add_item(category, name, icon path)
    player.add_item("Items", "Fuse", FUSE_ICON)
    say("You > " + T(MSG_FUSE_TAKEN))
    describe()      # the rack looks different now


########## desk ##########
def openQuiz():
    if quiz.completed:
        return
    setView(View.QUIZ)


def openDrawer():
    if not quiz.completed:
        say("You > " + T(MSG_DRAWER_LOCKED_HINT))   # no view change, so no description
    else:
        setView(View.DRAWER)


########## quiz ##########
def checkAnswer(choice):
    correct, justCompleted = quiz.answer(choice)

    if not correct:
        say("You > " + T(MSG_WRONG))
        setView(View.QUIZ)      # rebuilds the buttons and describes question 1
        return

    if justCompleted:
        # quiz done: back to the desk, the drawer is unlocked but you still have to open it
        say("You > " + T(MSG_QUIZ_DONE))
        setView(View.DESK)
    else:
        setView(View.QUIZ)


########## stone ##########
def collectStone():
    global stone_collected
    if stone_collected:
        return
    stone_collected = True
    player.add_item("Stones", "Green", STONE_IMAGE)
    #say("You > " + T(MSG_STONE_TAKEN))
    setView(View.DRAWER)