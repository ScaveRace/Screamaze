# Project Room 1

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

# an item hidden in an element, you get it the first time you press its close-up: id -> (item name, icon)
# the name must be spelled exactly like the Project Room badge it belongs to, there is no picture for it yet
FOUND = {
    "beanbag": ("Square", FOLDER + "beanbag/square.png"),
}
