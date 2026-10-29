from autoplayer import mask_point
import functions.leaderboard as lb
import roomFunc.stoRoomFunc as sF


# ---------- checks ----------
def room_done(room):
    # passes when every counted event of this room is saved
    def check(p):
        missing = [s for s in lb.STEPS[room] if s not in p.getCompletion(room)["all"]]
        assert not missing, f"{room} is missing: {missing}"
        return True
    return check


def event_done(room, event):
    return lambda p: event in p.getCompletion(room)["all"]


def everything_done(p):
    pct = lb.completion(p)
    missing = [(room, s) for room, steps in lb.STEPS.items()
               for s in steps if s not in p.getCompletion(room)["all"]]
    assert pct == 100, f"completion is {pct}%, missing: {missing}"
    return True


# ---------- where to click (read from the game itself, not hard-coded) ----------
def door(label):
    # a door in the corridor, found by its label
    return lambda room: mask_point(next(m for m in room.elements if m.label == label))


def sto_mask(name):
    return lambda room: mask_point(sF.masks[name])


def sto_button(i):
    # i-th button of the storage view that is open right now
    return lambda room: sF.currentButtons()[i].rect.center


def sto_answer(n):
    # the right answer button of quiz question n; the index comes from the room's own data
    return lambda room: sF.currentButtons()[sF.QUESTION_IDS[n][2]].rect.center
STEPS = (
    # ---------- start ----------
        [("click", (195, 445), "press New Game"),
         ("expect_room", "frontD", "front desk opens")]
        + [("click", (700, 300), f"skip story {i + 1}") for i in range(9)]
        + [
            ("wait", lambda room: room.storyDone(), "story is finished"),
            ("do", lambda room: setattr(room.textField, "text", "Bot"), "set the name to Bot"),
            ("click", (1200, 375), "press Start Run"),
            ("expect_room", "corridor", "corridor opens"),

        # ---------- storage room ----------
        ("click", door("Storage"), "click the Storage door"),
        ("expect_room", "storrR", "storage room opens"),
        ("click", sto_mask("rack"), "open the rack"),
        ("click", sto_mask("fuse"), "take the fuse"),
        ("check", lambda p: p.has_item("Items", "Fuse"), "fuse is in the inventory"),
        ("click", sto_button(0), "return to the room"),
        ("click", sto_mask("desk"), "go to the desk"),
        ("click", sto_mask("quiz"), "open the quiz"),
        ("click", sto_answer(0), "quiz question 1"),
        ("click", sto_answer(1), "quiz question 2"),
        ("click", sto_answer(2), "quiz question 3"),
        ("check", event_done("StorrageRoom", "sto.quiz"), "quiz solved"),
        ("click", sto_mask("drawer"), "open the drawer"),
        ("click", sto_mask("stone"), "take the stone"),
        ("click", sto_button(0), "back to the desk"),
        ("click", sto_button(0), "return to the room"),
        ("check", room_done("StorrageRoom"), "storage room complete"),
        ("click", sto_button(0), "leave the room"),
        ("expect_room", "corridor", "back in the corridor"),
    ]
)