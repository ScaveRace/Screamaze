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
        ("safe", "Safe"),
        ("notice_board", "Notice Board"),
        ("plant", "Plant"),
        ("door", "Leave room"),
    ]
    # the brass key lies in the spilled soil of the plant, it opens the box in the desk of classroom 2.035 (optional)
    # id -> (item name, picture and inventory icon, centre in the room picture, width on screen)
    FOUND = {
        "plant": ("Small brass key", "assets/items/brass_key.png", (586, 536), 110),
    }
