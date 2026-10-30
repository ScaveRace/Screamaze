import pygame
import UI.uiElements as u
import menu.inventory as i
import UI.pauseMenu as pause
import functions.language as lang
from Phone.PhoneUI import Phone


font = pygame.font.Font(None, 24)

class FrontUI:
    def __init__(self,p,screen,aria):
        self.aria = aria
        self.player = p
        self.screen = screen
        self.visible = False
        self.inventory = i.InventoryMenu(screen,p)
        self.pause = pause.PauseMenu(screen,p)
        self.pauseButton = u.Button(1370, 20, 90, 36, "pause", self.pause.toggle)
        self.showAiChat = False          # which chat the phone shows: False the NPC talks (the chat app), True the AI chat (the handset app)
        self.phone = Phone(screen,p,self)     # the phone is where the chat was, the chats of the phone are Chatboxes
        self.chat = self.phone.chat           # the NPC talks, the rooms add theirs here
        self.aiChat = self.phone.aiChat       # the AI chat
        self.db = lang   # the rooms get their texts with fui.db.chatMessage(room, id)

    def reset(self):
        for chat in (self.chat, self.aiChat):
            chat.messages.clear()
            chat.input = ""
            chat.focus = False
            chat.scroll = 0
        self.showAiChat = False
        self.inventory.open = False
        self.pause.paused = False

    def sendMessage(self,npc,roomName,msg_id):
        self.chat.sayKey(npc,roomName,msg_id)

    def getMessage(self):
        print(self.chat.messages)
        return
    def handleEvenet(self,event):
        if self.pause.handle_event(event):
            return True
        self.inventory.handle_event(event)
        self.pauseButton.handle_event(event)
        self.phone.handle_event(event)
        return False

    def draw(self):

        seconds = self.player.time
        timeText = font.render(f"{seconds // 60:02d}:{seconds % 60:02d}", True, (210, 200, 160))
        self.screen.blit(timeText, timeText.get_rect(topleft=(320, 30)))
        self.phone.draw()
        self.pauseButton.draw2(self.screen)
        self.pause.draw()
        if not self.pause.paused:
            self.inventory.draw()  # last, so it sits on top of the room
