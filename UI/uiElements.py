import pygame
from functions import uiFunc as uF
import data.maskPositions as mP
import functions.language as lang

pygame.font.init()  #### fonts need to be initialized before using them

startX = 300

##basic functions
def load_image(path, size, fallback=(40,38,42)):  ###  loading images, has fallbacks (very useful)
    try:
        image = pygame.image.load(path).convert() #if we do convert_alpha() we also have the transparency else it is black
        return pygame.transform.smoothscale(image, (size[0]-startX,size[1]))  # image by default is fullscreen, but given a size change it to the room size
    except (pygame.error, FileNotFoundError):  ### in case of an error, still functions
        surface = pygame.Surface(size)
        surface.fill(fallback)
        return surface

def load_alpha_image(path, size, fallback=(40,38,42)):  ###  loading images, has fallbacks (very useful)
    try:
        image = pygame.image.load(path).convert_alpha() #if we do convert_alpha() we also have the transparency else it is black
        return pygame.transform.smoothscale(image, (size[0],size[1]))  # image by default is fullscreen, but given a size change it to the room size
    except (pygame.error, FileNotFoundError):  ### in case of an error, still functions
        surface = pygame.Surface(size)
        surface.fill(fallback)
        return surface

def storyImageAnim(startAnim,alpha,fadetime):  ##  transition between images, when it starts, takes alpha and returns it to decide when to stop
    if startAnim <= pygame.time.get_ticks() and alpha < 255:
        alpha = min(alpha + 255 / fadetime, 255)
    return alpha

def butImageAnim(alpha,fadetime):  ##  same thing
    alpha = min(alpha + 255 / fadetime, 255)
    return alpha




##button setup
class Button:

    def __init__(self,x,y,w,h,label,action):  ## inits decide what information is within a button. Easy to reference
        self.rect = pygame.Rect(x,y,w,h)

        self.label = label #text of the button
        self.action = action #function to be called
        self.bgCol = (0,0,0)
        self.fgCol = (255,255,255),
        self.outline = 0 # 0 = if you hover, 1 equals always
        self.align = "center" #left,right or center
        self.hoverCol =(128,128,128) #color when hovering background
        self.font = pygame.font.Font(None, 28)

    def handle_event(self, event):  ## when you have pressed (released) a button, the button does the function inside it
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.action()


    def draw2(self,screen):   ##  will change, but every UI class has their own draw function
        hovered = self.rect.collidepoint(pygame.mouse.get_pos())  ## changes look upon mouse above the button  ##
        text = lang.ui(self.label)    # self.label stays the id, the text follows the chosen language
        if hovered:
            pygame.draw.rect(screen, self.hoverCol, self.rect)
            if self.outline == 0 or self.outline == 1:
                pygame.draw.rect(screen, self.fgCol, self.rect, 1)
            label = self.font.render(text, True, self.fgCol)
        else:
            pygame.draw.rect(screen, self.bgCol, self.rect)
            if self.outline == 1:
                pygame.draw.rect(screen, self.fgCol, self.rect, 1)
            label = self.font.render(text, True, (222, 222, 214))
        if self.align == "left":        ## alignment of text
            screen.blit(label, label.get_rect(midleft=(self.rect.x + 14, self.rect.centery)))
        elif self.align == "right":     ## needs testing
            screen.blit(label, label.get_rect(midright=(self.rect.x + 14, self.rect.centery)))
        else:
            pos = label.get_rect(center=self.rect.center)
            screen.blit(label, pos)



 

#########  one message in the chatbox  ########
##  a message from the language files is kept as (table, id) and looked up again every time it is drawn, so the old messages follow the language
##  a message the player typed has no id, it stays as it was typed
class Message:
    def __init__(self, who="", table=None, messageID=None, values=None, text=""):
        self.who = who.strip().rstrip(":").strip()     ## "Thuas: " and "Thuas" are the same speaker
        self.table = table
        self.messageID = messageID
        self.values = values        ## fills the {} in the text
        self.text = text

    def body(self):
        if self.table is None:
            return self.text
        text = lang.chatMessage(self.table, self.messageID) or ""
        if self.values is not None:
            text = text.format(**self.values)
        return text


