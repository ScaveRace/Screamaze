# Thuas' Screamaze

A Pygame point-and-click escape-room game set in a THUAS school building. You create a character
at the front desk, walk the corridor, enter the rooms behind its doors, solve each room's puzzle
and collect a coloured stone from each one.

This file is what a new person on the team reads first.

---

## Install

You need **Python 3.13** and **Git**. Not Python 3.14: pygame 2.6.1 has no ready-made install for
it and `pip install` fails with a long red error.

```
py -3.13 --version        # Windows
python3.13 --version      # macOS and Linux
```

### 1. Get the game

```
git clone https://github.com/ScaveRace/Screamaze.git
cd Screamaze
```

### 2. Install the packages

| | Windows (PowerShell) | macOS and Linux |
|---|---|---|
| Create the environment | `py -3.13 -m venv .venv` | `python3.13 -m venv .venv` |
| Install everything | `.venv\Scripts\python -m pip install -r requirements.txt` | `.venv/bin/python -m pip install -r requirements.txt` |

`requirements.txt` holds **pygame** (the game) and **llama-cpp-python** (runs the AI). If
llama-cpp-python does not install, open `requirements.txt`, delete its last two lines and run
the command again: the game works without it, only the AI chat does not.

### 3. Run it

| | Windows (PowerShell) | macOS and Linux |
|---|---|---|
| Run the game | `.venv\Scripts\python main.py` | `.venv/bin/python main.py` |

Run the game from the project folder: all asset and data paths are relative to it.

In PyCharm: **Settings → Project → Python Interpreter → Add Interpreter → Add Local Interpreter →
Virtualenv**, base interpreter Python 3.13, location `.venv`.
In VS Code: `Ctrl+Shift+P` → **Python: Create Environment → Venv → Python 3.13**.

`ModuleNotFoundError: No module named 'pygame'` means your editor is running a different Python
than the one in `.venv`.

---

## The AI (ARIA)

ARIA answers questions about the game in the **globe** app of the phone. The model is too big for
git, so it is not in the repository: you download it once.

| Model | Size | For |
|---|---|---|
| `game-f16.gguf` | 3.6 GB | the standard, full precision |
| `game-q4_k_m.gguf` | 1.2 GB | the smaller brother, for weak computers |

1. Start the game. While there is no `.gguf` in the `AI/` folder, the start screen shows three
   buttons: **Download AI** (the standard model), **Small AI** (the small one) and
   **Open AI folder**.
2. Press one of the download buttons. Your browser downloads the file from Hugging Face
   (`Sacve/Screamaze_Qwen3.5_2B_Q4_K_M.gguff`).
3. Press **Open AI folder** and put the `.gguf` file in it. Restart the game.

If both files are in `AI/`, the game uses the full one. The model loads in the background while
you are in the menus. The first answers can be slow on a weak computer.

ARIA does not know the game by heart. For each question `AI/aria.py` looks up 3 facts in
`AI/lore.json` by keyword and puts them in the prompt, so a new puzzle needs a new entry there.

---

## Playing

| | |
|---|---|
| Click | Buttons, doors and objects. Hover over something clickable to see it highlighted. |
| Type + `Enter` | Click the chat first, then type. Used for riddle answers and for ARIA. |
| Mouse wheel over the chat | Scroll back through older messages. |
| `Esc` or the **pause** button | Pause menu: save game, resume. |
| **Phone** (left side) | **Globe** ARIA, **chat** the talks of the characters, **gear** volume and language, **handset** a keypad (try 911), **briefcase** your items. The button under the phone goes back to its home screen. |

The timer on the phone only runs while the game is not paused. The battery shows how far you are.

**Load Game** on the start screen continues from `data/savePlayer.json`, in the room you saved in.
Volume and language are stored in `data/gameSettings.json` every time you change them. All buttons,
labels and texts follow the chosen language (English or Dutch).

The window can be resized. The game always renders at 1480×720 and pygame scales that picture to
the window, keeping the aspect ratio.

---

## Project structure

