import json
import os
import UI.uiElements as u
SAVE_PATH = "data/savegame.json"


# --- saving / loading ---
def save(self, path=SAVE_PATH):
    with open(path, "w", encoding="utf-8") as f:
        # pImage is a pygame Surface and can't be saved as json
        data = {k: v for k, v in vars(self).items() if k != "pImage"}
        json.dump(data, f, indent=2)


def load(self, path=SAVE_PATH):
    if not os.path.exists(path):
        return  # no save file yet, so keep the defaults
    with open(path, "r", encoding="utf-8") as f:
        vars(self).update(json.load(f))
    self.pImage = u.load_image(self.setGenderIm(self.gender), (64, 64))