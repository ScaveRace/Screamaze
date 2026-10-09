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

# (room key, element id) of every element the player already changed, stays until the game closes
changed = set()


# a view is "room", the id of the element you are looking at, or that id with ".changed" behind it
def getElements(room):
    folder = room.data.FOLDER
    size = room.screen.get_size()
    images = {"room": u.load_image(folder + "room.png", size)}
    masks = {"room": []}
    for name, label in room.data.ELEMENTS:
        # mask images: full picture size, transparent except for the clickable area
        if name == "door":
            masks["room"].append(u.Mask(folder + "masks/door.png", size, (0, 0), door(room, "corridor"), label))
            continue
        masks["room"].append(u.Mask(folder + "masks/" + name + ".png", size, (0, 0), look(room, name), label))
        images[name] = u.load_image(folder + name + "/pov.png", size)
        images[name + ".changed"] = u.load_image(folder + name + "/pov_changed.png", size)
        masks[name] = [u.Mask(folder + name + "/mask.png", size, (0, 0), inspect(room, name))]
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
