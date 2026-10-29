import sqlite3

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


def connect():
    con = sqlite3.connect(DB_PATH)
    con.execute("CREATE TABLE IF NOT EXISTS leaderboard ("
                "name TEXT PRIMARY KEY, time INTEGER, completion INTEGER, finished INTEGER DEFAULT 0)")
    return con


# called when the player saves: puts the run on the leaderboard or updates it
def saveRun(player):
    con = connect()
    con.execute("INSERT INTO leaderboard (name, time, completion) VALUES (?, ?, ?) "
                "ON CONFLICT(name) DO UPDATE SET time = excluded.time, completion = excluded.completion",
                (player.name, player.time, completion(player)))
    con.commit()
    con.close()


# called when the game is finished: only updates a run that was saved before
def finishRun(player):
    con = connect()
    con.execute("UPDATE leaderboard SET time = ?, completion = ?, finished = 1 WHERE name = ?",
                (player.time, completion(player), player.name))
    con.commit()
    con.close()


# the best five runs: the highest completion first, the fastest time wins when it is the same
def topFive():
    con = connect()
    rows = con.execute("SELECT name, time, completion, finished FROM leaderboard "
                       "ORDER BY completion DESC, time ASC LIMIT 5").fetchall()
    con.close()
    return rows
