import pygame
import UI.uiElements as u
import functions.language as lang
import functions.uiFunc as uF
from Phone.chatLog import Message
from Phone.pages.basePage import BasePage
from Phone.pages.homescreen import PHONE_SIZE

A = "assets/phoneIm/"

# where things are on the phone of 300 x 720, the pause menu covers the top 60
TITLE = pygame.Rect(24, 66, 252, 28)
VIEW = pygame.Rect(24, 98, 252, 540)      # the messages
INPUT = pygame.Rect(24, 646, 252, 38)     # the line the player types in

GREYS = ((30, 30, 34), (42, 42, 47))      # the rows switch between these when the speaker changes
FONTS = "segoeui,helveticaneue,arial,dejavusans,liberationsans,notosans,freesans"   # clean sans-serif, the first one on this computer


class ChatPage(BasePage):

    def __init__(self, screen, player, phone):
        super().__init__(screen, player, phone)
        self.image = u.load_alpha_image(A + "phone_bg.png", PHONE_SIZE)
        self.font = pygame.font.SysFont(FONTS, 15)
        self.nameFont = pygame.font.SysFont(FONTS, 13, bold=True)
        self.titleFont = pygame.font.SysFont(FONTS, 17, bold=True)
        self.input = ""
        self.focus = False
        self.scroll = 0         ### pixels up from the newest message, gets clamped in draw
        self.count = 0          ### how many messages there were last frame, to jump to a new one

    def on_enter(self):
        self.focus = False
        self.phone.log.unread = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.focus = uF.focused(event, INPUT)
        if event.type == pygame.MOUSEWHEEL and VIEW.collidepoint(pygame.mouse.get_pos()):
            self.scroll += event.y * 36

        if not self.focus:
            return
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            text = self.input.strip()
            self.input = ""
            if text:
                self.phone.log.add(Message("You", text=text))
        else:
            self.input = uF.handle_text_event(self.input, event)[:200]

    ###  cuts every message in lines, the grey changes every time the speaker changes
    ###  the messages are looked up again every frame, that is why they follow the language
    def getRows(self):
        rows = []
        grey = 0
        speaker = None
        for message in self.phone.log.messages:
            first = message.who != speaker      ## the first message of this speaker, only that one has the name
            if first and speaker is not None:
                grey = 1 - grey
            speaker = message.who

            textY = 7 if first else 2
            if first and message.who:
                textY += self.nameFont.get_linesize()
            lines = uF.wrap_lines(self.font, message.body(), VIEW.width - 26)
            height = textY + len(lines) * self.font.get_linesize() + 7
            rows.append({"who": message.who if first else "", "lines": lines, "grey": grey, "textY": textY, "height": height})
        return rows

    def draw(self):
        self.phone.log.unread = False       ## the chat is open, so nothing is new
        self.screen.blit(self.image, (0, 0))
        title = self.titleFont.render(lang.ui("Chat"), True, (206, 206, 200))
        self.screen.blit(title, title.get_rect(center=TITLE.center))
        pygame.draw.rect(self.screen, (22, 22, 25), VIEW, border_radius=6)

        rows = self.getRows()
        total = sum(row["height"] for row in rows)
        if len(rows) != self.count:
            self.scroll = 0                 ## a new message, show it
            self.count = len(rows)
        self.scroll = max(0, min(self.scroll, total - VIEW.height))

        # the newest message sits at the bottom, everything outside of VIEW is cut off
        y = VIEW.bottom - self.scroll - total
        self.screen.set_clip(VIEW)
        for row in rows:
            if VIEW.top - row["height"] < y < VIEW.bottom:
                pygame.draw.rect(self.screen, GREYS[row["grey"]], (VIEW.x, y, VIEW.width, row["height"]))
                if row["who"]:
                    colour = (140, 190, 255) if row["who"] == "You" else (232, 190, 120)
                    self.screen.blit(self.nameFont.render(row["who"], True, colour), (VIEW.x + 10, y + 7))
                lineY = y + row["textY"]
                for line in row["lines"]:
                    self.screen.blit(self.font.render(line, True, (206, 206, 200)), (VIEW.x + 10, lineY))
                    lineY += self.font.get_linesize()
            y += row["height"]
        self.screen.set_clip(None)

        # scroll bar, only when there is something to scroll
        if total > VIEW.height:
            thumb = max(20, VIEW.height * VIEW.height // total)
            thumbY = VIEW.y + (VIEW.height - thumb) * (total - VIEW.height - self.scroll) // (total - VIEW.height)
            pygame.draw.rect(self.screen, (90, 88, 96), (VIEW.right - 5, thumbY, 3, thumb), border_radius=2)

        self.drawInput()

    def drawInput(self):
        pygame.draw.rect(self.screen, GREYS[1], INPUT, border_radius=10)
        pygame.draw.rect(self.screen, (110, 110, 120) if self.focus else (60, 58, 64), INPUT, 1, border_radius=10)

        shown = self.input
        colour = (206, 206, 200)
        if not shown and not self.focus:
            shown, colour = lang.ui("Type a message"), (120, 120, 128)
        else:
            ###  the line is only so wide, so when the text is too long to fit we cut letters off the front
            ###  until the rest fits, so you always see the end of what you type, where the cursor is
            ###  the whole text is still kept in self.input and sent when you press enter
            while shown and self.font.size(shown + "|")[0] > INPUT.width - 20:
                shown = shown[1:]
            if self.focus and (pygame.time.get_ticks() // 500) % 2 == 0:
                shown += "|"
        text = self.font.render(shown, True, colour)
        self.screen.blit(text, text.get_rect(midleft=(INPUT.x + 10, INPUT.centery)))
