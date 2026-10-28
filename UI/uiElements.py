import pygame
from functions import uiFunc as uF
import data.maskPositions as mP

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
        if hovered:
            pygame.draw.rect(screen, self.hoverCol, self.rect)
            if self.outline == 0 or self.outline == 1:
                pygame.draw.rect(screen, self.fgCol, self.rect, 1)
            label = self.font.render(self.label, True, self.fgCol)
        else:
            pygame.draw.rect(screen, self.bgCol, self.rect)
            if self.outline == 1:
                pygame.draw.rect(screen, self.fgCol, self.rect, 1)
            label = self.font.render(self.label, True, (222, 222, 214))
        if self.align == "left":        ## alignment of text
            screen.blit(label, label.get_rect(midleft=(self.rect.x + 14, self.rect.centery)))
        elif self.align == "right":     ## needs testing
            screen.blit(label, label.get_rect(midright=(self.rect.x + 14, self.rect.centery)))
        else:
            pos = label.get_rect(center=self.rect.center)
            screen.blit(label, pos)



 

#########  A chatbox is used for NPC talking or player talking, needs rework to create text boundaries ########
class Chatbox:


    def __init__(self,x,y,w,h,font = pygame.font.Font(None, 28)):
        self.rect = pygame.Rect(x,y,w,h)
        self.messages = []
        self.input = ""
        self.focus = False
        self.font = font  ### make it used standard font, can decide a different one.
        self.scroll = 0
        self.scrollRect = None
        self.startScroll = None

    def say(self,text): ### simple get a new messages
        self.messages.append(text)
        self.scroll = 0  ## jump back to the newest message

    def handle_event(self,event):   ###  if text was added, create that as well
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.focus = uF.focused(event,self.rect)
        if event.type == pygame.MOUSEWHEEL and self.rect.collidepoint(pygame.mouse.get_pos()):
            self.scroll += event.y  ## gets clamped in draw

        if self.focus:
            if(self.isSubmit(event)):
                text = self.input.strip()
                self.input = ""
                if text:
                    self.say(f"You > {text}")
            else:
                self.input = uF.handle_text_event(self.input,event)

    def handle_event_npc(self,npc, message_npc):  ###  prints message as NPC
        self.say(f"{npc} > {message_npc}")

    def isSubmit(self,event):  ###  enters upon user pressing enter (return)
        return event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN

    def draw(self, screen):
        pygame.draw.rect(screen, (26, 25, 28), self.rect)  ## background
        pygame.draw.rect(screen, (60, 58, 64), self.rect, 1)  ## outline
        max_w = self.rect.width - 20

        # Input line: show only the end if it's too long
        shown = "> " + self.input
        while self.font.size(shown + "|")[0] > max_w and len(shown) > 2:
            shown = shown[:2] + shown[3:]  ## drop the oldest character after "> "
        if self.focus and (pygame.time.get_ticks() // 500) % 2 == 0:
            shown += "|"
        screen.blit(self.font.render(shown, True, (222, 222, 214)),
                    (self.rect.x + 10, self.rect.bottom - 34))

        # Messages: wrap only the text next to the name, then draw from the bottom up
        rows = []  ## (name, indent, line), name is empty on wrapped lines
        for message in self.messages:
            speaker, sep, text = message.partition(" > ")
            if not sep:
                speaker, text = "", message  ## no name in front, use the full width
            name = speaker + sep
            indent = self.font.size(name)[0]
            for i, line in enumerate(uF.wrap_lines(self.font, text, max_w - indent)):
                rows.append((name if i == 0 else "", indent, line))
        line_h = self.font.get_linesize()
        visible = (self.rect.height - 54) // line_h
        self.scroll = max(0, min(self.scroll, len(rows) - visible))
        y = self.rect.bottom - 44
        for name, indent, line in reversed(rows[:len(rows) - self.scroll]):
            y -= line_h
            if y < self.rect.y + 10:
                break  ## box is full
            if name:
                screen.blit(self.font.render(name, True, (222, 222, 214)),
                            (self.rect.x + 15, y))
            screen.blit(self.font.render(line, True, (150, 150, 142)),
                        (self.rect.x + 15 + indent, y))
            # Scroll bar: thin line on the left, only when there is something to scroll
            max_scroll = len(rows) - visible
            if max_scroll > 0:
                track_h = self.rect.height - 54
                thumb_h = max(20, track_h * visible // len(rows))
                thumb_y = self.rect.y + 10 + (track_h - thumb_h) * (max_scroll - self.scroll) // max_scroll
                self.scrollRect = pygame.rect.Rect(self.rect.x + 3, thumb_y, 4, thumb_h)
                pygame.draw.rect(screen, (90, 88, 96),self.scrollRect)




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
        self.labelSurf = uF.render_wrapped(self.font, self.label, (255, 255, 255), shape.width - 20)
        self.labelRect = self.labelSurf.get_rect(center=shape.center)

        self.outlineColor = (128, 128, 128)
        self.hovering = False

    def handle_event(self, event):
        mouseX, mouseY = pygame.mouse.get_pos()
        localX = mouseX - self.imageX
        localY = mouseY - self.imageY
        maskW, maskH = self.imageMask.get_size()

        self.hovering = (0 <= localX < maskW and 0 <= localY < maskH
                         and self.imageMask.get_at((localX, localY)))

        if self.hovering and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.action()

    def draw(self, screen):
        screen.blit(self.image, (self.imageX, self.imageY))
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
