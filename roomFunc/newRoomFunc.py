import os
import pygame
import UI.uiElements as u

# every secondary room has a file in Rooms/secondaryRooms with its folder and its elements
# the pictures of a room all have the same names inside its folder:
#   room.png                          the room itself
#   masks/<element>.png               the part of the room you press to look at an element
#   <element>/pov.png                 the close-up of an element
#   <element>/pov_changed.png         the close-up after you pressed it
#   <element>/mask.png                the part of the close-up you can press
# the text of each element is in the language files, under the name below
DB_TABLE = "NewRooms"

# every element the player already changed is saved in player.completion["SecondaryRooms"]["all"]
# as "room key.element id", for example "lab2001R.window"
def isChanged(room, name):
    return room.key + "." + name in room.player.getCompletion("SecondaryRooms")["all"]


# a picture that wasn't made yet: the game uses the fallback picture until it is in the folder
def picture(path, fallback):
    return path if os.path.exists(path) else fallback


# a view is "room", the id of the element you are looking at, or that id with ".changed" behind it
def getElements(room):
    folder = room.FOLDER
    size = room.screen.get_size()
    images = {"room": u.load_image(folder + "room.png", size)}
    masks = {"room": []}
    inputs = {}     # view -> things you type in, see CODES in the room's file
    for name, label in room.ELEMENTS:
        # mask images: full picture size, transparent except for the clickable area
        if name == "door":
            masks["room"].append(u.Mask(folder + "masks/door.png", size, (0, 0), door(room, "corridor"), label))
            continue
        masks["room"].append(u.Mask(folder + "masks/" + name + ".png", size, (0, 0), look(room, name), label))
        images[name] = u.load_image(folder + name + "/pov.png", size)
        images[name + ".changed"] = u.load_image(folder + name + "/pov_changed.png", size)
        masks[name] = [u.Mask(folder + name + "/mask.png", size, (0, 0), inspect(room, name))]
        masks[name + ".changed"] = []
        # an item that falls out of the element lies in its changed view until the player takes it, see FOUND in the room's file
        found = room.FOUND.get(name)
        if found and not isFound(room, name):
            masks[name + ".changed"] = [spriteMask(found[1], found[3], found[2], pickUp(room, name))]
        # things you can press inside a close-up, see CLICKABLES in the room's file
        # a thing whose mask picture wasn't made yet can't be pressed, a missing "then" picture shows the "on" picture instead
        for part, label, what in room.CLICKABLES.get(name, []):
            on = folder + name + "/" + what.get("on", "pov_changed") + ".png"
            for pic in (what.get("on", "pov_changed"), what.get("then")):
                if pic and viewOf(name, pic) not in images:
                    images[viewOf(name, pic)] = u.load_image(picture(folder + name + "/" + pic + ".png", on), size)
                    masks[viewOf(name, pic)] = []
            mask = folder + name + "/" + part + "_mask.png"
            if os.path.exists(mask):
                masks[viewOf(name, what.get("on", "pov_changed"))].append(u.Mask(mask, size, (0, 0), press(room, name, part), label))
        # a code you type in the changed view, the right code shows a picture of its own
        if name in room.CODES:
            answer, pic = room.CODES[name]
            images[viewOf(name, pic)] = u.load_image(picture(folder + name + "/" + pic + ".png", folder + name + "/pov_changed.png"), size)
            masks[viewOf(name, pic)] = []
            inputs[name + ".changed"] = [CodeEntry(room, name)]
    buttons = [u.Button(1320, 650, 140, 50, "Back", lambda: back(room))]
    # the buttons a room has besides its elements, they are in the room view only
    extra = [u.Button(x, y, w, h, label, lambda action=ACTIONS[action]: action(room))
             for label, (x, y, w, h), action in room.BUTTONS]
    return images, masks, buttons, extra, inputs


