import UI.uiElements as u
import functions.sound as s
import functions.savingFunc as load
from functions.settingsFunc import settings as sett

images = []
buttons = []
next_room = None
player = None
bgMusic = "assets/music/niceThomas.mp3"

def getElements(p,screen):
    global player
    player = p
    start(screen)
    current()
    return images,buttons

def current():
    global buttons
    buttons = [
        u.Button(120, 420, 150, 50, "New Game", new_game),
        u.Button(120, 470, 150, 50, "Load Game", load_game),
        u.Button(120, 520, 150, 50, "Settings", settings),
    ]


def start(screen):
    global images
    images = [u.load_image("assets/startup.png", (screen.get_size()[0]+300,screen.get_size()[1]))]
    s.play_music(bgMusic,sett)


def load_game():
    global next_room
    load.load(player,"data/savePlayer.json")
    player.setImage()
    next_room = player.location


def new_game():
    global next_room
    print("starting new game")
    next_room = "frontD"


def settings():
    print("entering settings menu")
