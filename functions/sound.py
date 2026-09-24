import pygame

vol = 1
def play_music(music, volume):
    pygame.mixer.music.load(music)
    pygame.mixer.music.set_volume(volume *vol)
    pygame.mixer.music.play(loops=-1)


def play_sound(sound, volume):
    sound_effect = pygame.mixer.Sound(sound)
    sound_effect.set_volume(volume*vol)
    sound_effect.play()


def setVolume(v):
    global vol
    vol = v