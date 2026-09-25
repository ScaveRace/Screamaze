import pygame
import functions.settingsFunc as s

def play_music(music, volume=1):

    pygame.mixer.music.load(music)
    pygame.mixer.music.set_volume(volume*s.Settings().musicVolume)
    pygame.mixer.music.play(loops=-1)

def play_sound(sound,volume = 1):
    sound_effect = pygame.mixer.Sound(sound)
    sound_effect.set_volume(volume*s.Settings().getSFXVolume())
    sound_effect.play()



