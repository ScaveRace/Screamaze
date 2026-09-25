import pygame

class Sound:
    def __init__(self, player,volume=1):
        self.volume = volume
        self.player = player

    def play_music(self, music, volume=1):
        self.volume = volume
        pygame.mixer.music.load(music)
        pygame.mixer.music.set_volume(self.volume*self.player.getVolume())
        pygame.mixer.music.play(loops=-1)

    def play_sound(self, sound):
        sound_effect = pygame.mixer.Sound(sound)
        sound_effect.set_volume(self.volume*self.player.volume)
        sound_effect.play()

    def setVolume(self, playervolume):
        pygame.mixer_music.set_volume(playervolume*self.volume)
        self.player.volume = playervolume

