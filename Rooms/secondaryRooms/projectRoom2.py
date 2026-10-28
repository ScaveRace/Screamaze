# Project Room 2
from Rooms.baseRoom import register
from Rooms.newRooms import NewRoom

@register
class ProjectRoom2(NewRoom):
    key = "projRoom2R"
    # all the pictures of this room are in this folder
    FOLDER = "assets/project_room_2/"
    # (id, label) of everything you can press in this room
    ELEMENTS = [
        ("window", "Window"),
        ("vending_machine", "Vending Machine"),
        ("sticky_board", "Sticky Board"),
        ("workshop_table", "Workshop Table"),
        ("tool_cabinet", "Tool Cabinet"),
        ("robot", "Robot"),
        ("cardboard_boxes", "Cardboard Boxes"),
        ("door", "Leave room"),
    ]
