import pygame

TIMEOUT = 600       # frames a "wait" or "expect_room" may take (about 10 seconds)


class AutoPlayer:
    def __init__(self, steps, delay=15):
        self.steps = list(steps)
        self.total = len(self.steps)
        self.delay = delay
        self.wait = 0               # frames to pause after a finished step
        self.waited = 0             # frames spent waiting for the current step
        self.passed = 0
        self.failed = None          # (step number, label, message) of the first failure
        self.done = False

    def update(self, current, player, room):
        if self.done:
            return
        if not self.steps:
            self.report()
            return
        if self.wait > 0:
            self.wait -= 1
            return

        kind, arg, *rest = self.steps[0]
        label = rest[0] if rest else kind
        number = self.total - len(self.steps) + 1
        try:
            # "expect_room" and "wait" keep trying every frame until true (or time runs out)
            if kind == "expect_room":
                ok = current == arg
            elif kind == "wait":
                try:
                    ok = bool(arg(room))
                except Exception:
                    ok = False
            else:
                ok = True
            if not ok:
                self.waited += 1
                assert self.waited < TIMEOUT, f"timed out, the game is in room {current!r}"
                return

            if kind == "click":         # arg = (x, y), or a function(room) that returns (x, y)
                pos = arg(room) if callable(arg) else arg
                for t in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                    pygame.event.post(pygame.event.Event(t, pos=pos, button=1))
            elif kind == "type":        # types text like the keyboard does
                for ch in arg:
                    pygame.event.post(pygame.event.Event(pygame.TEXTINPUT, text=ch))
            elif kind == "do":          # runs a function(room): a shortcut for setup
                arg(room)
            elif kind == "check":
                assert arg(player), "check returned False"

            self.steps.pop(0)
            self.waited = 0
            self.passed += 1
            print(f"[autoplay] {number}/{self.total} OK    {label}")
            self.wait = self.delay
        except Exception as e:
            self.failed = (number, label, str(e))
            print(f"[autoplay] {number}/{self.total} FAIL  {label}: {e}")
            self.steps.clear()          # later steps make no sense after a failure

    def report(self):
        self.done = True
        if self.failed:
            n, label, msg = self.failed
            text = f"AUTOPLAY FAILED at step {n} ({label}): {msg}"
        else:
            text = f"AUTOPLAY PASSED: {self.passed}/{self.total} steps ok"
        print(text)
        with open("autoplay_report.txt", "w") as f:
            f.write(text + "\n")

    def draw(self, screen, font):
        if self.done:
            ok = self.failed is None
            msg = "AUTOPLAY PASSED" if ok else "AUTOPLAY FAILED"
            color = (0, 200, 0) if ok else (220, 0, 0)
        else:
            msg = f"autoplay {self.total - len(self.steps)}/{self.total}"
            color = (255, 255, 255)
        screen.blit(font.render(msg, True, color), (320, 10))


def mask_point(mask):
    # a point that really lies inside the clickable shape
    r = mask.image.get_bounding_rect()
    cx, cy = r.center
    if mask.imageMask.get_at((cx, cy)):
        return (cx + mask.imageX, cy + mask.imageY)
    best = None                          # centre is hollow: take the solid pixel closest to it
    for y in range(r.top, r.bottom, 3):
        for x in range(r.left, r.right, 3):
            if mask.imageMask.get_at((x, y)):
                d = (x - cx) ** 2 + (y - cy) ** 2
                if best is None or d < best[0]:
                    best = (d, x, y)
    assert best, "mask has no solid pixel to click"
    return (best[1] + mask.imageX, best[2] + mask.imageY)