import pygame

ui_mode = "game"
volume = 1.0
auto_text = True

#assets

#integers

#floats

#strings

#bool


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

BUTTON_COLOR = (70, 70, 70)
BUTTON_HOVER_COLOR = (100, 100, 100)
BACKGROUND_COLOR = (30, 30, 30)

settings_button = pygame.Rect(SCREEN_WIDTH - 180, 25, 150, 50)
inventory_button = pygame.Rect(SCREEN_WIDTH - 180, SCREEN_HEIGHT - 75, 150, 50)

save_button = pygame.Rect(40, 120, 180, 50)
load_button = pygame.Rect(240, 120, 180, 50)
auto_text_button = pygame.Rect(40, 220, 350, 50)
volume_down_button = pygame.Rect(40, 320, 60, 50)
volume_up_button = pygame.Rect(330, 320, 60, 50)
back_button = pygame.Rect(40, SCREEN_HEIGHT - 75, 150, 50)


def draw_button(screen, font, rect, text):
    color = BUTTON_HOVER_COLOR if rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, "white", rect, 2)
    surface = font.render(text, True, "white")
    screen.blit(surface, surface.get_rect(center=rect.center))


def draw_base_ui(screen, font):
    draw_button(screen, font, settings_button, "Settings")
    draw_button(screen, font, inventory_button, "Inventory")


def handle_base_ui(mouse_event):
    if not mouse_event or mouse_event.type != pygame.MOUSEBUTTONUP or mouse_event.button != 1:
        return None

    if settings_button.collidepoint(mouse_event.pos):
        return "settings"

    if inventory_button.collidepoint(mouse_event.pos):
        return "inventory"

    return None


def draw_settings(screen, font):
    screen.fill(BACKGROUND_COLOR)

    title = font.render("Settings", True, "white")
    screen.blit(title, (40, 40))

    draw_button(screen, font, save_button, "Save Game")
    draw_button(screen, font, load_button, "Load Game")

    auto_text_label = "Auto Text: ON" if auto_text else "Auto Text: OFF"
    draw_button(screen, font, auto_text_button, auto_text_label)

    draw_button(screen, font, volume_down_button, "-")
    draw_button(screen, font, volume_up_button, "+")

    volume_text = font.render(f"Volume: {int(volume * 100)}%", True, "white")
    screen.blit(volume_text, (130, 332))

    draw_button(screen, font, back_button, "Back")


def handle_settings(mouse_event):
    global ui_mode, volume, auto_text

    if not mouse_event or mouse_event.type != pygame.MOUSEBUTTONUP or mouse_event.button != 1:
        return None

    if save_button.collidepoint(mouse_event.pos):
        return "save"

    if load_button.collidepoint(mouse_event.pos):
        return "load"

    if auto_text_button.collidepoint(mouse_event.pos):
        auto_text = not auto_text
        return "setting_changed"

    if volume_down_button.collidepoint(mouse_event.pos):
        volume = max(0.0, volume - 0.1)
        return "volume_changed"

    if volume_up_button.collidepoint(mouse_event.pos):
        volume = min(1.0, volume + 0.1)
        return "volume_changed"

    if back_button.collidepoint(mouse_event.pos):
        ui_mode = "game"
        return "back"

    return None


def draw_inventory(screen, font, inventory):
    screen.fill(BACKGROUND_COLOR)

    title = font.render("Inventory", True, "white")
    screen.blit(title, (40, 40))

    if not inventory:
        text = font.render("Inventory is empty.", True, "white")
        screen.blit(text, (40, 120))
    else:
        for i, item in enumerate(inventory):
            text = font.render(str(item), True, "white")
            screen.blit(text, (40, 120 + i * 40))

    draw_button(screen, font, back_button, "Back")


def handle_inventory(mouse_event):
    global ui_mode

    if not mouse_event or mouse_event.type != pygame.MOUSEBUTTONUP or mouse_event.button != 1:
        return

    if back_button.collidepoint(mouse_event.pos):
        ui_mode = "game"