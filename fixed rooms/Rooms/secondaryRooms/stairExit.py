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
        ("emergency_light", "Emergency Light"),
        ("door", "Leave room"),
    ]
    # behind the extinguisher is a keypad with a close-up of its own: fire_extinguisher/keypad.png and keypad_mask.png
    CLOSEUPS = {
        "fire_extinguisher": "keypad",
    }
