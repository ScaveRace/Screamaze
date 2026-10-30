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
    # locker 2 is padlocked, the silver key from Classroom 2.035 opens it (optional)
    LOCKS = {
        "lockers": "Small silver key",
    }
