import pygame.mixer_music

musicVolume = 1.0
sfxVolume = 1.

def getMusicVolume():
    return musicVolume

def getSFXVolume():
    return sfxVolume

def setSFXVolume(self, volume):
    pygame.mixer_music.set_volume(volume*self.volume)
    seteffectVolume(volume)
