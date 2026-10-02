import sqlite3


class StoryDB:
    LANGUAGES = {"en", "nl"}

    def __init__(self, path="data/database/storyDB.db"):
        self.conn = sqlite3.connect(path)
        rows = self.conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        self.tables = {r[0] for r in rows}        # read once at startup

    def chatMessage(self, room, messageID, lang="en"):
        if room not in self.tables:
            raise ValueError(f"unknown table: {room}")
        if lang not in self.LANGUAGES:
            raise ValueError(f"unknown language: {lang}")
        row = self.conn.execute(
            f'SELECT text_{lang} FROM "{room}" WHERE id = ?',
            (messageID,),).fetchone()
        return row[0] if row else None

    def close(self):
        self.conn.close()