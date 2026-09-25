import json
import os
import UI.uiElements as u
SAVE_PATH = "data/savegame.json"


# --- saving / loading ---
def save(what, path=SAVE_PATH):
    with open(path, "w", encoding="utf-8") as f:
        # pImage is a pygame Surface and can't be saved as json
        data = {k: v for k, v in vars(what).items() if k != "pImage"}
        json.dump(data, f, indent=2)


def load(what, path=SAVE_PATH):
    if not os.path.exists(path):
        return  # no save file yet, so keep the defaults
    with open(path, "r", encoding="utf-8") as f:
        vars(what).update(json.load(f))
    what.pImage = u.load_image(what.setGenderIm(what.gender), (64, 64))

def is_json_empty(path):
    if not os.path.exists(path):
        return True
    with open(path, "r", encoding="utf-8") as f:
        try:
            json_obj = json.load(f)
        except json.JSONDecodeError:
            return True
    return len(json_obj)