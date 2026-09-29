
#####  player data  #####
#  use: from player import player
#  call function like: player.add_item("testitem")
import UI.uiElements as u


class Player:

    def __init__(self):
        self.pImage = None
        self.name = ""
        self.time = 0            # seconds, integer
        self.position = (505,500)
        self.location = "corridor"
        self.inventory = []
        self.gender = ""

    def createPlayer(self,name,gender):
        self.pImage = u.load_alpha_image(self.setGenderIm(gender), (64, 64))
        self.pImage.convert_alpha()
        self.name = name
        self.gender = gender

    def setImage(self):
        self.pImage = u.load_alpha_image(self.setGenderIm(self.gender), (64, 64))

    # --- inventory ---
    def add_item(self, item, amount=1):
        for _ in range(amount):
            self.inventory.append(item)


    def setGenderIm(self, g):
        return (f"assets/player/player_{g.lower()}.png")


    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False


    def has_item(self, item):
        return item in self.inventory


    def count(self, item):
        return self.inventory.count(item)


    # --- time ---
    def add_time(self, seconds):
        self.time += int(seconds)


    def draw(self,screen):

        screen.blit(self.pImage,self.position)
