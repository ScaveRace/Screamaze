import UI.uiElements as u


def settingsMenu():
    def volume():
        print("volume button pressed")

    def auto_text():
        print("auto-text button pressed")
    buttons =[
    u.Button(120, 570, 150, 50, "Volume", volume),
    u.Button(120, 620, 150, 50, "Auto-Text", auto_text)
]

