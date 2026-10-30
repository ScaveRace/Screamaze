# LAB 2.001
from Rooms.baseRoom import register
from Rooms.newRooms import NewRoom

@register
class Lab2001(NewRoom):
    key = "lab2001R"
    # all the pictures of this room are in this folder
    FOLDER = "assets/lab_2001/"
    # (id, label) of everything you can press in this room
    ELEMENTS = [
        ("window", "Window"),
        ("whiteboard", "Whiteboard"),
        ("server_rack", "Server Rack"),
        ("metal_cabinet", "Metal Cabinet"),
        ("computers", "Computers"),
        ("door", "Leave room"),
    ]
    # the password of the computers is the answer of the hangman game in classroom 2.021 (optional)
    # the right code shows computers/log.png, the maintenance log
    CODES = {
        "computers": ("WATCH", "log"),
    }
