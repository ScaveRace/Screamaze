import random
import pygame

SOUND_DIR = "assets/soundEffects/paranormal/"

# category -> file names inside that folder (edit these to match your files)
FILES = {
    "door":    ["door/creak.mp3", "door/slam.mp3", "door/knock.mp3"],
    "scream":  ["scream/scream1.mp3", "scream/scream2.mp3", "scream/scream3.mp3", "scream/scream4.mp3"],
    "misc":    ["misc/eerie1.mp3", "misc/footsteps1.mp3"],
}


class Paranormal:
    def __init__(self, minDelay=8000, maxDelay=25000, volume=0.7):
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        self.volume = volume
        self.minDelay = minDelay          # milliseconds between events
        self.maxDelay = maxDelay
        self.enabled = True
        self.sounds = {
            category: [pygame.mixer.Sound(SOUND_DIR + f) for f in files]
            for category, files in FILES.items()
        }
        self._schedule()

    def _schedule(self):
        self.nextEvent = pygame.time.get_ticks() + random.randint(self.minDelay, self.maxDelay)

    def play(self, category, pan=None, volume=None):
        """Play a random sound from a category. pan: -1 = full left, 1 = full right."""
        options = self.sounds.get(category)
        if not options:
            return
        channel = random.choice(options).play()
        if channel is None:               # no free channel
            return
        vol = self.volume if volume is None else volume
        if pan is None:
            pan = random.uniform(-1, 1)
        channel.set_volume(vol * min(1, 1 - pan), vol * min(1, 1 + pan))

    def update(self):
        """Call every frame."""
        if not self.enabled:
            return
        if pygame.time.get_ticks() >= self.nextEvent:
            self.play(random.choice(list(self.sounds)))
            self._schedule()

    def setActive(self, active):
        """Called every frame with the current room's flag."""
        if active == self.enabled:
            return
        self.enabled = active
        if active:
            self._schedule()  # wait a normal delay before the first sound
        else:
            pygame.mixer.stop()  # cut off anything still playing

paranormal = Paranormal()  # the one and only instance