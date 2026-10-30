# Stair Exit
from Rooms.baseRoom import register
from Rooms.newRooms import NewRoom

@register
class StairExit(NewRoom):
    key = "stairR"
    # all the pictures of this room are in this folder
    FOLDER = "assets/stair_exit/"
    # (id, label) of everything you can press in this room
    ELEMENTS = [
        ("staircase", "Staircase"),
        ("fire_door", "Fire Door"),
        ("fire_extinguisher", "Fire Extinguisher"),
        ("cardboard_boxes", "Cardboard Boxes"),
        ("emergency_light", "Emergency Light"),
        ("door", "Leave room"),
    ]
    # things you can press in a close-up: element id -> (id, label, what it does), see newRoomFunc.press
    # their pictures are in the folder of the element: <id>_mask.png, and the picture named in "then"
    CLICKABLES = {
        # the keypad behind the extinguisher is a dead end, it only has a close-up of its own
        "fire_extinguisher": [
            ("keypad", "Keypad", {"then": "keypad"}),
        ],
    }
