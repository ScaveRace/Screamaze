import pygame
import UI.uiElements as u
import functions.language as lang
import functions.savingFunc as save
from functions.settingsFunc import settings as sett
from Phone.pages.basePage import BasePage
from Phone.pages.homescreen import PHONE_SIZE
from UI.pauseMenu import LANGUAGES

A = "assets/phoneIm/"

# where things are on the phone of 300 x 720, the pause menu covers the top 60
TITLE = pygame.Rect(24, 66, 252, 28)
SLIDER_X, SLIDER_W = 24, 252
LANGUAGE_BUTTON = (24, 290, 252, 44)


# the page of the gear app: music volume, sound effects volume and language, they used to be in the pause menu
class SettingsPage(BasePage):

    def __init__(self, screen, player, phone):
        super().__init__(screen, player, phone)
        self.image = u.load_alpha_image(A + "phone_bg.png", PHONE_SIZE)
        self.titleFont = pygame.font.SysFont(u.Chatbox.CHAT_FONTS, 17, bold=True)

        self.volumeSlider = u.Slider(SLIDER_X, 150, SLIDER_W, 18, "volume", sett.setMusicVolume, self.saveAction, sett.getMusicVolume())
        self.sfxSlider = u.Slider(SLIDER_X, 220, SLIDER_W, 18, "sound effects", sett.setSFXVolume, self.saveAction, sett.getSFXVolume())
        self.langButton = u.Button(*LANGUAGE_BUTTON, "", self.switchLanguage)
        self.showLanguage()

    def on_enter(self):
        self.volumeSlider.value = sett.getMusicVolume()
        self.sfxSlider.value = sett.getSFXVolume()
        self.showLanguage()

    def showLanguage(self):
        self.langButton.label = lang.ui("language") + ": " + LANGUAGES[sett.getLanguage()]

    def switchLanguage(self):
        sett.setLanguage("nl" if sett.getLanguage() == "en" else "en")
        self.showLanguage()
        self.saveAction()

    def saveAction(self):
        save.save(sett, "data/gameSettings.json")

    def handle_event(self, event):
        self.volumeSlider.handle_event(event)
        self.sfxSlider.handle_event(event)
        self.langButton.handle_event(event)

    def draw(self):
        self.screen.blit(self.image, (0, 0))
        title = self.titleFont.render(lang.ui("Settings"), True, (206, 206, 200))
        self.screen.blit(title, title.get_rect(center=TITLE.center))
        self.volumeSlider.draw(self.screen)
        self.sfxSlider.draw(self.screen)
        self.langButton.draw2(self.screen)
