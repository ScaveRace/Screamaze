# Thuas' Screamaze

A Pygame point-and-click escape-room game set in a THUAS school building. You create a character
at the front desk, walk the corridor, enter the rooms behind its doors, solve each room's puzzle
and collect a coloured stone from each one.

This file is what a new person on the team reads first.

---

## Requirements

- **Python 3.13.** Not 3.14 — pygame 2.6.1 has no ready-made install for it and `pip install`
  fails with a long red error.
- **pygame 2.6.1.** It is the only dependency (`json` comes with Python).
- Git.

```
py -3.13 --version        # Windows
python3.13 --version      # macOS and Linux
```

---

## Getting started

```
git clone https://github.com/ScaveRace/Screamaze.git
cd Screamaze
```

| | Windows (PowerShell) | macOS and Linux |
|---|---|---|
| Create the environment | `py -3.13 -m venv .venv` | `python3.13 -m venv .venv` |
| Install pygame | `.venv\Scripts\python -m pip install pygame==2.6.1` | `.venv/bin/python -m pip install pygame==2.6.1` |
| Run the game | `.venv\Scripts\python main.py` | `.venv/bin/python main.py` |

Run the game from the project folder: all asset and data paths are relative to it.

In PyCharm: **Settings → Project → Python Interpreter → Add Interpreter → Add Local Interpreter →
Virtualenv**, base interpreter Python 3.13, location `.venv`.
In VS Code: `Ctrl+Shift+P` → **Python: Create Environment → Venv → Python 3.13**.

`ModuleNotFoundError: No module named 'pygame'` means your editor is running a different Python
than the one in `.venv`.

---

## Playing

| | |
|---|---|
| Click | Buttons, doors and objects. Hover over something clickable to see it highlighted. |
| Type + `Enter` | Click the chat first, then type. Used for riddle answers. |
| Mouse wheel over the chat | Scroll back through older messages. |
| `Esc` or the **pause** button | Pause menu: music volume, sound-effect volume, save game, resume. |
| **Inventory** button | Shows the items you carry. |

The timer at the top only runs while the game is not paused.

**Load Game** on the start screen continues from `data/savePlayer.json`, in the room you saved in.
Volume settings are stored in `data/gameSettings.json` every time you move a slider.

The window can be resized. The game always renders at 1480×720 and pygame scales that picture to
the window, keeping the aspect ratio.

---

## Project structure

```
main.py                    the window, the game loop, the timer and the ROOMS dictionary
player.py                  Player: name, gender, time, location, inventory
UI/
  uiElements.py            Button, Chatbox, TextField, Mask, Slider, load_image — shared by everyone
  frontUI.py               the overlay drawn on top of every room: side chat, timer, pause, inventory
  pauseMenu.py             pause panel with volume sliders and save
menu/
  startupMenu.py           new game / load game / settings
  inventory.py             inventory panel
Rooms/
  frontDesk.py             character creation (name and gender)
  corridor.py              the hub: every door is a clickable mask
  ghostRoom.py             teacher's homework and a keypad cabinet      -> white stone
  vampireRoom.py           fuses and a fuse box                         -> red stone
  storrageRoom.py          quiz at the desk                             -> green stone
  equinoxRoom.py           three riddles from a hungry student          -> yellow stone
  projectRoom.py           hidden shapes and a puzzle box
  endingRoom.py            placeholder, not written yet
functions/
  uiFunc.py                text wrapping and text-input helpers
  sound.py                 play_music, play_sound
  settingsFunc.py          the shared `settings` object (volumes, language)
  savingFunc.py            save / load any object to JSON
  language.py              chatMessage: reads dialogue from the language files
data/
  playerLogistics.py       DOOR_SPAWNS: where the player stands in front of each corridor door
  languages/en.json        dialogue in english, room -> id -> text
  languages/nl.json        the same dialogue in dutch
  savePlayer.json          the save file
  gameSettings.json        volume and language settings
assets/                    images, masks and music
```

Room keys used in `main.py` and in `self.next_room`:

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

**You own your own room file and your own assets.** Nobody else edits them, and you don't edit
anyone else's. That is what keeps merge conflicts away.

---

## Adding a room

1. Create `Rooms/<yourRoom>.py` with one class in it (skeleton below).
2. Put your images in `assets/` (a subfolder per room, like `assets/vampire/`) and load them in
   `__init__`.
3. Register the room in the `ROOMS` dictionary in `main.py` — this is the one shared line you
   have to add.
4. Point a corridor door at it: in `Rooms/corridor.py`, give the door's `Mask` an action that sets
   `self.next_room` to your key.

```python
import pygame
import UI.uiElements as u


class YourRoom:
    def __init__(self, screen, player, fui):
        self.screen = screen          # keep the screen for draw()
        self.player = player
        self.fui = fui                # the overlay: side chat, pause, inventory
        self.next_room = None         # must exist, must start as None
        self.image = u.load_image("assets/yourRoom.png", screen.get_size())
        self.buttons = [
            u.Button(930, 350, 140, 50, "Leave", self.leave),
        ]
        self.masks = [
            u.Mask("assets/yourRoom/door.png", screen.get_size(), (0, 0), self.leave, "Door"),
        ]

    def leave(self):
        self.next_room = "corridor"

    def handle_event(self, event):    # called by main.py for every event
        for b in self.buttons:
            b.handle_event(event)
        for m in self.masks:
            m.handle_event(event)

    def draw(self):                   # called by main.py every frame
        self.screen.blit(self.image, (300, 0))   # to the right of the side chat
        for m in self.masks:
            m.draw(self.screen)
        for b in self.buttons:
            b.draw2(self.screen)
```

### The room contract

Every room **must**:

- be a class in its own file in `Rooms/`
- take `def __init__(self, screen, player, fui)` — `main.py` creates every room except the start
  menu and the front desk with these three arguments
- set `self.next_room = None` in `__init__`
- have `handle_event(self, event)` and `draw(self)` — `main.py` calls both
- load images, fonts and sounds in `__init__`, never inside `draw()`
- leave the room by setting `self.next_room = "<the other room's key>"`

Every room **must not**:

- contain a `while` loop, or call `pygame.display.set_mode`, `clock.tick`, `pygame.display.flip`
  or `pygame.quit` — `main.py` owns the loop and the window
- import another room. Use `self.next_room` instead.
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
| `Chatbox(x, y, w, h, font)` | Message list with a text input | `c.draw(screen)` |
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

- `GhostRoom`, `StorrageRoom` and `ProjectRoom` still take `(screen, player)` without `fui`, while
  `main.py` passes three arguments. They need the third parameter added.
- Most corridor doors without a room of their own currently lead to the vampire room.
- The **Settings** button on the start screen does nothing yet; the volume sliders are in the
  pause menu.
- There is no `.gitignore` or `requirements.txt` yet, and `__pycache__` files are tracked in Git.

---

## Working together

1. **Never work on `main`.** Branch, push, open a pull request, get one review.
2. One task, one branch, one pull request. Keep branches short-lived.
3. Stay in your own room file. Shared files (`main.py`, `player.py`, `UI/`, `menu/`, `functions/`,
   `data/`) get their own small pull request, announced in the group chat first.
4. Pull `main` into your branch every day.
5. Read `git status` before every commit. Don't commit `__pycache__`, `.venv`, `.idea` or your
   own save file.

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
