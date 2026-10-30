import pygame
import UI.uiElements as u
import functions.sound as s
from functions.settingsFunc import settings as sett
import functions.savingFunc as save
import functions.leaderboard as lb
import functions.language as lang


font = pygame.font.Font(None, 36)

LANGUAGES = {"en": "English", "nl": "Nederlands"}   # language code -> name on the button


class PauseMenu:
    def __init__(self, screen,player,canSave=True):
        self.screen = screen
        self.paused = False
        # in the game the settings are in the gear app of the phone, the startup menu has no phone so its settings stay here
        self.hasSettings = not canSave
        self.saveButton = u.Button(870, 385, 140, 44, "save game", self.saveGame)
        self.langButton = u.Button(840, 385, 200, 44, "", self.switchLanguage)
        self.buttons = [
            self.saveButton,
            u.Button(870, 440, 140, 44, "resume", self.toggle),
        ]
        if self.hasSettings:
            self.buttons.insert(0, self.langButton)
        if not canSave:   # the startup menu has no game to save yet
            self.buttons.remove(self.saveButton)
        self.firstButtonY = 385 if self.hasSettings else 255
        for i, b in enumerate(self.buttons):   # stack the buttons under the sliders, or at the top when there are none
            b.rect.y = self.firstButtonY + i * 55
        self.showLanguage()
        self.player = player
        self.volumeSlider = u.Slider(790, 280, 300, 18, "volume",sett.setMusicVolume,self.saveAction,sett.getMusicVolume())
        self.sfxSlider = u.Slider(790, 335, 300, 18, "sound effects", sett.setSFXVolume, self.saveAction, sett.getSFXVolume())



    def toggle(self):
        self.paused = not self.paused
        self.saveButton.label = "save game"
        # the volume can also be changed from the other pause menu, so show the current one
        self.volumeSlider.value = sett.getMusicVolume()
        self.sfxSlider.value = sett.getSFXVolume()
        self.showLanguage()

    def showLanguage(self):
        self.langButton.label = lang.ui("language") + ": " + LANGUAGES[sett.getLanguage()]

    def switchLanguage(self):
        sett.setLanguage("nl" if sett.getLanguage() == "en" else "en")
        self.showLanguage()
        self.saveAction()


    def saveGame(self):
        save.save(self.player,"data/savePlayer.json")
        lb.saveRun(self.player)   # a saved run also goes on the leaderboard
        self.saveButton.label = "saved!"



    def saveAction(self):
        save.save(sett, "data/gameSettings.json")

    def handle_event(self, event):
        # returns True when the pause menu used the event, so the room ignores it
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:

            self.toggle()
            return True

        if self.paused:
            if self.hasSettings:
                self.volumeSlider.handle_event(event)
                self.sfxSlider.handle_event(event)
            for b in self.buttons:
                b.handle_event(event)
            return True
        return False

    def draw(self):


        if self.paused:
            panel = pygame.Rect(740, 180, 400, self.firstButtonY - 175 + len(self.buttons) * 55)
            pygame.draw.rect(self.screen, (0, 0, 0), panel)
            pygame.draw.rect(self.screen, (255, 255, 255), panel, 1)
            title = font.render("PAUSED", True, (255, 255, 255))
            self.screen.blit(title, title.get_rect(center=(940, 215)))
            if self.hasSettings:
                self.volumeSlider.draw(self.screen)
                self.sfxSlider.draw(self.screen)
            for b in self.buttons:
                b.draw2(self.screen)