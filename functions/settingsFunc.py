import pygame.mixer_music

class Settings:
    def __init__(self):
        self.musicVolume = 1.0
        self.sfxVolume = 1.0
        self.roomVolume = 1
        self.language = "en"   # "en" or "nl", decides which text column of the database is used

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

    def getLanguage(self):
        return self.language

    def setLanguage(self, language):
        self.language = language

settings = Settings()
