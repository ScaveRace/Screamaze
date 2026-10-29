# Teachers Room 4
from Rooms.baseRoom import register
from Rooms.newRooms import NewRoom

@register
class TeachersRoom4(NewRoom):
    key = "teach4R"
    # all the pictures of this room are in this folder
    FOLDER = "assets/teachers_room_4/"
    # (id, label) of everything you can press in this room
    ELEMENTS = [
        ("window", "Window"),
        ("sofa", "Sofa"),
        ("coffee_table", "Coffee Table"),
        ("meeting_table", "Meeting Table"),
        ("coffee_machine", "Coffee Machine"),
        ("bookshelf", "Bookshelf"),
        ("door", "Leave room"),
    ]
