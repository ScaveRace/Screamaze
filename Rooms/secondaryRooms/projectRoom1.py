# Project Room 1
from Rooms.baseRoom import register
from Rooms.newRooms import NewRoom

@register
class ProjectRoom1(NewRoom):
    key = "projRoom1R"
    # all the pictures of this room are in this folder
    FOLDER = "assets/project_room_1/"
    # (id, label) of everything you can press in this room
    ELEMENTS = [
        ("window", "Window"),
        ("bookshelf", "Bookshelf"),
        ("printer_3d", "3D Printer"),
        ("whiteboard", "Whiteboard"),
        ("table_left", "Project Table"),
        ("table_right", "Project Table"),
        ("beanbag", "Beanbag"),
        ("door", "Leave room"),
    ]
    # an item that falls out of an element when you press its close-up, you pick it up by pressing it:
    # id -> (item name, picture and inventory icon, centre in the room picture, width on screen)
    # the name must be spelled exactly like the Project Room badge it belongs to
    FOUND = {
        "beanbag": ("Square", "assets/shapes/square.png", (740, 590), 100),
    }
