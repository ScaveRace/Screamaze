import sqlite3
from datetime import datetime


# the leaderboard is its own small database, one row per player name
# a run only gets on it when the player saves the game, saving again updates the row
DB_PATH = "data/leaderboard.db"

# the steps that count for the completion percentage: room -> events in player.completion[room]["all"]
# the secondary rooms are only extra story, so they are saved but don't count
STEPS = {
    "Corridor": ["corr.going"],
    "VampRoom": ["vamp.talk_1", "vamp.talk_2", "vamp.talk_3", "vamp.circle_found", "vamp.fuse_inserted",
                 "vamp.task_done", "vamp.stone"],
    "StorrageRoom": ["sto.fuse", "sto.quiz", "sto.stone"],
    "TeacherRoom": ["tr.described", "tr.chest_described", "tr.placed.White", "tr.placed.Red", "tr.placed.Green",
                    "tr.placed.Purple", "tr.placed.Yellow", "tr.unlocked", "tr.necklace"],
    "GhostRoom": ["gr.described", "gr.talk_1", "gr.talk_2", "gr.talk_3", "gr.cabinet_unlocked",
                  "gr.homework_taken", "gr.homework_done", "gr.stone_taken"],
    "EquinoxRoom": ["equin.talked", "equin.sandwich", "equin.lookaway", "equin.stone"],
    "ProjectRoom": ["proj.visited", "proj.placed.Circle", "proj.placed.Triangle", "proj.placed.Square", "proj.stone"],
}


# how much of the game the player did, from 0 to 100
def completion(player):
    done = 0
    total = 0
    for room, steps in STEPS.items():
        for step in steps:
            total += 1
            if step in player.getCompletion(room)["all"]:
                done += 1
    return round(done / total * 100)

def today():
    return datetime.now().strftime("%d-%m-%Y") # "29-10-2026"

def fmtDate(d):
    return datetime.strptime(d, "%d-%m-%Y").strftime("%d %b") if d else "-" # "29 Oct", "-" if no date

def dateKey(d):
    return datetime.strptime(d, "%d-%m-%Y") if d else datetime.min   # for sorting on date

def fmtTime(seconds):
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


def connect():
    con = sqlite3.connect(DB_PATH)
    con.execute("CREATE TABLE IF NOT EXISTS leaderboard ("
                "name TEXT PRIMARY KEY, time INTEGER, completion INTEGER, finished INTEGER DEFAULT 0, "
                "updated_at TEXT)")
    try:
        con.execute("ALTER TABLE leaderboard ADD COLUMN updated_at TEXT")
    except sqlite3.OperationalError:
        pass  # column already exists
    return con


# called when the player saves: puts the run on the leaderboard or updates it
def saveRun(player):
    if not player.name.strip():
        return
    con = connect()
    con.execute("INSERT INTO leaderboard (name, time, completion, updated_at) VALUES (?, ?, ?, ?) "
                "ON CONFLICT(name) DO UPDATE SET time = excluded.time, completion = excluded.completion, "
                "updated_at = excluded.updated_at",
                (player.name, player.time, completion(player), today()))
    con.commit()
    con.close()


# called when the game is finished: only updates a run that was saved before
def finishRun(player):
    con = connect()
    con.execute("UPDATE leaderboard SET time = ?, completion = ?, finished = 1, updated_at = ? WHERE name = ?",
                (player.time, completion(player), today(), player.name))
    con.commit()
    con.close()

def allRuns():
    con = connect()
    rows = con.execute("SELECT name, time, completion, finished, updated_at FROM leaderboard").fetchall()
    con.close()
    return rows

# the best five runs: the highest completion first, the fastest time wins when it is the same
def topFive():
    con = connect()
    rows = con.execute("SELECT name, time, completion, finished FROM leaderboard "
                       "ORDER BY completion DESC, time ASC LIMIT 5").fetchall()
    con.close()
    return rows

connect().execute("DELETE FROM leaderboard WHERE name = '';")