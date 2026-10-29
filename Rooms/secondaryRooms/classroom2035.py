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
