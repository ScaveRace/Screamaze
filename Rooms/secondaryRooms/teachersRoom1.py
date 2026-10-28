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