# a small picture, not as big as the room: the centre is relative to the room picture
def spriteMask(path, width, centre, action):
    w, h = pygame.image.load(path).get_size()
    h = round(width * h / w)
    return u.Mask(path, (width + u.startX, h), (centre[0] - width // 2, centre[1] - h // 2), action)


# the item of an element was taken, saved as "room key.element id.found"
def isFound(room, name):
    return room.key + "." + name + ".found" in room.player.getCompletion("SecondaryRooms")["all"]


# the id of a text in the language files is "room key.view", for example "lab2001R.window.changed"
def say(room):
    room.fui.sendMessage("You", DB_TABLE, room.key + "." + room.view)


# makes the action for an element: pressing it walks up to it and shows its close-up
def look(room, name):
    def action():
        room.view = name + ".changed" if isChanged(room, name) else name
        # a thing in the close-up that was already used shows the picture it left behind, for example the opened box
        moved = True
        while moved:
            moved = False
            for part, label, what in room.CLICKABLES.get(name, []):
                if what.get("then") and isDone(room, name, part) and room.view == viewOf(name, what.get("on", "pov_changed")):
                    room.view = viewOf(name, what["then"])
                    moved = True
        if name in room.CODES and isDone(room, name, "code") and room.view == name + ".changed":
            room.view = viewOf(name, room.CODES[name][1])
        say(room)
    return action


# makes the action for a close-up: pressing it changes the picture and tells what you found
def inspect(room, name):
    def action():
        room.player.addCompletion("SecondaryRooms", room.key + "." + name, "")
        room.view = name + ".changed"
        say(room)
    return action


# the view of a picture in the folder of an element: pov_changed is the changed view, any other picture is "element id.picture"
def viewOf(name, picture):
    return name + ".changed" if picture == "pov_changed" else name + "." + picture


# a thing in a close-up that only works once was used, saved as "room key.element id.thing id"
def isDone(room, name, part):
    return room.key + "." + name + "." + part in room.player.getCompletion("SecondaryRooms")["all"]


# makes the action for a thing in a close-up, what it does is in CLICKABLES in the room's file:
#   "needs": the item that opens it, it is used up    "gives": (item name, inventory icon) the player gets
#   "then": the picture shown after pressing it        "once": it stays done, saved like the elements
# its text is "room key.element id.thing id", and "...thing id.locked" when the item is missing
def press(room, name, part):
    what = next(w for p, l, w in room.CLICKABLES[name] if p == part)
    def action():
        textId = room.key + "." + name + "." + part
        if what.get("once") and isDone(room, name, part):
            return
        if what.get("needs"):
            if not room.player.has_item("Items", what["needs"]):
                room.fui.sendMessage("You", DB_TABLE, textId + ".locked")
                return
            room.player.remove_item("Items", what["needs"])
        if what.get("gives"):
            room.player.add_item("Items", *what["gives"])
        if what.get("once"):
            room.player.addCompletion("SecondaryRooms", textId, "")    # after add_item, so a failed pickup doesn't count as taken
        if what.get("then"):
            room.view = viewOf(name, what["then"])
        room.fui.sendMessage("You", DB_TABLE, textId)
    return action


# a text field and an Enter button in a close-up, for the codes in CODES of the room's file
# the right code is saved as "room key.element id.code", its text is "room key.element id.picture", a wrong code says "...code.wrong"
class CodeEntry:
    def __init__(self, room, name):
        self.room = room
        self.name = name
        self.field = u.TextField(1000, 650, 200, 50, outline=True)
        self.field.focus = True     # you can type right away
        self.button = u.Button(1210, 650, 100, 50, "Enter", self.check)

    def check(self):
        room = self.room
        answer, pic = room.CODES[self.name]
        if self.field.text.strip().upper() != answer.upper():
            self.field.text = ""
            room.fui.sendMessage("You", DB_TABLE, room.key + "." + self.name + ".code.wrong")
            return
        self.field.text = ""
        room.player.addCompletion("SecondaryRooms", room.key + "." + self.name + ".code", "")
        room.view = viewOf(self.name, pic)
        say(room)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER) and self.field.focus:
            self.check()
            return
        if not (event.type == pygame.TEXTINPUT and len(self.field.text) >= 10):
            self.field.handle_event(event)
        self.button.handle_event(event)

    def draw(self, screen):
        self.field.draw(screen)
        self.button.draw2(screen)


# makes the action for the item that fell out of an element: pressing it puts the item in the inventory
def pickUp(room, name):
    def action():
        item, path = room.FOUND[name][:2]
        room.player.add_item("Items", item, path)
        room.player.addCompletion("SecondaryRooms", room.key + "." + name + ".found", "")   # after add_item, so a failed pickup doesn't count as taken
        room.elements[name + ".changed"].clear()                # it is not on the floor anymore
        room.fui.sendMessage("You", DB_TABLE, room.key + "." + name + ".found")
    return action


# makes the action for a door: pressing it sends the player to that room
def door(room, to):
    return lambda: room.goTo(to)


def back(room):
    room.view = "room"


# the lady at the front desk takes the necklace, and the game ends
def giveNecklace(room):
    if not room.player.has_item("Items", "Necklace"):
        room.fui.sendMessage("You", DB_TABLE, room.key + ".necklace_missing")
        return
    room.player.remove_item("Items", "Necklace")
    room.player.addCompletion("SecondaryRooms", room.key + ".necklace", "")
    room.goTo("ending")


# the actions a room can give to its buttons, by the name used in the BUTTONS of its file
ACTIONS = {"giveNecklace": giveNecklace}
