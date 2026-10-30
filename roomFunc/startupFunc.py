import glob
import os
import subprocess
import sys
import webbrowser
import UI.uiElements as u
import functions.sound as s
import functions.savingFunc as load
from functions.settingsFunc import settings as sett

AI_FOLDER = "AI/"
AI_LINK = "https://huggingface.co/Sacve/Screamaze_Qwen3.5_2B_Q4_K_M.gguff/resolve/main/game-q4_k_m.gguf"    # the browser downloads the model from here


def getElements(player,screen,goTo,openSettings,openLeaderboard):
    images = start(screen)
    buttons = current(player,goTo,openSettings,openLeaderboard)
    return images,buttons

def current(player,goTo,openSettings,openLeaderboard):
    buttons = [
        u.Button(120, 420, 150, 50, "New Game", lambda: new_game(player,goTo)),
        u.Button(120, 470, 150, 50, "Load Game", lambda: load_game(player,goTo)),
        u.Button(120, 520, 150, 50, "Settings", openSettings),
        u.Button(120, 570, 150, 50, "Leaderboard", openLeaderboard),
    ]
    if not aiInstalled():       # only there until a .gguf is in the AI folder: download it, then put it in the folder
        buttons.append(u.Button(120, 620, 150, 50, "Download AI", lambda: webbrowser.open(AI_LINK)))
        buttons.append(u.Button(120, 670, 150, 50, "Open AI folder", openAiFolder))
    return buttons


def aiInstalled():
    return len(glob.glob(AI_FOLDER + "*.gguf")) > 0


def openAiFolder():
    folder = os.path.abspath(AI_FOLDER)
    if sys.platform == "win32":
        os.startfile(folder)
    else:
        subprocess.Popen(["open" if sys.platform == "darwin" else "xdg-open", folder])


def start(screen):
    s.play_music("assets/music/The_Unmarked_Door.mp3",sett, .4)
    return [u.load_image("assets/startup.png", (screen.get_size()[0]+300,screen.get_size()[1]))]


def load_game(player,goTo):
    if not load.is_json_empty("data/savePlayer.json"):
        player.reset()
    load.load(player,"data/savePlayer.json")
    player.setImage()
    goTo(player.location)


def new_game(player,goTo):
    print("starting new game")
    player.reset()
    goTo("frontD")