```
main.py                    the window, the game loop and the timer; finds rooms in the registry
player.py                  Player: name, gender, time, location, inventory
UI/
  uiElements.py            Button, Chatbox, TextField, Mask, Slider, load_image — shared by everyone
  frontUI.py               the overlay drawn on top of every room: phone, pause button, inventory
  leaderboard.py           the leaderboard panel of the start screen
  pauseMenu.py             pause panel with volume sliders and save
AI/
  aria.py                  ARIA: loads the .gguf model, finds the facts, answers in a background thread
  lore.json                the game facts ARIA looks up by keyword
  aria_knowledge.json      the line the model was trained with
Phone/
  PhoneUI.py               the phone on the left: shows one page at a time (PAGES = name -> class)
  pages/                   homescreen, browser (ARIA), chatPage, settingsPage, dialerPage
roomFunc/                  the puzzle code of each room, next to its Rooms/ file
menu/
  startupMenu.py           new game / load game / settings (a room: key "startup")
  endingScreen.py          the end of the game and the leaderboard (a room: key "ending")
  inventory.py             inventory panel
Rooms/
  baseRoom.py              BaseRoom, the @register decorator and the REGISTRY of all rooms
  __init__.py              load_all(): imports every room file so each one registers itself
  newRooms.py              NewRoom: the base of the secondary rooms, which only hold data
  secondaryRooms/          the 12 small rooms (lab, classrooms, teacher rooms ...), data only
  frontDesk.py             character creation (name and gender)
  corridor.py              the hub: every door is a clickable mask
  ghostRoom.py             teacher's homework and a keypad cabinet      -> white stone
  vampireRoom.py           fuses and a fuse box                         -> red stone
  storrageRoom.py          quiz at the desk                             -> green stone
  equinoxRoom.py           three riddles from a hungry student          -> yellow stone
  projectRoom.py           hidden shapes and a puzzle box
functions/
  uiFunc.py                text wrapping and text-input helpers
  sound.py                 play_music, play_sound
  settingsFunc.py          the shared `settings` object (volumes, language)
  savingFunc.py            save / load any object to JSON
  language.py              chatMessage and ui(): read dialogue and button texts from the language files
  leaderboard.py           saves finished runs in data/leaderboard.db
data/
  playerLogistics.py       DOOR_SPAWNS: where the player stands in front of each corridor door
  languages/en.json        dialogue in english, room -> id -> text, and a Buttons table: the labels
  languages/nl.json        the same in dutch
  savePlayer.json          the save file
  gameSettings.json        volume and language settings
assets/                    images, masks and music
```

Room keys used in `goTo("...")`, in saves and in the language files (never rename one):

| Key | Room |
|---|---|
| `startup` | `StartupMenu` |
| `frontD` | `FrontDesk` |
| `corridor` | `Corridor` |
| `ghostR` | `GhostRoom` |
| `vampR` | `VampireRoom` |
| `storrR` | `StorrageRoom` |
| `equinR` | `EquinoxRoom` |
| `projRoom` | `ProjectRoom` |
| `teacherR` | `TeacherRoom` |
| `ending` | `EndingScreen` |
| `lab2001R`, `frontDeskR`, `class2021R`, `class2031R`, `class2035R`, `stairR`, `teach1R` - `teach4R`, `projRoom1R`, `projRoom2R` | the secondary rooms in `Rooms/secondaryRooms/` |

**You own your own room file and your own assets.** Nobody else edits them, and you don't edit
anyone else's. That is what keeps merge conflicts away.

---

## Adding a room

No change to `main.py` is needed: a room registers itself and `main.py` finds it by its key.

1. Create `Rooms/<yourRoom>.py` with one class that extends `BaseRoom`, has `@register` above it
   and a `key` (skeleton below).
2. Put your images in `assets/` (a subfolder per room, like `assets/vampire/`) and load them in
   `__init__`.
3. Point a door at it: a button or mask action that calls `self.goTo("yourKey")`, for example in
   `Rooms/corridor.py`.

```python
import UI.uiElements as u
from Rooms.baseRoom import BaseRoom, register


@register
class YourRoom(BaseRoom):
    key = "yourRoom"              # the name used in goTo("yourRoom"), saves and language files
    show_ui = True                # False = no side chat, pause button or inventory

    def __init__(self, screen, player, fui):
        super().__init__(screen, player, fui)   # sets self.screen, self.player, self.fui, self.next_room
        self.image = u.load_image("assets/yourRoom.png", screen.get_size())
        self.buttons = [
            u.Button(930, 350, 140, 50, "Leave", lambda: self.goTo("corridor")),
        ]
        self.masks = [
            u.Mask("assets/yourRoom/door.png", screen.get_size(), (0, 0), lambda: self.goTo("corridor"), "Door"),
        ]

    def on_enter(self):               # optional: runs every time the player walks in
        pass

    def handle_event(self, event):    # optional: called by main.py for every event
        for b in self.buttons:
            b.handle_event(event)
        for m in self.masks:
            m.handle_event(event)

    def draw(self):                   # optional: called by main.py every frame
        self.screen.blit(self.image, (300, 0))   # to the right of the side chat
        for m in self.masks:
            m.draw(self.screen)
        for b in self.buttons:
            b.draw2(self.screen)
```

A small room that is only pictures and clickable elements extends `NewRoom` instead and holds
only data, like the files in `Rooms/secondaryRooms/`:

```python
from Rooms.baseRoom import register
from Rooms.newRooms import NewRoom


@register
class Lab2001(NewRoom):
    key = "lab2001R"
    FOLDER = "assets/lab_2001/"
    ELEMENTS = [("window", "Window"), ("door", "Leave room")]
```

### The room contract

Every room **must**:

- be a class that extends `BaseRoom` (or `NewRoom`), with `@register` and a unique `key`, in its
  own file in `Rooms/` or `Rooms/secondaryRooms/`
- take `def __init__(self, screen, player, fui)` and call `super().__init__(screen, player, fui)`;
  `main.py` creates every room with these three arguments
