import UI.uiElements as u
import pygame


pygame.init()
pygame.mixer.init()

clock = pygame.time.Clock()
font = pygame.font.Font(None, 28)
smallFont = pygame.font.Font(None, 20)

import functions.language as lang
from functions import uiFunc as uF
running = True

# the story before the game starts: (who says it, id of the text under FrontDesk in the language files)
STORY = [
    ("", "story_1"),
    ("", "story_2"),
    ("", "story_3"),
    ("", "story_4"),
    ("Receptionist", "story_5"),
    ("Receptionist", "story_6"),
    ("Receptionist", "story_7"),
    ("Receptionist", "story_8"),
    ("Receptionist", "story_9"),
]
PART_TIME = 4500   # how long one part of the story stays on screen, in ms
LOOK_UP = 4        # the part where the receptionist looks up, the second picture fades in here
FADE_TIME = 100    # how many frames the fade to the second picture takes



class FrontDesk:
    text = ""

    def __init__(self, screen,p):
        self.player = None
        self.animation = False ### button animation switch
        self.alpha = 0
        self.startAnim = 0 ### animation start time, set when the story reaches LOOK_UP
        self.story = [(who, lang.chatMessage("FrontDesk", msg_id) or "") for who, msg_id in STORY]
        self.part = 0 ### which part of the story is on screen
        self.partStart = pygame.time.get_ticks()
        self.next_room = None
        self.screen = screen
        self.background = u.load_image("assets/frontDesk_1.png", (self.screen.get_size()[0]+300,self.screen.get_size()[1]))
        self.secondIm = u.load_image("assets/frontDesk_2.png", (self.screen.get_size()[0]+300,self.screen.get_size()[1]))
        self.p = p
        self.buttons = [
            u.Button(1200, 290, 140, 30, "Male", self.gender),
            u.Button(1130, 350, 140, 50, "Start Run", self.startRun),

        ]
        self.textField = u.TextField(1200, 250, 140, 30,font,(255,255,255), (0,0,0),0,True)



    def gender(self):
        if self.buttons[0].label == "Male":
            self.buttons[0].label = "Female"
        else:
            self.buttons[0].label = "Male"


        # startAnim =
    def startRun(self):
        if self.textField.text.replace(" ","") != "":
            self.p.createPlayer(self.textField.text,self.buttons[0].label)
            self.next_room = "corridor"

    ########## story ##########
    def storyDone(self):
        return self.part == len(self.story) - 1

    def nextPart(self):
        if self.storyDone():
            return
        self.part += 1
        self.partStart = pygame.time.get_ticks()
        if self.part == LOOK_UP:
            self.startAnim = self.partStart + 400

    def drawStory(self):
        who, text = self.story[self.part]
        box = pygame.Rect(240, 590, 1000, 110)
        box_surface = pygame.Surface(box.size)
        box_surface.fill((25, 25, 25))
        box_surface.set_alpha(170)
        self.screen.blit(box_surface, box)
        pygame.draw.rect(self.screen, (255, 255, 255), box, 1)
        if who:
            self.screen.blit(font.render(who, True, (210, 200, 160)), (box.x + 14, box.y + 8))
        lines = uF.render_wrapped(font, text, (244, 255, 255), box.width - 60)
        self.screen.blit(lines, lines.get_rect(center=(box.centerx, box.centery + 8)))
        if not self.storyDone():
            hint = smallFont.render("click to continue", True, (150, 150, 142))
            self.screen.blit(hint, hint.get_rect(bottomright=(box.right - 10, box.bottom - 6)))

    def handle_event(self, event):
        if not self.storyDone():
            # a click skips to the next part of the story
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.nextPart()
            return
        for b in self.buttons:
            b.handle_event(event)
        self.textField.handle_event(event)

        # in draw:


    def draw(self):  ####  very complicated draw

        x = 1050
        y = 200
        rect_surface = pygame.Surface((300, 300))
        rect_outline = pygame.Rect(x,y,300,300)
        underline = pygame.Rect(x +25, y+40, 250, 1)


        rect_surface.fill((25, 25, 25))
        rect_surface.set_alpha(170)
        ########## story ###########
        if pygame.time.get_ticks() - self.partStart >= PART_TIME:
            self.nextPart()

        ########## animation ###########
        if self.alpha != 255:
            if self.part >= LOOK_UP:
                self.alpha = u.storyImageAnim(self.startAnim, self.alpha, FADE_TIME)
            self.screen.blit(self.background, (0, 0))

        ##### latest frame when alpha=255 #####
        self.secondIm.set_alpha(self.alpha)
        self.screen.blit(self.secondIm, (0, 0))
        #########  blit UI after animation  ##########
        self.drawStory()
        if self.alpha == 255 and self.storyDone():
            self.screen.blit(rect_surface, (x, y))
            pygame.draw.rect(self.screen, (255, 255, 255), rect_outline, 1)
            pygame.draw.rect(self.screen, (255, 255, 255), underline, 1)
            self.screen.blit(font.render("CREATE YOUR CHARACTER", True, (244, 255, 255)),(x + 14,y+10))
            self.textField.draw(self.screen)
            self.screen.blit(font.render("NAME", True, (244, 255, 255)),(x + 14,y+60))
            self.screen.blit(font.render("Appearance", True, (244, 255, 255)),(x + 14,y+95))
            for b in self.buttons:
                b.draw2(self.screen)
