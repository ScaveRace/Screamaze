import random
import pygame
import UI.uiElements as u
from player import player

pygame.init()

pygame.mixer.init()

class EquinoxRoom:
    def __init__(self, screen):
        self.image = u.load_image("assets/startup.png", screen.get_size()) #  will change
        self.screen = screen
        self.conversation = 0 #### 0 = idle, 1 = riddles, 2 = reveal, 3 = stone on floor, 4 = done
        self.next_room = None

        self.student = u.load_image("assets/equinox_student.png", (220, 360))
        self.demon = u.load_image("assets/equinox_demon.png", (220, 360))
        self.stone = u.load_image("assets/yellow_stone.png", (48, 48))
        self.sandwich = u.load_image("assets/sandwich.png", (64, 44))
        self.figurePos = (760, 180)
        self.stonePos = (846, 520)
        self.sandwichSpots = [(690, 230), (1000, 250), (700, 360), (1010, 380), (840, 120), (980, 140)]
        self.summoned = 0 # how many sandwiches he has summoned so far

        self.disguised = True
        self.vanishing = False
        self.demonAlpha = 255

        # dialogue queue: (who, text) lines or functions, shown one at a time
        self.lines = []
        self.lineTimer = 0
        self.chat = u.Chatbox(40, 470, 700, 230)

        # (question lines, accepted answers, hint) - the chatbox doesn't wrap, keep lines short
        self.riddles = [
            (["An earl loved cards too much to leave the",
              "table, so he ate me with his hands.",
              "What am I?"],
             ["sandwich", "sandwiches"],
             "You're looking at one. It's floating."),
            (["I am the first and last of every",
              "sandwich, yet never the filling.",
              "What am I?"],
             ["bread", "slice", "slices", "slice of bread", "slices of bread",
              "bread slice", "bread slices"],
             "Loaf around a little longer. Think."),
            (["I'm churned from cream, I'm spread thin,",
              "and I melt in the pan. What am I?"],
             ["butter"],
             "It goes on the bread before the pan."),
        ]
        self.wrongLines = ["Wrong.", "Stale answer.", "No. Undercooked.", "Try again. I have all night."]
        self.riddle = 0
        self.wrong = 0
        self.lastWrongLine = ""

        self.corridorButton = u.Button(400, 400, 140, 50, "corridor", self.corridor)
        self.testButton = u.Button(200, 400, 140, 50, "testitem", self.gettestitem)
        self.talkButton = u.Button(760, 600, 220, 50, "talk to student", self.talk)
        self.stoneButton = u.Button(770, 600, 200, 50, "take the stone", self.takeStone)

        if player.has_item("yellow_stone"):
            self.conversation = 4
            self.buttons = [self.corridorButton, self.testButton]
            self.chat.say("* Crumbs on an empty desk. Nobody here.")
        else:
            self.buttons = [self.corridorButton, self.testButton, self.talkButton]
            self.chat.say("* The room smells of toasted bread.")
            self.chat.say("* A student sits hunched over a book, eating.")

    def gettestitem(self):
        if not player.has_item("testitem"):
            player.add_item("testitem")

    def corridor(self):
        self.next_room = "corridor"

    def talk(self):
        self.conversation = 1
        self.buttons = [self.corridorButton, self.testButton]
        self.chat.focus = True
        self.say(None, "* He doesn't look up. He keeps chewing.")
        self.say("Student", "...mm. You're not in my class.")
        self.say("Student", "Hungry?")
        self.lines.append(self.summon)
        self.say(None, "* A sandwich appears in the air beside him.")
        self.say("Student", "Answer me three things, and I'll leave")
        self.say("Student", "you something better than lunch.")
        self.askRiddle()

    def takeStone(self):
        player.add_item("yellow_stone")
        self.conversation = 4
        self.buttons = [self.corridorButton, self.testButton]
        self.chat.say("* You pick up the stone. Warm as fresh toast.")

    def say(self, who, text):
        self.lines.append((who, text)) # who = None means narration

    def askRiddle(self):
        for line in self.riddles[self.riddle][0]:
            self.say("Student", line)

    def answer(self, text):
        if self.lines: # he's still talking
            interrupt = ("Student", "Shh. Let me finish.")
            if interrupt not in self.lines:
                self.lines.insert(0, interrupt)
            return

        guess = text.lower().strip(" .!?'\"")
        for article in ("a ", "an ", "the "):
            if guess.startswith(article):
                guess = guess[len(article):]

        question, answers, hint = self.riddles[self.riddle]
        if guess in answers:
            self.riddle += 1
            self.wrong = 0
            self.lines.append(self.summon)
            if self.riddle < len(self.riddles):
                self.say("Student", random.choice(["Correct.", "Mm. Correct.", "...Correct."]))
                self.askRiddle()
            else:
                self.reveal()
        else:
            self.wrong += 1
            line = random.choice([l for l in self.wrongLines if l != self.lastWrongLine])
            self.lastWrongLine = line
            self.say("Student", line)
            if self.wrong >= 2:
                self.say("Student", hint)

    def reveal(self):
        self.conversation = 2
        self.chat.focus = False
        self.say("Student", "...Correct.")
        self.say(None, "* He stops chewing.")
        self.lines.append(self.dropDisguise)
        self.say(None, "* The lights dim. Something tall stands up.")
        self.say("Demon", "SHARPER THAN THE LAST ONE.")
        self.lines.append(self.summonAll)
        self.say("Demon", "Did you really think I was a student?")
        self.say("Demon", "I have eaten in this room for 400 years.")
        self.say("Demon", "Keep the stone. We will meet again...")
        self.say("Demon", "...somewhere with better catering.")
        self.lines.append(self.vanish)

    def summon(self):
        self.summoned = min(self.summoned + 1, len(self.sandwichSpots))

    def summonAll(self):
        self.summoned = len(self.sandwichSpots)

    def dropDisguise(self):
        self.disguised = False

    def vanish(self):
        self.vanishing = True

    def runLines(self):
        if self.lineTimer > 0:
            self.lineTimer -= 1
        while self.lines and self.lineTimer == 0:
            item = self.lines.pop(0)
            if callable(item):
                item() # story events happen instantly, between lines
            else:
                who, text = item
                if who is None:
                    self.chat.say(text)
                else:
                    self.chat.handle_event_npc(who, text)
                self.lineTimer = 75 # frames until the next line (~1.25 s)

    def handle_event(self, event):
        for b in self.buttons:
            b.handle_event(event)

        if self.conversation == 1:
            if self.chat.focus and self.chat.isSubmit(event):
                text = self.chat.input.strip() # grab it before the chatbox clears it
                self.chat.handle_event(event)
                if text:
                    self.answer(text)
            else:
                self.chat.handle_event(event)

    def draw(self):
        self.runLines()

        if self.vanishing: # demon and his sandwiches fade out together
            self.demonAlpha = max(self.demonAlpha - 4, 0)
            if self.demonAlpha == 0:
                self.vanishing = False
                self.conversation = 3
                self.buttons = [self.corridorButton, self.testButton, self.stoneButton]
                self.say(None, "* He's gone. Where he stood lies a yellow stone.")

        self.screen.blit(self.image, (0, 0))

        if self.conversation == 3 or self.vanishing:
            self.screen.blit(self.stone, self.stonePos)

        if self.conversation <= 2 and self.demonAlpha > 0:
            figure = self.student if self.disguised else self.demon
            figure.set_alpha(self.demonAlpha)
            self.screen.blit(figure, self.figurePos)
            self.sandwich.set_alpha(self.demonAlpha)
            for pos in self.sandwichSpots[:self.summoned]:
                self.screen.blit(self.sandwich, pos)

        if self.chat.messages:
            self.chat.draw(self.screen)
        for b in self.buttons:
            b.draw2(self.screen)