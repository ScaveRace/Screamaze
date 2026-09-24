import pygame



def wrap_lines(font, text, max_width):
    lines = []
    for paragraph in text.split("\n"):
        line = ""
        for word in paragraph.split():
            test = f"{line} {word}" if line else word
            if font.size(test)[0] <= max_width:
                line = test
                continue
            if line:
                lines.append(line)
            while font.size(word)[0] > max_width:
                cut = len(word)
                while cut > 1 and font.size(word[:cut])[0] > max_width:
                    cut -= 1
                lines.append(word[:cut])
                word = word[cut:]
            line = word
        lines.append(line)
    return lines


def render_wrapped(font, text, color, max_width):
    """Wrapped text as one surface, each line centered."""
    surfaces = [font.render(l, True, color) for l in wrap_lines(font, text, max_width)]
    width = max((s.get_width() for s in surfaces), default=0)
    height = sum(s.get_height() for s in surfaces)
    result = pygame.Surface((width, height), pygame.SRCALPHA)
    y = 0
    for s in surfaces:
        result.blit(s, s.get_rect(centerx=width // 2, y=y))
        y += s.get_height()
    return result


########################## functions for all classes  ###################################

def handle_text_event(text,event):
    if event.type == pygame.TEXTINPUT:  ## adds text that user types
        return text + event.text
    elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:  ## remove text upon backspace, does not repeat every tick
        return text[:-1]
    return text


def focused(event,rect):  ## easy function to check for collision
    if rect.collidepoint(event.pos):
        return True
    return False
