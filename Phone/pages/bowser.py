import UI.uiElements as u
from Phone.pages.basePage import BasePage
from Phone.pages.homescreen import PHONE_SIZE

A = "assets/phoneIm/"
PHONE_SIZE = (300,720)

class Browser(BasePage):

    def __init__(self,screen,player,phone):
        super().__init__(screen,player,phone)
        self.image = u.load_alpha_image(A+"phone_bg.png",PHONE_SIZE)
        self.getElements()

    def getElements(self):
        self.textField = u.TextField(50,350,200,50)

    def on_enter(self):
        pass

    def handle_event(self, event):
        self.textField.handle_event(event)

    def draw(self):
        self.screen.blit(self.image,(0,0))
        self.textField.draw(self.screen)



