# Teachers Room 3
from Rooms.baseRoom import register
from Rooms.newRooms import NewRoom

@register
class TeachersRoom3(NewRoom):
    key = "teach3R"
    # all the pictures of this room are in this folder
    FOLDER = "assets/teachers_room_3/"
    # (id, label) of everything you can press in this room
    ELEMENTS = [
        ("sofa", "Sofa"),
        ("telephone", "Telephone"),
        ("bookshelf", "Bookshelf"),
        ("armchair", "Armchair"),
        ("door", "Leave room"),
    ]
    # things you can press in a close-up: element id -> (id, label, what it does), see newRoomFunc.press
    # their pictures are in the folder of the element: <id>_mask.png, and the picture named in "then"
    CLICKABLES = {
        # the diary is hidden in the cushion of the sofa (optional)
        "sofa": [
            ("diary", "Marsh's diary", {"gives": ("Marsh's diary", "assets/items/marsh_diary/icon.png"), "then": "pov_taken", "once": True}),
        ],
        # the red book is a dead end, it only has a text
        "bookshelf": [
            ("red_book", "Red book", {}),
        ],
    }
