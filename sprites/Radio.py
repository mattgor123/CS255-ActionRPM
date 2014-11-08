import pygame as PG
import pygame.image as PI
import pygame.gfxdraw as PD
import pygame.midi
from states.Constants import Constants


#All music found in http://musicmoz.org/Sound_Files/MIDI/Originals/
class Radio(PG.sprite.Sprite):
    Image = None
    song_locations = None
    song_names = None
    num_songs = 0
    def __init__(self):
        PG.init()
        PG.sprite.Sprite.__init__(self)
        #Initialize the array of songs
        if Radio.song_locations is None:
            Radio.song_locations = []
            Radio.song_locations.append("audio/music/wakemeupavicii.mid")
            Radio.song_locations.append("audio/music/funkytown.mid")
            Radio.song_locations.append("audio/music/blue.mid")
            Radio.song_locations.append("audio/music/rebelyell.mid")
            Radio.song_locations.append("audio/music/thriller.mid")
            Radio.song_locations.append("audio/music/andthebeatgoeson.mid")
            Radio.song_locations.append("audio/music/discoinferno.mid")
            Radio.song_locations.append("audio/music/september.mid")
            Radio.song_locations.append("audio/music/girlsjustwannahavefun.mid")
            Radio.song_locations.append("audio/music/lastnightthedjsavedmylife.mid")
            Radio.song_locations.append("audio/music/wakemeupwham.mid")
            Radio.song_locations.append("audio/music/onceinalifetime.mid")
            Radio.song_locations.append("audio/music/hungrylikeawolf.mid")
            Radio.song_locations.append("audio/music/sandstorm.mid")
            Radio.song_locations.append("audio/music/takeonme.mid")
            Radio.num_songs = len(Radio.song_locations)

        PG.mixer.music.load(Radio.song_locations[0])
        PG.mixer.music.play()




