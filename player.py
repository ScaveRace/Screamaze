import json

with open("story.json", encoding = "utf-8") as f:
    data = json.load(f)

class Player:
    completionPercentage = 0.0
    stones = []
    weapons = []
    deathCount = 0
    inventory = [stones,weapons]
    fullWeight = 0 #weight of all teh stories based on  json later


    def __init__(self, name, time, position, currentId, newRun):
        self.name = name
        self.time = time
        self.position = position
        self.currentId = currentId
        self.newRun = newRun



    def addToStone(self,stone):
        self.stones.append(stone)

    def addToWeapon(self, weapon):
        self.weapons.append(weapon)

    def addToInventory(self, item):
        self.inventory.append(item)

    def playerdeath(self):
        self.deathCount += 1

    def changeCurrentID(self, cId):
        self.currentId = cId

    def updateTime(self,time):
        self.time = time



    def weight_up_to(self):
        total = 0
        for key, entry in data.items():
            total += entry["weight"]
            if key == self.currentId:
                break
        percentageweight = 100/self.fullWeight
        self.completionPercentage = percentageweight*total
        print(self.completionPercentage)

    def fullWeightCal(self):
        for key, entry in data.items():
            self.fullWeight += entry["weight"]
            if key == "moment.green_stone":
                break

    def saveJson(self):
        data = {}
        if self.newRun:
            self.newRun = False
        for key, value in vars(type(self)).items():
            if key.startswith("_"):
                continue
            if callable(value):
                continue
            if isinstance(value, (property, classmethod, staticmethod)):
                continue
            data[key] = value
        data.update(vars(self))
        with open("playerRun.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

newPlayer = Player("Johan",11099.7,"Stuck","quiz.lab2001", False)
newPlayer.fullWeightCal()
newPlayer.weight_up_to()
saveStruct.saveRunDB(newPlayer)
newPlayer.saveJson()


