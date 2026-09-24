import pygame

volume = 1
def play_music(music, volume):
    pygame.mixer.music.load(music)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(loops=-1)


def play_sound(sound, volume):
    sound_effect = pygame.mixer.Sound(sound)
    sound_effect.set_volume(volume)
    sound_effect.play()


def setVolume(v):
    global volume
    volume = v