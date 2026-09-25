volume = 1



def getVolume():
    return volume

def setSFXVolume(self, volume):
    pygame.mixer_music.set_volume(volume*self.volume)
    s.seteffectVolume(volume)
