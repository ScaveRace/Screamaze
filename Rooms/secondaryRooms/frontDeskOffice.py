# Front Desk Office
from Rooms.baseRoom import register
from Rooms.newRooms import NewRoom

@register
class FrontDeskOffice(NewRoom):
    key = "frontDeskR"
    # all the pictures of this room are in this folder
    FOLDER = "assets/front_desk_office/"
    # (id, label) of everything you can press in this room
    ELEMENTS = [
        ("window", "Window"),
        ("filing_cabinets", "Filing Cabinets"),
        ("reception_desk", "Reception Desk"),
        ("key_cabinet", "Key Cabinet"),
        ("wall_clock", "Wall Clock"),
        ("printer", "Printer"),
        ("door", "Leave room"),
    ]
    # buttons this room has besides its elements: (label, (x, y, width, height), name of the action in newRoomFunc.ACTIONS)
    # this one is a placeholder for the lady at the front desk, she takes the necklace and the game ends
    BUTTONS = [
        ("Give the necklace", (770, 130, 260, 50), "giveNecklace"),
    ]
