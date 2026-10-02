import pygame
import UI.uiElements as u
import menu.inventory as i
import UI.pauseMenu as pause


font = pygame.font.Font(None, 24)

class FrontUI:
    def __init__(self,p,screen):
        self.player = p
        self.screen = screen
        self.visible = False
        self.inventory = i.InventoryMenu(screen,p)
        self.pause = pause.PauseMenu(screen,p)
        self.chat = u.Chatbox(0,0,300,720,font)



    def handleEvenet(self,event):
        self.inventory.handle_event(event)
        self.pause.handle_event(event)
        self.chat.handle_event(event)

    def draw(self):

        seconds = self.player.time
        timeText = font.render(f"{seconds // 60:02d}:{seconds % 60:02d}", True, (210, 200, 160))
        self.screen.blit(timeText, timeText.get_rect(topleft=(320, 30)))
        self.chat.draw(self.screen)
        self.pause.draw()
        if not self.pause.paused:
            self.inventory.draw()  # last, so it sits on top of the room
