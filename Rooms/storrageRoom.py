import pygame
import UI.uiElements as u
from functions import uiFunc as uF
import roomFunc.stoRoomFunc as sF

pygame.init()
pygame.mixer.init()

QUESTION_COLOUR = (30, 25, 20)  # text colour of the question on the quiz paper


########## storage room class ##########
class StorrageRoom:

    def __init__(self, screen, player, fui):
        self.screen = screen
        self.player = player
        self.fui = fui
        self.next_room = None

        self.questionFont = pygame.font.Font(None, 34)
        self.fieldoftext = u.TextField(1100, 600, 100, 60)

        self.images = {}
        self.buttons = {}
        self.masks = {}
        self.getElements()

    def getElements(self):
        tmp = sF.getElements(self.player, self.fui, self.screen)
        self.images = tmp[0]
        self.buttons = tmp[1]
        self.masks = tmp[2]

    ########## handle user input depending on current view ##########
    def handle_event(self, event):
        self.dispatch(event)
        self.next_room = sF.next_room
        sF.next_room = None

    def dispatch(self, event):
        # snapshot both lists first, so a click that changes the view
        # can't also click something in the new view
        masks = sF.activeMasks()
        buttons = list(sF.currentButtons())
        viewBefore = sF.view

        for m in masks:
            m.handle_event(event)
            if sF.view != viewBefore:
                return

        for b in buttons:
            b.handle_event(event)
            if sF.view != viewBefore:
                return

        if sF.view == sF.View.ROOM:
            self.fieldoftext.handle_event(event)

    ########## draw the current storage room view ##########
    def draw(self):
        self.screen.blit(self.images[sF.view], (300, 0))

        if sF.view == sF.View.QUIZ:
            question = sF.quiz.current_question()[0]
            text = uF.render_wrapped(self.questionFont, question, QUESTION_COLOUR, 600)
            self.screen.blit(text, text.get_rect(midbottom=(sF.centerX, 285)))

        for m in sF.activeMasks():
            m.draw(self.screen)

        for b in sF.currentButtons():
            b.draw2(self.screen)

        if sF.view == sF.View.ROOM:
            self.fieldoftext.draw(self.screen)
