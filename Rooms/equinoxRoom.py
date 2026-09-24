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

        self.stonePos = (870, 544) # centre of the yellow stone circle, change to move it

        self.chat = u.Chatbox(40, 470, 700, 230) # all dialogue and your typed answers show up here

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
        # what he says when you answer wrong, one is picked at random
        self.wrongLines = ["Wrong.", "Stale answer.", "No. Undercooked.", "Try again. I have all night."]
        self.lastWrongLine = "" # so he doesn't say the same wrong line twice in a row
        self.riddle = 0 # which riddle you are on (0, 1 or 2)
        self.wrong = 0 # wrong answers on the current riddle, hint shows after 2

        # all buttons are made once here, self.buttons decides which ones are on screen
        self.corridorButton = u.Button(400, 400, 140, 50, "corridor", self.corridor)
        self.talkButton = u.Button(760, 600, 220, 50, "talk to student", self.talk)
        self.lookAwayButton = u.Button(760, 600, 220, 50, "look away", self.lookAway)
        self.stoneButton = u.Button(770, 600, 200, 50, "take the stone", self.takeStone)

        # coming back after taking the stone: the room is empty
        if EquinoxRoom.stoneTaken:
            self.conversation = 4
            self.buttons = [self.corridorButton]
            self.chat.say("* Crumbs on an empty desk. Nobody here.")
        # first visit: the student is here
        else:
            self.buttons = [self.corridorButton, self.talkButton]
            self.chat.say("* The room smells of toasted bread.")
            self.chat.say("* A student sits hunched over a book, eating.")

    # "corridor" button: main.py sees next_room and switches rooms
    def corridor(self):
        self.next_room = "corridor"

    # "talk to student" button: intro lines, then the first riddle
    def talk(self):
        self.conversation = 1
        self.buttons = [self.corridorButton]
        self.chat.focus = True # so you can type right away without clicking the chatbox
        self.say(None, "* He doesn't look up. He keeps chewing.")
        self.say("Student", "...mm. You're not in my class.")
        self.say("Student", "Hungry?")
        self.say(None, "* A sandwich appears in the air beside him.")
        self.say("Student", "Answer me three things, and I'll leave")
        self.say("Student", "you something better than lunch.")
        self.askRiddle()

    # "look away" button: the demon is gone and the stone appears
    def lookAway(self):
        self.conversation = 3
        self.buttons = [self.corridorButton, self.stoneButton]
        self.say(None, "* You blink. He's gone. The sandwiches too.")
        self.say(None, "* Where he stood lies a yellow stone.")

    # "take the stone" button: the stone is picked up and won't come back
    def takeStone(self):
        EquinoxRoom.stoneTaken = True # later: add "yellow_stone" to the player's inventory here
        self.conversation = 4
        self.buttons = [self.corridorButton]
        self.say(None, "* You pick up the stone. Warm as fresh toast.")

    # puts a line in the chatbox, who = None means narration (a "* " line)
    def say(self, who, text):
        if who is None: # narration
            self.chat.say(text)
        else:
            self.chat.handle_event_npc(who, text)

    # shows the lines of the current riddle
    def askRiddle(self):
        for line in self.riddles[self.riddle][0]:
            self.say("Student", line)

    # checks what you typed against the current riddle
    def answer(self, text):
        # clean up the answer so "The Bread." counts the same as "bread"
        guess = text.lower().strip(" .!?'\"")
        for article in ("a ", "an ", "the "):
            if guess.startswith(article):
                guess = guess[len(article):]

        question, answers, hint = self.riddles[self.riddle]
        if guess in answers: # right: next riddle, or the reveal after the last one
            self.riddle += 1
            self.wrong = 0
            if self.riddle < len(self.riddles):
                self.say("Student", random.choice(["Correct.", "Mm. Correct.", "...Correct."]))
                self.askRiddle()
            else:
                self.reveal()
        else: # wrong: a wrong line, plus the hint from the 2nd try on
            self.wrong += 1
            line = random.choice([l for l in self.wrongLines if l != self.lastWrongLine])
            self.lastWrongLine = line
            self.say("Student", line)
            if self.wrong >= 2:
                self.say("Student", hint)

    # all riddles solved: the student turns out to be the demon
    def reveal(self):
        self.conversation = 2
        self.chat.focus = False # typing does nothing from here on
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
        self.chat.handle_event(event)

        # the chatbox when riddles
        if self.conversation == 1:
            if self.chat.focus and self.chat.isSubmit(event):
                text = self.chat.input.strip() # grab it before the chatbox clears it
                self.chat.handle_event(event)
                if text: # ignore empty enters
                    self.answer(text)
            else:
                self.chat.handle_event(event)

    def draw(self):
        self.screen.blit(self.image, (0, 0)) # background

        if self.conversation == 3: # stone lies on the floor until you take it
            pygame.draw.circle(self.screen, (235, 200, 40), self.stonePos, 24)

        if self.chat.messages: # only draw the chatbox when there is text in it
            self.chat.draw(self.screen)
        for b in self.buttons:
            b.draw2(self.screen)