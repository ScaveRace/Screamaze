import json
import pygame
import UI.uiElements as u
from roomFunc.corrFunc import makeMask

# every new room is described in rooms.json: its picture, its elements and the text of each element
with open("data/rooms.json") as f:
    ROOMS = {room["key"]: room for room in json.load(f)["rooms"]}

# (room key, element id) of every element the player already changed, stays until the game closes
changed = set()


########## load the room picture and build a mask for every element ##########
def getElements(room):
    data = ROOMS[room.key]
    size = room.screen.get_size()
    image = u.load_image(data["image"], size)
    masks = []
    hotspots = {}
    for element in data["elements"]:
        if element["id"] == "door":
            action = lambda: leave(room)
        else:
            # element=element locks in the element for each mask (avoids late-binding bug)
            action = lambda element=element: look(room, element)
            hotspots[element["id"]] = makeHotspot(room, element)
        # mask images: full picture size, transparent except for the clickable area
        mask = u.Mask(element["mask"], size, (0, 0), action)
        cropMask(mask)
        masks.append((mask, element["label"]))
    return image, masks, hotspots


# cuts the empty part off a full-size mask, so drawing 7 of them every frame stays fast
def cropMask(mask):
    shape = mask.image.get_bounding_rect()
    mask.image = mask.image.subsurface(shape).copy()
    mask.imageMask = pygame.mask.from_surface(mask.image)
    mask.imageX += shape.x
    mask.imageY += shape.y


# the hotspot is the part of the close-up you can click, its pos is measured in the full picture
def makeHotspot(room, element):
    hotspot = element["pov"]["hotspot"]
    return makeMask(room.screen, hotspot["cutout"], hotspot["pos"], lambda: inspect(room), "")


########## helpers ##########
def say(room, text):
    room.fui.chat.say("You > " + text)


def isChanged(room, element):
    return (room.key, element["id"]) in changed


# the close-up pictures are big, so they are only loaded the first time you look at them
def povImage(room):
    pov = room.element["pov"]
    path = pov["changed"] if isChanged(room, room.element) else pov["image"]
    if path not in room.povImages:
        room.povImages[path] = u.load_image(path, room.screen.get_size())
    return room.povImages[path]


# the hotspot of the close-up you are looking at, gone once you clicked it
def activeHotspot(room):
    if room.element is None or isChanged(room, room.element):
        return None
    return room.hotspots[room.element["id"]]


########## element functions ##########
# pressing an element in the room walks up to it and shows its close-up
def look(room, element):
    room.element = element
    if isChanged(room, element):
        say(room, element["pov"]["changed_text"])
    else:
        say(room, element["text"])


# pressing the hotspot in a close-up changes the picture and tells what you found
def inspect(room):
    changed.add((room.key, room.element["id"]))
    say(room, room.element["pov"]["changed_text"])


def back(room):
    room.element = None


def leave(room):
    room.next_room = "corridor"
