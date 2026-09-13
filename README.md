# Thuas' Screamaze

A Pygame escape-room game. The player moves from room to room, solves what's in each one and
works their way out of the building.

This file is what a new person on the team reads first. The full Git and GitHub workflow is in
`docs/github-guide.pdf`.

---

## Requirements

- **Python 3.13.** Not 3.14 — pygame 2.6.1 has no ready-made install for it and `pip install`
  fails with a long red error.
- Git.

```
py -3.13 --version        # Windows
python3.13 --version      # macOS and Linux
```

---

## Getting started

```
git clone https://github.com/<owner>/<repo>.git
cd <repo>
```

| | Windows (PowerShell) | macOS and Linux |
|---|---|---|
| Create the environment | `py -3.13 -m venv .venv` | `python3.13 -m venv .venv` |
| Install pygame | `.venv\Scripts\python -m pip install -r requirements.txt` | `.venv/bin/python -m pip install -r requirements.txt` |
| Run the game | `.venv\Scripts\python main.py` | `.venv/bin/python main.py` |

In PyCharm: **Settings → Project → Python Interpreter → Add Interpreter → Add Local Interpreter →
Virtualenv**, base interpreter Python 3.13, location `.venv`.
In VS Code: `Ctrl+Shift+P` → **Python: Create Environment → Venv → Python 3.13**, tick
`requirements.txt`.

`ModuleNotFoundError: No module named 'pygame'` means your editor is running a different Python
than the one in `.venv`.

---

## Project structure

```
main.py                  the window, the game loop, and the list of rooms
UI/uiElements.py         Button, TextField, load_image, animations — shared by everyone
menu/
  startupMenu.py         new game / load game / settings
  pauseMenu.py
  settingsMenu.py        volume, auto-text
Rooms/
  orientRoom.py          READ THIS FIRST — the commented example room
  frontDesk.py           character creation
  ghostRoom.py
  corridor.py
  lab2001.py
functions/sound.py       play_music, play_sound
data/saver.py            save data (work in progress)
assets/                  images and sounds
docs/                    sprint documents and the GitHub guide
```

**You own your own room file and your own assets.** Nobody else edits them, and you don't edit
anyone else's. That is what keeps merge conflicts away.

---

## Running

```
python main.py
```

Ask whoever owns `main.py` to add a way to start directly in one room (`python main.py frontD`).
It saves everyone from clicking through the menu every time they test their own room, and it lets
five rooms be built at the same time even when the rooms before yours don't exist yet.

---

## Adding a room

`Rooms/orientRoom.py` is the commented template — copy it and read the comments. The short
version:

1. Copy `Rooms/orientRoom.py` to `Rooms/<yourRoom>.py`.
2. Rename the class to your room's name.
3. Put your images in `assets/` and load them in `__init__`.
4. Register your room in `main.py` (ask the owner of that file — this is the one shared line you
   have to add).

```python
import pygame
import UI.uiElements as u


class YourRoom:
    def __init__(self, screen):
        self.screen = screen          # keep the screen for draw()
        self.next_room = None         # must exist, must start as None
        self.image = u.load_image("assets/yourRoom.png", screen.get_size())
        self.buttons = [
            u.Button(930, 350, 140, 50, "Continue", self.action),
        ]

    def action(self):
        print("button pressed")

    def handle_event(self, event):    # called by main.py every frame
        for b in self.buttons:
            b.handle_event(event)

    def draw(self):                   # called by main.py every frame
        self.screen.blit(self.image, (0, 0))
        for b in self.buttons:
            b.draw2(self.screen)
```

### The room contract

Every room **must**:

- be a class in its own file in `Rooms/`
- take `screen`: `def __init__(self, screen)`, and store it as `self.screen`
- set `self.next_room = None` in `__init__`
- have `handle_event(self, event)` and `draw(self)` — `main.py` calls both every frame
- load images, fonts and sounds in `__init__`, never inside `draw()`
- leave the room by setting `self.next_room = "<the other room's key>"`

Every room **must not**:

- contain a `while` loop, or call `pygame.display.set_mode`, `clock.tick`, `pygame.display.flip`
  or `pygame.quit` — `main.py` owns the loop and the window
- import another room (`from Rooms import frontDesk` inside a room or menu creates circular
  imports and breaks as soon as that room changes). Use `self.next_room` instead.
- edit files outside its own room in the same pull request

Note: buttons are drawn with `b.draw2(self.screen)`, not `b.draw()`. Check `UI/uiElements.py` for
the argument order of `Button` and `TextField` before you write a long list of them — it differs
between existing rooms, so copy from `orientRoom.py`, not from an older file.

### Naming

Room file names and keys: letters and digits, camelCase, starting with a letter — `frontDesk`,
`ghostRoom`, `lab2001`. No dots, spaces or dashes; Python cannot import them.

Write asset paths exactly as the file is named. Windows and macOS ignore capitalisation, Linux
does not, so `assets/FrontDesk_1.png` works on one laptop and crashes on another.

---

## Working together

Full details in `docs/github-guide.pdf`. The short version:

1. **Never work on `main`.** Branch, push, open a pull request, get one review.
2. One task, one branch, one pull request. Branches live one to three days, not a whole sprint.
3. Stay in your own room file. Shared files (`main.py`, `UI/`, `menu/`, `functions/`, `data/`)
   get their own small pull request, announced in the group chat first.
4. Pull `main` into your branch every day.
5. Read `git status` before every commit. Never commit `__pycache__`, `.venv`, `.idea`, or save
   files — see `.gitignore`.

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

| Area | File | Owner | Reviewer |
|---|---|---|---|
| Front desk | `Rooms/frontDesk.py` | Fynn | |
| Ghost room | `Rooms/ghostRoom.py` | Jill | |
| Lab 2.001 | `Rooms/lab2001.py` | Alexander | |
| Corridor | `Rooms/corridor.py` | Fynn | |
| Menus | `menu/` | Collaboration | |
| UI elements | `UI/uiElements.py` | Collaboration | |
| main.py and the room list | `main.py` | / | |
| Sound | `functions/sound.py` | | |
| Save data | `data/saver.py` | | |

Fill this in during sprint planning: one owner per area, and a reviewer who isn't the owner.
