import pygame
from functions.settingsFunc import settings as s

def play_music(music, sett,volume=1):

    pygame.mixer.music.load(music)
    pygame.mixer.music.set_volume(volume*s.musicVolume)
    pygame.mixer.music.play(loops=-1)
    s.setRoomVolume(volume)

def play_sound(sound,sett,volume = 1):
    sound_effect = pygame.mixer.Sound(sound)
    sound_effect.set_volume(volume*s.getSFXVolume())
    sound_effect.play()



