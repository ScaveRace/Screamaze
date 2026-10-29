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
    "SecondaryRooms": [
        "class2021R.window", "class2021R.teacher_desk", "class2021R.chalkboard", "class2021R.fridge", "class2021R.notice_board",
        "class2031R.window", "class2031R.teacher_desk", "class2031R.globe", "class2031R.projector", "class2031R.chalkboard", "class2031R.lockers",
        "class2035R.chalkboard", "class2035R.teacher_desk", "class2035R.bookshelf", "class2035R.metal_cabinet", "class2035R.notice_board", "class2035R.globe",
        "frontDeskR.window", "frontDeskR.filing_cabinets", "frontDeskR.reception_desk", "frontDeskR.key_cabinet", "frontDeskR.wall_clock", "frontDeskR.printer",
        "lab2001R.window", "lab2001R.whiteboard", "lab2001R.server_rack", "lab2001R.metal_cabinet", "lab2001R.computers",
        "projRoom1R.window", "projRoom1R.bookshelf", "projRoom1R.printer_3d", "projRoom1R.whiteboard", "projRoom1R.table_left", "projRoom1R.table_right", "projRoom1R.beanbag",
        "projRoom2R.window", "projRoom2R.vending_machine", "projRoom2R.sticky_board", "projRoom2R.workshop_table", "projRoom2R.tool_cabinet", "projRoom2R.robot", "projRoom2R.cardboard_boxes",
        "stairR.staircase", "stairR.fire_door", "stairR.fire_extinguisher", "stairR.emergency_light",
        "teach1R.bookshelf", "teach1R.safe", "teach1R.notice_board", "teach1R.plant",
        "teach2R.filing_cabinets", "teach2R.desk", "teach2R.notice_board", "teach2R.plant",
        "teach3R.sofa", "teach3R.bookshelf", "teach3R.armchair", "teach3R.radio",
        "teach4R.window", "teach4R.sofa", "teach4R.coffee_table", "teach4R.meeting_table", "teach4R.coffee_machine", "teach4R.bookshelf",
    ]}


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