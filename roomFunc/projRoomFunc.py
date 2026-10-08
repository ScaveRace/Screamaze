import pygame
import UI.uiElements as u

images = []
buttons = {}
next_room = None

########## shapes and items ##########
found = {}
placed = {}
holding = None
hasFlyer = False

########## room states ##########
view = "room"
riddleDone = False

########## message system ##########
message = ""
messageUntil = 0

########## positions of the box slots ##########
slots = {
    "circle": (450, 300),
    "triangle": (580, 300),
    "square": (710, 300),
}
slotSize = 100


def getElements(player,fui,screen):
    start(screen)
    current()
    return images,buttons

def current():
    global buttons
    buttons = {
        ########## buttons in the main room ##########
        "corners": [
            u.Button(60, 120, 230, 60, "Bookshelf", searchShelf),
            u.Button(990, 120, 230, 60, "Whiteboard", readRiddle),
            u.Button(60, 560, 230, 60, "Beanbags", searchBeanbags),
            u.Button(990, 560, 230, 60, "Locked box", openBox),
        ],
        ########## riddle answer buttons ##########
        "riddle": [
            u.Button(340, 420, 200, 50, "Four", riddleWrong),
            u.Button(560, 420, 200, 50, "Three", riddleRight),
            u.Button(780, 420, 200, 50, "Eight", riddleWrong),
        ],
        ########## navigation buttons ##########
        "back": u.Button(60, 650, 160, 45, "Back", backToRoom),
        "leave": u.Button(540, 650, 200, 45, "Leave the room", leave),
    }


########## load the images and reset the puzzle ##########
def start(screen):
    global images, found, placed, holding, hasFlyer, view, riddleDone, message, messageUntil
    images = [
        u.load_image("assets/project_room.png", screen.get_size(), (22, 20, 26)),
        u.load_image("assets/", (420, 300), (40, 32, 26)),
    ]
    found = {"circle": False, "triangle": False, "square": False}
    placed = {"circle": False, "triangle": False, "square": False}
    holding = None
    hasFlyer = False
    view = "room"
    riddleDone = False
    message = ""
    messageUntil = 0


########## search bookshelf for circle ##########
def searchShelf():
    if found["circle"]:
        say("Nothing else behind the books.")
    else:
        found["circle"] = True
        say("A round wooden disc was wedged between two folders.")


########## search beanbags for square ##########
def searchBeanbags():
    if found["square"]:
        say("Just crumbs down there.")
    else:
        found["square"] = True
        say("Under the beanbag: a square block.")


########## open the whiteboard riddle ##########
def readRiddle():
    global view
    if found["triangle"]:
        say("The whiteboard is wiped clean now.")
    else:
        view = "riddle"


########## open the locked box ##########
def openBox():
    global view
    view = "box"


########## correct riddle answer ##########
def riddleRight():
    global view, riddleDone
    found["triangle"] = True
    riddleDone = True
    view = "room"
    say("The marker tray slides open. A triangle falls out.")


########## wrong riddle answer ##########
def riddleWrong():
    say("Nothing happens.")


########## pick up a shape ##########
def pickUp(shape):
    global holding
    if found[shape] and not placed[shape]:
        holding = shape


########## place shape into the matching slot ##########
def tryPlace(slot):
    global holding, hasFlyer
    if holding is None:
        return

    if holding == slot:
        placed[slot] = True
        holding = None
        say("It clicks into place.")

        ########## check if all shapes have been placed ##########
        if all(placed.values()):
            hasFlyer = True
            say("The lid springs open. Inside is a flyer: EQUINOX STUDENT SOCIETY.")

    else:
        holding = None
        say("That does not fit.")


########## handle clicking shapes and box slots ##########
def boxClick(pos):
    x = 420

    for shape in ("circle", "triangle", "square"):
        if found[shape] and not placed[shape]:
            if pygame.Rect(x, 470, 90, 90).collidepoint(pos):
                pickUp(shape)
            x = x + 110

    for shape in slots:
        sx, sy = slots[shape]

        if pygame.Rect(sx, sy, slotSize, slotSize).collidepoint(pos):
            tryPlace(shape)


########## return to the main room ##########
def backToRoom():
    global view, holding
    view = "room"
    holding = None


########## leave project room and go to corridor ##########
def leave():
    global next_room
    next_room = "corridor"


########## display temporary message ##########
def say(text):
    global message, messageUntil
    message = text
    messageUntil = pygame.time.get_ticks() + 4000
