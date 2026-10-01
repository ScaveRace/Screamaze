import pygame.mixer_music

class Settings:
    def __init__(self):
        self.musicVolume = 1.0
        self.sfxVolume = 1.0
        self.roomVolume = 1

    def getMusicVolume(self):
        return self.musicVolume

    def getSFXVolume(self):
        return self.sfxVolume

    def setSFXVolume(self, volume):
        self.sfxVolume = volume

    def setMusicVolume(self,volume):
        pygame.mixer_music.set_volume(volume * self.roomVolume)
        self.musicVolume = volume

    def setRoomVolume(self, roomvolume):
        self.roomVolume = roomvolume

settings = Settings()
