class BasePage:
    # every page of the phone extends this, like the rooms extend BaseRoom
    # the Phone makes it with (screen, player, phone) and shows it when somebody calls phone.goTo("<its name>")
    def __init__(self, screen, player, phone):
        self.screen = screen
        self.player = player
        self.phone = phone

    def goTo(self, page):
        self.phone.goTo(page)

    def on_enter(self): pass
    def handle_event(self, event): pass
    def draw(self): pass
