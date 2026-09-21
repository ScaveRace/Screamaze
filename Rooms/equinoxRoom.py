import random
import pygame
import UI.uiElements as u

pygame.init()

pygame.mixer.init()

class EquinoxRoom:
    stoneTaken = False # class variable, so it stays True when you come back into the room

    def __init__(self, screen):
        self.image = u.load_image("assets/sandwishRoom.png", screen.get_size()) #  will change
        self.screen = screen
        self.conversation = 0 # 0 = idle, 1 = riddles, 2 = demon revealed, 3 = stone on floor, 4 = done
        self.next_room = None

        self.stonePos = (870, 544) # centre of the yellow stone

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
        self.lastWrongLine = ""
        self.riddle = 0
        self.wrong = 0

        self.corridorButton = u.Button(400, 400, 140, 50, "corridor", self.corridor)
        self.talkButton = u.Button(760, 600, 220, 50, "talk to student", self.talk)
        self.lookAwayButton = u.Button(760, 600, 220, 50, "look away", self.lookAway)
        self.stoneButton = u.Button(770, 600, 200, 50, "take the stone", self.takeStone)

        if EquinoxRoom.stoneTaken:
            self.conversation = 4
            self.buttons = [self.corridorButton]
            self.chat.say("* Crumbs on an empty desk. Nobody here.")
        else:
            self.buttons = [self.corridorButton, self.talkButton]
            self.chat.say("* The room smells of toasted bread.")
            self.chat.say("* A student sits hunched over a book, eating.")

    def corridor(self):
        self.next_room = "corridor"

    def talk(self):
        self.conversation = 1
        self.buttons = [self.corridorButton]
        self.chat.focus = True
        self.say(None, "* He doesn't look up. He keeps chewing.")
        self.say("Student", "...mm. You're not in my class.")
        self.say("Student", "Hungry?")
        self.say(None, "* A sandwich appears in the air beside him.")
        self.say("Student", "Answer me three things, and I'll leave")
        self.say("Student", "you something better than lunch.")
        self.askRiddle()

    def lookAway(self):
        self.conversation = 3
        self.buttons = [self.corridorButton, self.stoneButton]
        self.say(None, "* You blink. He's gone. The sandwiches too.")
        self.say(None, "* Where he stood lies a yellow stone.")

    def takeStone(self):
        EquinoxRoom.stoneTaken = True # later: add "yellow_stone" to the player's inventory here
        self.conversation = 4
        self.buttons = [self.corridorButton]
        self.say(None, "* You pick up the stone. Warm as fresh toast.")

    def say(self, who, text):
        if who is None: # narration
            self.chat.say(text)
        else:
            self.chat.handle_event_npc(who, text)

    def askRiddle(self):
        for line in self.riddles[self.riddle][0]:
            self.say("Student", line)

    def answer(self, text):
        guess = text.lower().strip(" .!?'\"")
        for article in ("a ", "an ", "the "):
            if guess.startswith(article):
                guess = guess[len(article):]

        question, answers, hint = self.riddles[self.riddle]
        if guess in answers:
            self.riddle += 1
            self.wrong = 0
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
        self.buttons = [self.corridorButton, self.lookAwayButton]
        self.say(None, "* He stops chewing. Something tall stands up.")
        self.say("Demon", "SHARPER THAN THE LAST ONE.")
        self.say("Demon", "Did you really think I was a student?")
        self.say("Demon", "I have eaten in this room for 400 years.")
        self.say("Demon", "Keep the stone. We will meet again...")
        self.say("Demon", "...somewhere with better catering.")

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
        self.screen.blit(self.image, (0, 0))

        if self.conversation == 3:
            pygame.draw.circle(self.screen, (235, 200, 40), self.stonePos, 24)

        if self.chat.messages:
            self.chat.draw(self.screen)
        for b in self.buttons:
            b.draw2(self.screen)