import UI.uiElements as u
import functions.sound as s
import functions.savingFunc as load
from functions.settingsFunc import settings as sett


def getElements(player,screen,goTo,openSettings):
    images = start(screen)
    buttons = current(player,goTo,openSettings)
    return images,buttons

def current(player,goTo,openSettings):
    return [
        u.Button(120, 420, 150, 50, "New Game", lambda: new_game(goTo)),
        u.Button(120, 470, 150, 50, "Load Game", lambda: load_game(player,goTo)),
        u.Button(120, 520, 150, 50, "Settings", openSettings),
    ]


def start(screen):
    s.play_music("assets/music/niceThomas.mp3",sett)
    return [u.load_image("assets/startup.png", (screen.get_size()[0]+300,screen.get_size()[1]))]


def load_game(player,goTo):
    load.load(player,"data/savePlayer.json")
    player.setImage()
    goTo(player.location)


def new_game(goTo):
    print("starting new game")
    goTo("frontD")
