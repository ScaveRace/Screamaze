# Classroom 2.031
from Rooms.baseRoom import register
from Rooms.newRooms import NewRoom

@register
class Classroom2031(NewRoom):
    key = "class2031R"
    # all the pictures of this room are in this folder
    FOLDER = "assets/classroom_2031/"
    # (id, label) of everything you can press in this room
    ELEMENTS = [
        ("window", "Window"),
        ("teacher_desk", "Teacher Desk"),
        ("globe", "Globe"),
        ("projector", "Projector"),
        ("chalkboard", "Chalkboard"),
        ("lockers", "Lockers"),
        ("door", "Leave room"),
    ]
    # things you can press in a close-up: element id -> (id, label, what it does), see newRoomFunc.press
    # their pictures are in the folder of the element: <id>_mask.png, and the picture named in "then"
    CLICKABLES = {
        # locker 2 is padlocked, the silver key from classroom 2.035 opens it (optional)
        "lockers": [
            ("locker_2", "Locker 2", {"needs": "Small silver key", "then": "locker2_open", "once": True}),
        ],
        # a crumpled flyer lies on the floor next to the globe, it does nothing (optional)
        "globe": [
            ("flyer", "Biology flyer", {"gives": ("Biology flyer", "assets/items/biology_flyer/icon.png"), "then": "pov_taken", "once": True}),
        ],
    }
