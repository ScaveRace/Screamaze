# Teachers Room 1
from Rooms.baseRoom import register
from Rooms.newRooms import NewRoom

@register
class TeachersRoom1(NewRoom):
    key = "teach1R"
    # all the pictures of this room are in this folder
    FOLDER = "assets/teachers_room_1/"
    # (id, label) of everything you can press in this room
    ELEMENTS = [
        ("bookshelf", "Bookshelf"),
        ("desks", "Desks"),
        ("safe", "Safe"),
        ("notice_board", "Notice Board"),
        ("plant", "Plant"),
        ("door", "Leave room"),
    ]
    # things you can press in a close-up: element id -> (id, label, what it does), see newRoomFunc.press
    # their pictures are in the folder of the element: <id>_mask.png, and the picture named in "then"
    CLICKABLES = {
        # the brass key lies in the spilled soil, it opens the box in the desk of classroom 2.035 (optional)
        "plant": [
            ("brass_key", "Small brass key", {"gives": ("Small brass key", "assets/items/small_brass_key/icon.png"), "then": "pov_taken", "once": True}),
        ],
    }
