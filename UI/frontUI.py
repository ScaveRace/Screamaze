import pygame
import UI.uiElements as u
import functions.sound as s
from functions.settingsFunc import settings as sett
import functions.savingFunc as save

font = pygame.font.Font(None, 36)


class PauseMenu:
    def __init__(self, screen,player):
        self.screen = screen
        self.paused = False
        self.pauseButton = u.Button(1170, 20, 90, 36, "pause", self.toggle)
        self.buttons = [
            u.Button(570, 330, 140, 44, "save game", self.saveGame),
            u.Button(570, 390, 140, 44, "resume", self.toggle),
        ]
        self.player = player
        self.volumeSlider = u.Slider(490, 280, 300, 18, "volume",sett.setMusicVolume,self.saveAction,sett.getMusicVolume())

    def toggle(self):
        self.paused = not self.paused
        self.buttons[0].label = "save game"


    def saveGame(self):
        save.save(self.player,"data/savePlayer.json")
        self.buttons[0].label = "saved!"



    def saveAction(self):
        print("works")
        save.save(sett, "data/gameSettings.json")

    def handle_event(self, event):
        # returns True when the pause menu used the event, so the room ignores it
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:

            self.toggle()
            return True

        self.pauseButton.handle_event(event)

        if self.paused:
            self.volumeSlider.handle_event(event)
            for b in self.buttons:
                b.handle_event(event)
            return True
        return False

    def draw(self):
        self.pauseButton.draw2(self.screen)
        self.screen.blit(
            font.render(f"{self.player.name}", True, (210, 200, 160)),(10, 10))
        if self.paused:
            panel = pygame.Rect(440, 180, 400, 290)
            pygame.draw.rect(self.screen, (0, 0, 0), panel)
            pygame.draw.rect(self.screen, (255, 255, 255), panel, 1)
            title = font.render("PAUSED", True, (255, 255, 255))
            self.screen.blit(title, title.get_rect(center=(640, 215)))
            self.volumeSlider.draw(self.screen)
            for b in self.buttons:
                b.draw2(self.screen)