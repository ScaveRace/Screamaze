import UI.uiElements as u
import pygame


pygame.init()
pygame.mixer.init()

clock = pygame.time.Clock()
font = pygame.font.Font(None, 28)

from functions.settingsFunc import settings as sett
import functions.sound as s
running = True



class FrontDesk:
    text = ""

    def __init__(self, screen,p):
        self.player = None
        self.animation = False ### button animation switch
        self.alpha = 0
        self.startAnim = pygame.time.get_ticks() + 800 ### animation start time
        self.next_room = None
        self.screen = screen
        self.background = u.load_image("assets/frontDesk_1.png", (self.screen.get_size()[0]+300,self.screen.get_size()[1]))
        self.secondIm = u.load_image("assets/frontDesk_2.png", (self.screen.get_size()[0]+300,self.screen.get_size()[1]))
        self.bgMusic = "assets/music/The_Unmarked_Door.mp3"

        s.play_music(self.bgMusic,sett, .4)
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
        self.p.createPlayer(self.textField.text,self.buttons[0].label)
        self.next_room = "corridor"

    def handle_event(self, event):
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
        ########## animation ###########
        if self.alpha != 255:
            self.alpha = u.storyImageAnim(self.startAnim, self.alpha, 100)
            self.screen.blit(self.background, (0, 0))

        ##### latest frame when alpha=255 #####
        self.secondIm.set_alpha(self.alpha)
        self.screen.blit(self.secondIm, (0, 0))
        #########  blit UI after animation  ##########
        if self.alpha == 255:
            self.screen.blit(rect_surface, (x, y))
            pygame.draw.rect(self.screen, (255, 255, 255), rect_outline, 1)
            pygame.draw.rect(self.screen, (255, 255, 255), underline, 1)
            self.screen.blit(font.render("CREATE YOUR CHARACTER", True, (244, 255, 255)),(x + 14,y+10))
            self.textField.draw(self.screen)
            self.screen.blit(font.render("NAME", True, (244, 255, 255)),(x + 14,y+60))
            self.screen.blit(font.render("Appearance", True, (244, 255, 255)),(x + 14,y+95))
            for b in self.buttons:
                b.draw2(self.screen)
