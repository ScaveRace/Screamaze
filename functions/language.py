import json
from functions.settingsFunc import settings as sett

# every text of the game is in data/languages, one json file per language
# a file looks like this: room -> id of the message -> text
# {"GhostRoom": {"1": "Ohh a student has finally come to class.", "2": "..."}, "FrontDesk": {...}}
LANGUAGES = ("en", "nl")

texts = {}      # language -> room -> id -> text
for language in LANGUAGES:
    with open(f"data/languages/{language}.json", encoding="utf-8") as f:
        texts[language] = json.load(f)


# the text of one message, in the language chosen in the pause menu
def chatMessage(room, messageID, lang=None):
    if lang is None:
        lang = sett.getLanguage()
    if lang not in texts:
        raise ValueError(f"unknown language: {lang}")
    if room not in texts["en"]:
        raise ValueError(f"unknown room: {room}")
    messageID = str(messageID)      # some rooms use numbers as id, json only has text
    text = texts[lang].get(room, {}).get(messageID)
    if not text:
        text = texts["en"][room].get(messageID)     # english when there is no translation
    return text



# the text on a button or label, in the language chosen in the pause menu
# the text in the code is also the id in the "Buttons" table; without a translation it is shown as it is
def ui(text, lang=None):
    if lang is None:
        lang = sett.getLanguage()
    return texts.get(lang, {}).get("Buttons", {}).get(text, text)
