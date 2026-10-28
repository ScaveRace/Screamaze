
#####  player data  #####
#  use: from player import player
#  call function like: player.add_item("testitem")
import UI.uiElements as u
import data.playerLogistics as pL


class Player:

    def __init__(self):
        self.pImage = None
        self.name = ""
        self.time = 0            # seconds, integer
        self.position = (0,0)
        self.location = "corridor"
        self.lastLocation = "frontDesk"
        self.inventory = {"Stones":[],"Items":[ ]}
        self.gender = ""
        self.completion = {"VampRoom":{"all":[],"current": "", "msg":""},
                           "GhostRoom":{"all":[],"current": "", "msg":""},
                           "TeacherRoom":{"all":[],"current": "", "msg":""},
                           "EquinoxRoom":{"all":[],"current": "", "msg":""},
                           "StorrageRoom":{"all":[],"current": "", "msg":""},
                           "ProjectRoom":{"all":[],"current": "", "msg":""},
                           "Corridor":{"all":[],"current": "corr.start", "msg":""},
                           "FrontDesk":{"all":[],"current": "", "msg":""},
                           "SecondaryRooms":{"all":[],"current": "", "msg":""}
        }



    def createPlayer(self,name,gender):
        self.pImage = u.load_alpha_image(self.setGenderIm(gender), (64, 64))
        self.pImage.convert_alpha()
        self.name = name
        self.gender = gender

    def setImage(self):
        self.pImage = u.load_alpha_image(self.setGenderIm(self.gender), (64, 64))

    # --- inventory ---
    def add_item(self, StonesOrItems, name, path):
        self.inventory[StonesOrItems].append({name: path})


    def setGenderIm(self, g):
        return (f"assets/player/player_{g.lower()}.png")


    def addCompletion(self,room,current,msg):
        self.getCompletion(room)["all"].append(current)
        self.completion[room]["current"] = current
        self.completion[room]["msg"] = msg

    def getCompletion(self,room):
        # a save file from before a room was added doesn't have that room yet
        if room not in self.completion:
            self.completion[room] = {"all":[],"current": "", "msg":""}
        return self.completion[room]



    def remove_item(self, category, item):
        for element in self.inventory[category]:
            if item in element:
                self.inventory[category].remove(element)
                return True

    def setCurrent(self,current):
        self.lastLocation = self.location

    def has_item(self, category, item):
        for element in self.inventory[category]:
            if item in element:
                return True
        return False

    def count(self, item):
        return self.inventory.count(item)


    # --- time ---
    def add_time(self, seconds):
        self.time += int(seconds)

    #resets the whole game after every completion
    def reset(self):
        self.__init__()

    def draw(self,screen):
        if self.location == "corridor":
            self.position = pL.DOOR_SPAWNS[self.lastLocation]
        screen.blit(self.pImage,self.position)

