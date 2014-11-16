import pygame as PG
import pygame.midi
import random

import Label


# All music found in http://musicmoz.org/Sound_Files/MIDI/Originals/
class Radio(PG.sprite.Sprite):
    song_locations = None
    song_names = None
    max_index = 0
    current_index = None
    label = None
    text_rect = None
    volume = None
    is_on = False

    def __init__(self):
        PG.init()
        PG.midi.init()
        PG.sprite.Sprite.__init__(self)
        #Initialize the array of songs
        if Radio.song_locations is None:
            Radio.song_locations = []
            Radio.song_locations.append("audio/music/funkytown.mid")
            Radio.song_locations.append("audio/music/fridayiminlove.mid")
            Radio.song_locations.append("audio/music/thriller.mid")
            Radio.song_locations.append("audio/music/blue.mid")
            Radio.song_locations.append("audio/music/sweetdreams.mid")
            Radio.song_locations.append("audio/music/rebelyell.mid")
            Radio.song_locations.append("audio/music/taintedlove.mid")
            Radio.song_locations.append("audio/music/andthebeatgoeson.mid")
            Radio.song_locations.append("audio/music/somebodyswatchingme.mid")
            Radio.song_locations.append("audio/music/discoinferno.mid")
            Radio.song_locations.append(
                "audio/music/lastnightthedjsavedmylife.mid")
            Radio.song_locations.append("audio/music/september.mid")
            Radio.song_locations.append("audio/music/"
                                        "girlsjustwannahavefun.mid")
            Radio.song_locations.append("audio/music/wakemeupwham.mid")
            Radio.song_locations.append("audio/music/bleedinglove.mid")
            Radio.song_locations.append("audio/music/hungrylikeawolf.mid")
            Radio.song_locations.append("audio/music/lullaby.mid")
            Radio.song_locations.append("audio/music/iransofaraway.mid")
            Radio.song_locations.append("audio/music/justcantgetenough.mid")
            Radio.song_locations.append("audio/music/takeonme.mid")
            Radio.max_index = len(Radio.song_locations) - 1
        if Radio.song_names is None:
            Radio.song_names = []
            Radio.song_names.append("Funkytown")
            Radio.song_names.append("Friday I'm In Love")
            Radio.song_names.append("Thriller")
            Radio.song_names.append("Blue")
            Radio.song_names.append("Sweet Dreams Are Made Of This")
            Radio.song_names.append("Rebel Yell")
            Radio.song_names.append("Tainted Love")
            Radio.song_names.append("And The Beat Goes On")
            Radio.song_names.append("Somebody's Watching Me")
            Radio.song_names.append("Disco Inferno")
            Radio.song_names.append("Last Night The DJ Saved My Life")
            Radio.song_names.append("September")
            Radio.song_names.append("Girls Just Wanna Have Fun")
            Radio.song_names.append("Wake Me Up")
            Radio.song_names.append("Bleeding Love")
            Radio.song_names.append("Hungry Like A Wolf")
            Radio.song_names.append("Lullaby")
            Radio.song_names.append("I Ran So Far Away")
            Radio.song_names.append("Just Can't Get Enough")
            Radio.song_names.append("Take On Me")

        if Radio.current_index is None:
            Radio.current_index = random.randrange(0, Radio.max_index)

        if Radio.volume is None:
            Radio.volume = 1

        Radio.label = Label.Label("nowplaying", "", (0, 0))
        Radio.text_rect = pygame.Rect(268, 65, 170, 31)
        Radio.increment_current_index_and_play()
        PG.mixer.music.set_volume(Radio.volume)
        Radio.is_on = True
        self.labels = pygame.sprite.Group()
        self.labels.add(Radio.label)
        self.display_volume_timer = 0

    @staticmethod
    def play_random_song():
        Radio.current_index = random.randrange(0, Radio.max_index)
        Radio.label.update(Radio.song_names[Radio.current_index])
        if (Radio.label.image.get_rect().width > Radio.text_rect.width):
            Radio.trim_text_to_fit_and_update_label()
        PG.mixer.music.load(Radio.song_locations[Radio.current_index])
        PG.mixer.music.play()

    @staticmethod
    def toggle_radio():
        if Radio.is_on:
            PG.mixer.music.pause()
            Radio.label.update("")
            Radio.is_on = False
        else:
            Radio.is_on = True
            Radio.label.update(Radio.song_names[Radio.current_index])
            PG.mixer.music.unpause()


    @staticmethod
    def increment_current_index_and_play():
        if Radio.current_index < Radio.max_index:
            Radio.current_index += 1
        else:
            Radio.current_index = 0
        Radio.label.update(Radio.song_names[Radio.current_index])
        if (Radio.label.image.get_rect().width > Radio.text_rect.width):
            Radio.trim_text_to_fit_and_update_label()
        PG.mixer.music.load(Radio.song_locations[Radio.current_index])
        PG.mixer.music.play()

    @staticmethod
    def decrement_current_index_and_play():
        if Radio.current_index > 0:
            Radio.current_index -= 1
        else:
            Radio.current_index = Radio.max_index
        Radio.label.update(Radio.song_names[Radio.current_index])
        if (Radio.label.image.get_rect().width > Radio.text_rect.width):
            Radio.trim_text_to_fit_and_update_label()
        PG.mixer.music.load(Radio.song_locations[Radio.current_index])
        PG.mixer.music.play()

    @staticmethod
    def trim_text_to_fit_and_update_label():
        i = 0
        while Radio.label.image.get_rect().width > Radio.text_rect.width:
            i += 1
            text = Radio.song_names[Radio.current_index][:-i]
            Radio.label.update(text)
        text = text[:-2]
        text += "..."
        if i > 0:
            Radio.label.update(text)
            Radio.song_names[Radio.current_index] = text

    def update(self):
        if Radio.is_on:
            self.display_volume_timer += 1
            if not PG.mixer.music.get_busy():
                Radio.increment_current_index_and_play()
            keys_pressed = PG.key.get_pressed()
            if keys_pressed[PG.K_UP]:
                self.display_volume_timer = 0
                Radio.volume = min(1, Radio.volume + .01)
                PG.mixer.music.set_volume(Radio.volume)
                Radio.label.update("Volume: " + str(int(Radio.volume * 100)))
            elif keys_pressed[PG.K_DOWN]:
                self.display_volume_timer = 0
                Radio.volume = max(0, Radio.volume - .01)
                PG.mixer.music.set_volume(Radio.volume)
                Radio.label.update("Volume: " + str(int(Radio.volume * 100)))
            if self.display_volume_timer >= 100:
                Radio.label.update(Radio.song_names[Radio.current_index])
                self.display_volume_timer = 0

'''
   def __del__(self):
        if PG.mixer is not None:
            PG.mixer.music.stop()
            print "deleted"

    def __get__(self, instance, owner):
        if owner is None:
            print "No owner"
'''