- override `handle_event(self, event)` and `draw(self)` if it reacts to the player or draws
  anything (`BaseRoom` has empty versions of both, and of `on_enter`)
- load images, fonts and sounds in `__init__`, never inside `draw()`
- leave the room with `self.goTo("<the other room's key>")`

Every room **must not**:

- contain a `while` loop, or call `pygame.display.set_mode`, `clock.tick`, `pygame.display.flip`
  or `pygame.quit` — `main.py` owns the loop and the window
- import another room. Use `self.goTo` instead.
- draw the timer, pause button or inventory itself — `frontUI` draws those on top of every room
- edit files outside its own room in the same pull request

### Coordinates and images

Everything is positioned in the fixed **1480×720** game resolution, also when the window is
resized. The left 300 pixels are taken by the side chat (`startX` in `UI/uiElements.py`), so
`load_image(path, screen.get_size())` returns a 1180×720 background that you blit at `(300, 0)`,
as the corridor does. A `Mask` shifts itself right by the same 300 pixels, so a full-size mask
PNG with position `(0, 0)` lines up with that background.

### UI elements (`UI/uiElements.py`)

| Element | What it is | Draw with |
|---|---|---|
| `Button(x, y, w, h, label, action)` | Text button, runs `action` on click | `b.draw2(screen)` |
| `Mask(image, size, pos, action, label)` | Clickable shape taken from a PNG: only the non-transparent pixels react, and the label shows on hover | `m.draw(screen)` |
| `Chatbox(x, y, w, h)` | Message list with a text input, shown on the phone's chat page. Rooms add to it through `fui.chat.sayKey(who, table, id)` | `c.draw(screen)` |
| `TextField(x, y, w, h, ...)` | Single text input | `t.draw(screen)` |
| `Slider(x, y, w, h, label, action, action2, value)` | Used for the volume sliders | `s.draw(screen)` |

Note that buttons are drawn with `draw2`, everything else with `draw`.

### Chat messages

`chatbox.say("Vampire > I was sleeping.")` — one string, with the speaker in front of `" > "`.
The chatbox splits on that: the name is drawn once and wrapped lines line up under the text.
A message without `" > "` (narration such as `"* The room smells of toasted bread."`) uses the
full width. The mouse wheel scrolls the chat, and a new message jumps back to the bottom.

To write into the side chat from a room, with text taken from the language files:

```python
self.fui.sendMessage("Vampire", "VampireRoom", "msg_1")   # speaker, room, id of the text
```

### Inventory and sound

```python
self.player.add_item("Stones", "Red", "assets/stones/red.png")    # or "Items"

import functions.sound as s
from functions.settingsFunc import settings as sett
s.play_music("assets/music/The_Unmarked_Door.mp3", sett, 0.4)     # loops, volume 0–1
s.play_sound("assets/yourSound.wav", sett)
```

### Naming

Room file names and keys: letters and digits, camelCase, starting with a letter — `frontDesk`,
`ghostRoom`. No dots, spaces or dashes; Python cannot import them.

Write asset paths exactly as the file is named. Windows and macOS ignore capitalisation, Linux
does not, so `assets/FrontDesk_1.png` works on one laptop and crashes on another.

---

## Known issues

- The Dutch texts are not checked by a native speaker yet.

---

## Working together

1. **Never work on `main`.** Branch, push, open a pull request, get one review.
2. One task, one branch, one pull request. Keep branches short-lived.
3. Stay in your own room file. Shared files (`main.py`, `player.py`, `UI/`, `menu/`, `functions/`,
   `data/`) get their own small pull request, announced in the group chat first.
4. Pull `main` into your branch every day.
5. Read `git status` before every commit. Don't commit `__pycache__`, `.venv`, `.idea` or your
   own save file. The `.gitignore` already skips `__pycache__`, `.venv`, `.idea` and the
   `.gguf` models: never add a model to git, it is bigger than GitHub allows.

```
git switch main
git pull
git switch -c room/ghostroom-dialogue

# ... work, then:
git status
git add Rooms/ghostRoom.py assets/
git commit -m "ghostRoom: teacher dialogue"
git push -u origin room/ghostroom-dialogue
```

Then open a pull request on GitHub and ask someone to review it.

---

## Who owns what

Taken from who has committed most to each file — correct it during sprint planning.

| Area | File | Owner (Git name) |
|---|---|---|
| Front desk | `Rooms/frontDesk.py` | fynnherr |
| Corridor | `Rooms/corridor.py` | fynnherr |
| Project room | `Rooms/projectRoom.py` | fynnherr |
| Ghost room | `Rooms/ghostRoom.py` | Jill |
| Vampire room | `Rooms/vampireRoom.py` | Hadi |
| Storage room | `Rooms/storrageRoom.py` | Cesar |
| Equinox room | `Rooms/equinoxRoom.py` | mcmrg |
| Menus, UI, `main.py`, functions, data | shared | Collaboration |
