import sqlite3
from functions.settingsFunc import settings as sett


class StoryDB:
    LANGUAGES = {"en", "nl"}

    def __init__(self, path="data/database/storyDB.db"):
        self.conn = sqlite3.connect(path)
        rows = self.conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        self.tables = {r[0] for r in rows}        # read once at startup

    def chatMessage(self, room, messageID, lang=None):
        if lang is None:
            lang = sett.getLanguage()      # the language chosen in the pause menu
        if room not in self.tables:
            raise ValueError(f"unknown table: {room}")
        if lang not in self.LANGUAGES:
            raise ValueError(f"unknown language: {lang}")
        row = self.conn.execute(
            f'SELECT COALESCE(text_{lang}, text_en) FROM "{room}" WHERE id = ?',   # english when there is no translation
            (messageID,),).fetchone()
        return row[0] if row else None

    def close(self):
        self.conn.close()