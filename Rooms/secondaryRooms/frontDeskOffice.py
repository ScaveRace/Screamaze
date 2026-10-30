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
    # the people in this room: (id of the picture in masks/, label, name of the action in newRoomFunc.ACTIONS)
    # the lady at the front desk takes the necklace and the game ends
    PEOPLE = [
        ("lady", "Lady", "giveNecklace"),
    ]
