# Classroom 2.021
from Rooms.baseRoom import register
from Rooms.newRooms import NewRoom

@register
class Classroom2021(NewRoom):
    key = "class2021R"
    # all the pictures of this room are in this folder
    FOLDER = "assets/classroom_2021/"
    # (id, label) of everything you can press in this room
    ELEMENTS = [
        ("window", "Window"),
        ("teacher_desk", "Teacher Desk"),
        ("chalkboard", "Chalkboard"),
        ("fridge", "Fridge"),
        ("notice_board", "Notice Board"),
        ("door", "Leave room"),
    ]
