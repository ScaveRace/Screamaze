import UI.uiElements as u
import functions.sound as s
import functions.savingFunc as load
from functions.settingsFunc import settings as sett


def getElements(player,screen,goTo,openSettings,openLeaderboard):
    images = start(screen)
    buttons = current(player,goTo,openSettings,openLeaderboard)
    return images,buttons

def current(player,goTo,openSettings,openLeaderboard):
    return [
        u.Button(120, 420, 150, 50, "New Game", lambda: new_game(goTo)),
        u.Button(120, 470, 150, 50, "Load Game", lambda: load_game(player,goTo)),
        u.Button(120, 520, 150, 50, "Settings", openSettings),
        u.Button(120, 570, 150, 50, "Leaderboard", openLeaderboard),
    ]


def start(screen):
    s.play_music("assets/music/The_Unmarked_Door.mp3",sett, .4)
    return [u.load_image("assets/startup.png", (screen.get_size()[0]+300,screen.get_size()[1]))]


def load_game(player,goTo):
    load.load(player,"data/savePlayer.json")
    player.setImage()
    goTo(player.location)


def new_game(goTo):
    print("starting new game")
    goTo("frontD")
