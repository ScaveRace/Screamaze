# Classroom 2.035
from Rooms.baseRoom import register
from Rooms.newRooms import NewRoom

@register
class Classroom2035(NewRoom):
    key = "class2035R"
    # all the pictures of this room are in this folder
    FOLDER = "assets/classroom_2035/"
    # (id, label) of everything you can press in this room
    ELEMENTS = [
        ("chalkboard", "Chalkboard"),
        ("teacher_desk", "Teacher Desk"),
        ("bookshelf", "Bookshelf"),
        ("metal_cabinet", "Metal Cabinet"),
        ("notice_board", "Notice Board"),
        ("globe", "Globe"),
        ("door", "Leave room"),
    ]
    # things you can press in a close-up: element id -> (id, label, what it does), see newRoomFunc.press
    # their pictures are in the folder of the element: <id>_mask.png, and the picture named in "then"
    CLICKABLES = {
        # the box in the desk opens with the brass key from Teachers Room 1, the silver key inside opens locker 2 in classroom 2.031 (optional)
        "teacher_desk": [
            ("box", "Small box", {"needs": "Small brass key", "then": "box_open", "once": True}),
            ("silver_key", "Small silver key", {"on": "box_open", "gives": ("Small silver key", "assets/items/small_silver_key/icon.png"), "then": "box_taken", "once": True}),
        ],
        # the pin in the globe can be taken, it does nothing (optional)
        "globe": [
            ("pin", "Pin", {"gives": ("Pin", "assets/items/pin/icon.png"), "then": "pov_taken", "once": True}),
        ],
    }
