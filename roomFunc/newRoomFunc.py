import json
import UI.uiElements as u

# every new room is described in rooms.json: its picture and its elements
# the text of each element is in the language files, under the name below
with open("data/rooms.json") as f:
    ROOMS = {room["key"]: room for room in json.load(f)["rooms"]}

DB_TABLE = "NewRooms"

# (room key, element id) of every element the player already changed, stays until the game closes
changed = set()


# a view is "room", the id of the element you are looking at, or that id with ".changed" behind it
def getElements(room):
    data = ROOMS[room.key]
    size = room.screen.get_size()
    images = {"room": u.load_image(data["image"], size)}
    masks = {"room": []}
    for element in data["elements"]:
        name = element["id"]
        if name == "door":
            masks["room"].append(u.Mask(element["mask"], size, (0, 0), door(room, "corridor"), element["label"]))
            continue
        # mask images: full picture size, transparent except for the clickable area
        masks["room"].append(u.Mask(element["mask"], size, (0, 0), look(room, name), element["label"]))
        images[name] = u.load_image(element["pov"]["image"], size)
        images[name + ".changed"] = u.load_image(element["pov"]["changed"], size)
        masks[name] = [u.Mask(element["pov"]["mask"], size, (0, 0), inspect(room, name))]
        masks[name + ".changed"] = []
    buttons = [u.Button(1320, 650, 140, 50, "Back", lambda: back(room))]
    return images, masks, buttons


# the id of a text in the language files is "room key.view", for example "lab2001R.window.changed"
def say(room):
    room.fui.sendMessage("You", DB_TABLE, room.key + "." + room.view)


# makes the action for an element: pressing it walks up to it and shows its close-up
def look(room, name):
    def action():
        room.view = name + ".changed" if (room.key, name) in changed else name
        say(room)
    return action


# makes the action for a close-up: pressing it changes the picture and tells what you found
def inspect(room, name):
    def action():
        changed.add((room.key, name))
        room.view = name + ".changed"
        say(room)
    return action


# makes the action for a door: pressing it sends the player to that room
def door(room, to):
    return lambda: room.goTo(to)


def back(room):
    room.view = "room"
