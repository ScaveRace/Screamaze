import pygame
from player import player

class sound:
    def __init__(self, volume=1):
        self.volume = volume

    def play_music(self, music, volume=1):
        self.volume = volume
        pygame.mixer.music.load(music)
        pygame.mixer.music.set_volume(self.volume*player.volume)
        pygame.mixer.music.play(loops=-1)

    def play_sound(self, sound):
        sound_effect = pygame.mixer.Sound(sound)
        sound_effect.set_volume(self.volume*player.volume)
        sound_effect.play()

    def setVolume(self, playervolume):
        pygame.mixer_music.set_volume(playervolume*self.volume)
        player.volume = playervolume

sound = sound()

