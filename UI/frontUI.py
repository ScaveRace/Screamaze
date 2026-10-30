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
        self.inventory.say = self.sendMessage   # pressing an item in the inventory tells its text in the chat
        self.pause = pause.PauseMenu(screen,p)
        self.pauseButton = u.Button(1370, 20, 90, 36, "pause", self.pause.toggle)
        self.phone = Phone(screen,p,self)     # the phone is where the chat was, the chats of the phone are Chatboxes
        self.chat = self.phone.chat           # the NPC talks, the rooms add theirs here
        self.aiChat = self.phone.aiChat       # the AI chat, the browser page of the phone
        self.db = lang   # the rooms get their texts with fui.db.chatMessage(room, id)

    def reset(self):
        for chat in (self.chat, self.aiChat):
            chat.messages.clear()
            chat.input = ""
            chat.focus = False
            chat.scroll = 0
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
        self.phone.draw()
        self.pauseButton.draw2(self.screen)
        self.pause.draw()
        if not self.pause.paused:
            self.inventory.draw()  # last, so it sits on top of the room
