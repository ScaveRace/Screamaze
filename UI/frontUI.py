import pygame
import UI.uiElements as u
import menu.inventory as i
import UI.pauseMenu as pause
import functions.loreFunctions as lF


font = pygame.font.Font(None, 24)

class FrontUI:
    def __init__(self,p,screen):
        self.player = p
        self.screen = screen
        self.visible = False
        self.inventory = i.InventoryMenu(screen,p)
        self.pause = pause.PauseMenu(screen,p)
        self.pauseButton = u.Button(1370, 20, 90, 36, "pause", self.pause.toggle)
        self.chat = u.Chatbox(0,0,300,720,font)
        self.db = lF.StoryDB()
        self.lang = "en"


    def sendMessage(self,npc,roomName,msg_id):
        self.chat.handle_event_npc(npc,self.db.chatMessage(roomName,msg_id,self.lang))

    def getMessage(self):
        print(self.chat.messages)
        return
    def handleEvenet(self,event):
        if self.pause.handle_event(event):
            return True
        self.inventory.handle_event(event)
        self.pauseButton.handle_event(event)
        self.chat.handle_event(event)
        return False

    def draw(self):

        seconds = self.player.time
        timeText = font.render(f"{seconds // 60:02d}:{seconds % 60:02d}", True, (210, 200, 160))
        self.screen.blit(timeText, timeText.get_rect(topleft=(320, 30)))
        self.chat.draw(self.screen)
        self.pauseButton.draw2(self.screen)
        self.pause.draw()
        if not self.pause.paused:
            self.inventory.draw()  # last, so it sits on top of the room
