import UI.uiElements as u

ROOM = "ProjectRoom"                          # table name in the story database
STONE_ICON = "assets/stones/purple.png"

########## the chat takes the left 300px, so the room starts here ##########
X = u.startX

# a plain +300 would push the right-hand buttons (230 wide) past the 1480px screen,
# so they sit 60px from the right edge instead
RIGHT_X = 1480 - 60 - 230

########## the three badges, found in other rooms as items with exactly these names ##########
SHAPES = ("Circle", "Triangle", "Square")
owners = {"Circle": "Mina", "Triangle": "Sam", "Square": "Jorn"}    # whose badge it is, see the whiteboard

image = None
boxImage = None
roomButtons = []
slotButtons = {}         # shape -> the slot in the box that belongs to it
badgeButtons = []        # the badges the player carries, rebuilt when they change
backButton = None
next_room = None

view = "room"            # "room" or "box"
holding = None
player = None
fui = None
memory = {}              # ProjectRoom.memory, so progress survives leaving the room


def getElements(p, f, screen, mem):
    global player, fui, memory, image, boxImage, roomButtons, slotButtons, backButton, view, holding
    player, fui, memory = p, f, mem
    view = "room"
    holding = None

    image = u.load_image("assets/project_room.png", screen.get_size(), (22, 20, 26))
    boxImage = u.load_alpha_image("assets/", (420, 300), (40, 32, 26))

    roomButtons = [
        u.Button(X + 60, 120, 230, 60, "Bookshelf", searchShelf),
        u.Button(RIGHT_X, 120, 230, 60, "Whiteboard", readBoard),
        u.Button(X + 60, 560, 230, 60, "Beanbags", checkPhone),
        u.Button(RIGHT_X, 560, 230, 60, "Locked box", openBox),
        u.Button(X + 540, 650, 200, 45, "Leave the room", leave),
    ]
    backButton = u.Button(X + 60, 650, 160, 45, "Back", backToRoom)

    # one slot per badge, it shows the name of its owner until the badge is in
    slotButtons = {}
    for i, shape in enumerate(SHAPES):
        label = shape if memory["placed"][shape] else owners[shape]
        slotButtons[shape] = u.Button(X + 450 + 130 * i, 300, 100, 100, label,
                                      lambda shape=shape: tryPlace(shape))

    if memory["stoneTaken"]:
        say(19)
    elif not memory["visited"]:
        say(1)
    memory["visited"] = True
    return image


def currentButtons():
    if view == "room":
        return list(roomButtons)
    return list(slotButtons.values()) + badgeButtons + [backButton]


########## chat line from the database ##########
def say(n, who="You"):
    fui.sendMessage(who, ROOM, n)


########## story hotspots ##########
def searchShelf():
    say(2)


def checkPhone():
    say(3)
    say(4, "Voicemail")
    say(5, "Voicemail")


def readBoard():
    say(6)
    say(7, "Whiteboard")
    say(8, "Whiteboard")
    say(9, "Whiteboard")


########## open the locked box ##########
def openBox():
    global view
    view = "box"
    refreshBadges()
    if memory["stoneTaken"]:
        say(18)
    else:
        say(10)
        if not badgeButtons:
            say(11)


########## one button per badge the player carries and has not put in the box yet ##########
def refreshBadges():
    global badgeButtons
    badgeButtons = []
    for shape in SHAPES:
        if player.has_item(shape) and not memory["placed"][shape]:
            b = u.Button(X + 420 + 110 * len(badgeButtons), 500, 100, 50, shape,
                         lambda shape=shape: pickUp(shape))
            if shape == holding:
                b.bgCol = (110, 95, 60)       # the badge in your hand
            badgeButtons.append(b)


def pickUp(shape):
    global holding
    holding = shape
    refreshBadges()
    say(13)


########## place the badge in a slot ##########
def tryPlace(shape):
    global holding
    if memory["stoneTaken"] or memory["placed"][shape]:
        return
    if holding is None:
        say(12)
    elif holding == shape:
        memory["placed"][shape] = True
        slotButtons[shape].label = shape
        holding = None
        say(15)
        if all(memory["placed"].values()):
            finishBox()
    else:
        holding = None
        say(14)
    refreshBadges()


########## all badges are in: they are used up and the stone is the reward ##########
def finishBox():
    for shape in SHAPES:
        player.remove_item(shape)
    player.add_item("Stones", "Purple", STONE_ICON)
    memory["stoneTaken"] = True       # after add_item, so a failed pickup doesn't count as taken
    say(16)
    say(17)


########## return to the main room ##########
def backToRoom():
    global view, holding
    view = "room"
    holding = None


########## leave project room and go to corridor ##########
def leave():
    global next_room
    next_room = "corridor"
