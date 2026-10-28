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
        ("bookshelf", "Bookshelf"),
        ("armchair", "Armchair"),
        ("radio", "Radio"),
        ("door", "Leave room"),
    ]