#########  A chatbox is used for NPC talking or player talking, the rows change grey every time the speaker changes ########
class Chatbox:
    CHAT_FONTS = "segoeui,helveticaneue,arial,dejavusans,liberationsans,notosans,freesans"   ## clean sans-serif, the first one on this computer

    def __init__(self,x,y,w,h,font = None,nameFont = None):
        self.rect = pygame.Rect(x,y,w,h)
        self.viewRect = pygame.Rect(x,y,w,h-46)            ## the messages
        self.inputRect = pygame.Rect(x,y+h-38,w,38)        ## the line the player types in
        self.messages = []
        self.input = ""
        self.focus = False
        self.font = font or pygame.font.SysFont(self.CHAT_FONTS, 15)
        self.nameFont = nameFont or pygame.font.SysFont(self.CHAT_FONTS, 13, bold = True)
        self.scroll = 0     ## pixels up from the newest message, gets clamped in draw
        self.count = 0      ## how many messages there were last frame, to jump to a new one
        self.unread = False ## a message came and the chat was not open, the phone shows a red dot

    def say(self,text): ### a message that is not in the language files, "Name > text" or just text
        who, sep, rest = text.partition(" > ")
        if not sep:
            who, rest = "", text
        self.add(Message(who, text = rest))

    def sayKey(self,who,table,messageID,**values): ### a message from the language files, values fill the {} in it
        self.add(Message(who, table, messageID, values if values else None))

    def add(self,message):
        message.body()      ## a wrong table or id shows up here, where the room said it
        self.messages.append(message)
        self.unread = True

    def handle_event(self,event):   ###  if text was added, create that as well
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.focus = uF.focused(event,self.inputRect)
        if event.type == pygame.MOUSEWHEEL and self.viewRect.collidepoint(pygame.mouse.get_pos()):
            self.scroll += event.y * 36

        if not self.focus:
            return
        if self.isSubmit(event):
            text = self.input.strip()
            self.input = ""
            if text:
                self.add(Message("You", text = text))
        else:
            self.input = uF.handle_text_event(self.input,event)[:200]

    def isSubmit(self,event):  ###  enters upon user pressing enter (return)
        return event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN

    ###  cuts every message in lines, the grey changes every time the speaker changes
    ###  the messages are looked up again every frame, that is why they follow the language
    def getRows(self):
        rows = []
        grey = 0
        speaker = None
        for message in self.messages:
            first = message.who != speaker      ## the first message of this speaker, only that one has the name
            if first and speaker is not None:
                grey = 1 - grey
            speaker = message.who

            textY = 7 if first else 2
            if first and message.who:
                textY += self.nameFont.get_linesize()
            lines = uF.wrap_lines(self.font, message.body(), self.viewRect.width - 26)
            height = textY + len(lines) * self.font.get_linesize() + 7
            rows.append({"who": message.who if first else "", "lines": lines, "grey": grey, "textY": textY, "height": height})
        return rows

    def draw(self, screen):
        view = self.viewRect
        pygame.draw.rect(screen, (22, 22, 25), view, border_radius=6)

        rows = self.getRows()
        total = sum(row["height"] for row in rows)
        if len(rows) != self.count:
            self.scroll = 0                 ## a new message, show it
            self.count = len(rows)
        self.scroll = max(0, min(self.scroll, total - view.height))

        # the newest message sits at the bottom, everything outside of the view is cut off
        greys = ((30, 30, 34), (42, 42, 47))
        y = view.bottom - total + self.scroll       ## scrolling up pushes the messages down, so older ones come into view
        screen.set_clip(view)
        for row in rows:
            if view.top - row["height"] < y < view.bottom:
                pygame.draw.rect(screen, greys[row["grey"]], (view.x, y, view.width, row["height"]))
                if row["who"]:
                    colour = (140, 190, 255) if row["who"] == "You" else (232, 190, 120)
                    screen.blit(self.nameFont.render(row["who"], True, colour), (view.x + 10, y + 7))
                lineY = y + row["textY"]
                for line in row["lines"]:
                    screen.blit(self.font.render(line, True, (206, 206, 200)), (view.x + 10, lineY))
                    lineY += self.font.get_linesize()
            y += row["height"]
        screen.set_clip(None)

        # scroll bar, only when there is something to scroll
        if total > view.height:
            thumb = max(20, view.height * view.height // total)
            thumbY = view.y + (view.height - thumb) * (total - view.height - self.scroll) // (total - view.height)
            pygame.draw.rect(screen, (90, 88, 96), (view.right - 5, thumbY, 3, thumb), border_radius=2)

        self.drawInput(screen, greys[1])

    def drawInput(self, screen, grey):
        pygame.draw.rect(screen, grey, self.inputRect, border_radius=10)
        pygame.draw.rect(screen, (110, 110, 120) if self.focus else (60, 58, 64), self.inputRect, 1, border_radius=10)

        shown = self.input
        colour = (206, 206, 200)
        if not shown and not self.focus:
            shown, colour = lang.ui("Type a message"), (120, 120, 128)
        else:
            ###  the line is only so wide, so when the text is too long to fit we cut letters off the front
            ###  until the rest fits, so you always see the end of what you type, where the cursor is
            ###  the whole text is still kept in self.input and sent when you press enter
            while shown and self.font.size(shown + "|")[0] > self.inputRect.width - 20:
                shown = shown[1:]
            if self.focus and (pygame.time.get_ticks() // 500) % 2 == 0:
                shown += "|"
        text = self.font.render(shown, True, colour)
        screen.blit(text, text.get_rect(midleft=(self.inputRect.x + 10, self.inputRect.centery)))



class TextField:
    ## easy to use defaults ##
    def __init__(self,x,y,w,h,font = pygame.font.Font(None,28), fgCol = (255,255,255), bgCol = (0,0,0), bgAlpha = 255, outline = False):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.font = font
        self.fgCol = fgCol
        self.bgCol = bgCol
        self.bgAlpha = bgAlpha
        self.outline = outline
        self.text = ""
        self.focus = False

    def handle_event(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.focus = uF.focused(event,pygame.Rect(self.x,self.y,self.w,self.h))
        if self.focus:
            self.text = uF.handle_text_event(self.text,event)


    def draw(self,screen):
        bg = pygame.Surface((self.w,self.h))
        bg.fill(self.bgCol)
        bg.set_alpha(self.bgAlpha)

        outline = pygame.Rect(self.x,self.y,self.w,self.h)
        screen.blit(bg,(self.x,self.y))
        if self.outline:
            pygame.draw.rect(screen, self.fgCol,outline,1)
        shown = self.text
        if self.focus and (pygame.time.get_ticks() // 500) % 2 == 0:
            shown += "|"  ## nice animation
        screen.blit(self.font.render(shown, True, self.fgCol), (self.x+2, self.y+4))


class Mask:
    def __init__(self, image, size, pos, action, label=""):
        self.action = action

        self.image = pygame.image.load(image).convert_alpha()
        w, h = size[0]-startX, size[1]
        self.imageX, self.imageY = pos
        if image in mP.CUT:
            # this picture was cut down to its shape: put it back where it sat in the full picture
            x, y, fullW, fullH = mP.CUT[image]
            cutW, cutH = self.image.get_size()
            left, top = round(x * w / fullW), round(y * h / fullH)
            right, bottom = round((x + cutW) * w / fullW), round((y + cutH) * h / fullH)
            w, h = max(1, right - left), max(1, bottom - top)
            self.imageX += left
            self.imageY += top
        self.image = pygame.transform.scale(self.image, (w, h))
        self.imageX+=startX
        self.imageMask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=pos)

        self.font = pygame.font.SysFont("Arial", 11)
        self.label = label

        # Center of the non-transparent part
        shape = self.image.get_bounding_rect().move(self.imageX, self.imageY)
        self.labelWidth = shape.width - 20
        self.labelCentre = shape.center
        self.showLabel()

        self.outlineColor = (128, 128, 128)
        self.hovering = False

    # the label text follows the chosen language, it is drawn again when that changes
    def showLabel(self):
        self.labelText = lang.ui(self.label)
        self.labelSurf = uF.render_wrapped(self.font, self.labelText, (255, 255, 255), self.labelWidth)
        self.labelRect = self.labelSurf.get_rect(center=self.labelCentre)

    def handle_event(self, event):
        mouseX, mouseY = getattr(event, "pos", pygame.mouse.get_pos())
        localX = mouseX - self.imageX
        localY = mouseY - self.imageY
        maskW, maskH = self.imageMask.get_size()

        self.hovering = (0 <= localX < maskW and 0 <= localY < maskH
                         and self.imageMask.get_at((localX, localY)))

        if self.hovering and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.action()

    def draw(self, screen):
        screen.blit(self.image, (self.imageX, self.imageY))
        if lang.ui(self.label) != self.labelText:
            self.showLabel()
        screen.blit(self.labelSurf, self.labelRect)
        outline = self.imageMask.outline()
        if self.hovering:
            pygame.draw.lines(screen, (128, 0, 0), True,
                              [(x + self.imageX, y + self.imageY) for x, y in outline], 2)

        else:
            pygame.draw.lines(screen, self.outlineColor, True,
                              [(x + self.imageX, y + self.imageY) for x, y in outline], 1)
class Slider:
    def __init__(self, x, y, w, h, label, action,action2, value=1.0, knob_w=16):
        self.rect = pygame.Rect(x, y, w, h)
        self.label = label
        self.action = action          # called with the new value, 0.0 - 1.0
        self.action2 = action2
        self.value = max(0.0, min(1.0, value))
        self.knob_w = knob_w
        self.dragging = False

        self.trackCol = (60, 58, 64)
        self.fillCol = (150, 150, 142)
        self.knobCol = (222, 222, 214)
        self.hoverCol = (255, 255, 255)
        self.fgCol = (222, 222, 214)
        self.font = pygame.font.Font(None, 24)

    def knob_rect(self):
        travel = self.rect.w - self.knob_w
        return pygame.Rect(self.rect.x + int(travel * self.value),
                           self.rect.y, self.knob_w, self.rect.h)

    def set_from_mouse(self, mouse_x):
        travel = self.rect.w - self.knob_w

        if travel <= 0:
            return
        # centre the knob on the cursor
        offset = mouse_x - self.knob_w / 2 - self.rect.x
        self.value = max(0.0, min(1.0, offset / travel))

        if self.action:
            print(self.value)
            self.action(self.value)


    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.set_from_mouse(event.pos[0])   # click anywhere to jump

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.action2()
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.set_from_mouse(event.pos[0])

    def draw(self, screen):
        knob = self.knob_rect()
        pygame.draw.rect(screen, self.trackCol, self.rect)
        pygame.draw.rect(screen, self.fillCol,
                         pygame.Rect(self.rect.x, self.rect.y,
                                     knob.centerx - self.rect.x, self.rect.h))
        hovered = knob.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(screen, self.hoverCol if (hovered or self.dragging)
                         else self.knobCol, knob)

        text = self.font.render(f"{self.label}   {int(self.value * 100)}%",
                                True, self.fgCol)
        screen.blit(text, (self.rect.x, self.rect.y - 26))
