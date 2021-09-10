import Model
from pygame import mixer
from tkinter import filedialog
import os
from io import BytesIO
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from PIL import Image


class Player:

    def __init__(self):
        mixer.init()
        self.my_model = Model.Model()

    def get_db_status(self):
        return self.my_model.get_db_status()

    def close_player(self):
        mixer.music.stop()
        self.my_model.close_connection()

    def set_volume(self, volume_level):
        mixer.music.set_volume(volume_level)

    def add_songs(self):
        selected_files = filedialog.askopenfilenames(title="Select Your song...", filetype=[("mp3 files", "*.mp3")])
        songs=()
        if selected_files:
            for file in selected_files:
                file_name = os.path.basename(file)
                self.my_model.add_song(file_name, file)
                songs+=(file_name,)
            return songs
        else:
            return

    # def add_song(self):
    #     song_path = filedialog.askopenfilename(title="Select Your song...", filetype=[("mp3 files", "*.mp3")])
    #     if song_path == "":
    #         return
    #     song_name = os.path.basename(song_path)
    #     self.my_model.add_song(song_name, song_path)
    #     return song_name

    def remove_song(self, song_name):
        self.my_model.remove_song(song_name)

    def get_song_length(self, song_name):
        self.song_path = self.my_model.get_song_path(song_name)
        self.mtag = MP3(self.song_path)
        return self.mtag.info.length

    def get_song_count(self):
        return self.my_model.get_song_count()

    def move_seek(self, seek_value):
        start_sec = float(seek_value) / 1000
        # print("finalllllll=======", start_sec)
        mixer.music.play(start=start_sec)

    def music_pos(self):
        return mixer.music.get_pos()

    def play_song(self):
        mixer.quit()
        mixer.init(frequency=self.mtag.info.sample_rate)
        mixer.music.load(self.song_path)
        mixer.music.play(start=00.00)

    def stop_song(self):
        mixer.music.stop()

    def pause_song(self):
        mixer.music.pause()

    def unpause_song(self):
        mixer.music.unpause()

    def add_song_to_favourites(self, song_name):
        return self.my_model.add_song_to_favorites(song_name, self.my_model.get_song_path(song_name))

    def load_songs_from_favourites(self):
        result = self.my_model.load_songs_from_favourites()
        return result, self.my_model.song_dict

    def remove_song_from_favourites(self, song_name):
        result = self.my_model.remove_song_from_favourites(song_name)
        return result

#
# p1 = Player()
