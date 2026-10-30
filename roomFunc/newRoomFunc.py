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


# a view is "room", the id of the element you are looking at, or that id with ".changed" behind it
def getElements(room):
    folder = room.FOLDER
    size = room.screen.get_size()
    images = {"room": u.load_image(folder + "room.png", size)}
    masks = {"room": []}
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
    # the people in a room, you press them in the room view: they are cut out of the room picture like the elements, but have no close-up
    for name, label, action in room.PEOPLE:
        masks["room"].append(u.Mask(folder + "masks/" + name + ".png", size, (0, 0), ACTIONS[action](room), label))
    buttons = [u.Button(1320, 650, 140, 50, "Back", lambda: back(room))]
    # the buttons a room has besides its elements, they are in the room view only
    extra = [u.Button(x, y, w, h, label, ACTIONS[action](room))
             for label, (x, y, w, h), action in room.BUTTONS]
    return images, masks, buttons, extra


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
        say(room)
    return action


# makes the action for a close-up: pressing it changes the picture and tells what you found
def inspect(room, name):
    def action():
        room.player.addCompletion("SecondaryRooms", room.key + "." + name, "")
        room.view = name + ".changed"
        say(room)
    return action


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


# makes the action for the lady at the front desk: she takes the necklace, and the game ends
def giveNecklace(room):
    def action():
        if not room.player.has_item("Items", "Necklace"):
            room.fui.sendMessage("You", DB_TABLE, room.key + ".necklace_missing")
            return
        room.player.remove_item("Items", "Necklace")
        room.player.addCompletion("SecondaryRooms", room.key + ".necklace", "")
        room.goTo("ending")
    return action


# what a person in a room can do, by the name used in the PEOPLE of its file: name -> function(room) that makes the action
ACTIONS = {"giveNecklace": giveNecklace}
