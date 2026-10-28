# Teachers Room 2
from Rooms.baseRoom import register
from Rooms.newRooms import NewRoom

@register
class TeachersRoom2(NewRoom):
    key = "teach2R"
    # all the pictures of this room are in this folder
    FOLDER = "assets/teachers_room_2/"
    # (id, label) of everything you can press in this room
    ELEMENTS = [
        ("filing_cabinets", "Filing Cabinets"),
        ("desk", "Desk"),
        ("notice_board", "Notice Board"),
        ("plant", "Plant"),
        ("door", "Leave room"),
    ]
