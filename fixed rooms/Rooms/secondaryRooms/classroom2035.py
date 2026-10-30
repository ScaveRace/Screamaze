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
    # the box in the desk is locked, the brass key from Teachers Room 1 opens it (optional)
    LOCKS = {
        "teacher_desk": "Small brass key",
    }
    # the silver key lies in the opened box, it opens locker 2 in classroom 2.031 (optional)
    FOUND = {
        "teacher_desk": ("Small silver key", "assets/items/silver_key.png", (593, 451), 110),
    }
