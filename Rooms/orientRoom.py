# here you will find all the informations about teh rooms and what tehy need

#first you need to initialize the pygame and import it:
import pygame
#also import ui elements to use them as u to make it easier later
import UI.uiElements as u

pygame.init()
#teh mixer is for the music later
pygame.mixer.init()



#create a class called the way your room should be called

class Room:
    #initialization is the first step here you add everything your room needs
    #from the start on wile also important that the first line always stays the same
    def __init__ (self, screen):
        #add what you need
        #assets should be added to the assets folder and load image you can find in the ui element to better understand them
        self.image = u.load_image("assets/corridor.png",screen.get_size())
        #self if for everything inside teh clas as you can see that i used screen above taht is because it came from the () in the init
        # this will not bes possible outside so we save it as self
        self.screen = screen
        # next room needs to exist exactly liek this with none
        self.next_room = None
        #for buttons adn other lements you need to add them eighter one by one or in lists
        self.buttons = [
            u.Button(930, 350, 140, 50, "Start Run", self.action, 0, 0, 0, (255, 255, 255), "center"),
            u.Button(200, 350, 140, 50, "Start Run", self.action),
        ]
        #i made buttons and others very variabel abeove you see the min and max you can add as informations
        self.textF = u.TextField(200, 350, 140, 50, "Start Run",(255,255,255),(0,0,0),128, True)


    #function that we definded for the buttons
    def action(self):
        print("Action")

    #handle event comes from the main function and needs to exist it is 100% needed, evenet is everything happening like mouse or keyboard given from main
    def handle_event(self,event):
        #as we have many buttons:
        for b in self.buttons: #self is needed as they come from init, b doesn t have to be defined as it just takes the next button until there is none
            b.handle_event(event)
        #for the single one like here the text field:
        self.textF.handle_event(event)


    #then we need to draw the buttons and text fields or more needs to exist, comes from main
    def draw(self):
        self.screen.blit(self.image,(0,0)) #screen means where, blit means add,image here is what i add and 0.0 the position
        #for multiple items maybe buttons:
        for b in self.buttons:
            b.draw2(self.screen)
        self.textF.draw(self.screen)
