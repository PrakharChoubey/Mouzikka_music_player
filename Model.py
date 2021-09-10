from cx_Oracle import *
from traceback import *


class Model:
    def __init__(self):
        self.song_dict = {}
        self.db_status = True
        self.conn = None
        self.cur = None
        try:
            self.conn = connect("Mouzikka/mpass@localhost/xe")
            print("Connected to db")
            self.cur = self.conn.cursor()
        except DatabaseError:
            self.db_status = False
            print("Db Error:", format_exc())

    def get_db_status(self):
        return self.db_status

    def get_song_count(self):
        return len(self.song_dict)

    def close_connection(self):
        if self.cur is not None:
            self.cur.close()
            print("Cursor Closed")
        if self.conn is not None:
            self.conn.close()
            print("Connection closed")

    def add_song(self, song_name, song_path):
        self.song_dict[song_name] = song_path
        print("Song added", self.song_dict[song_name])

    def get_song_path(self, song_name):
        return self.song_dict[song_name]

    def remove_song(self, song_name):
        self.song_dict.pop(song_name)
        print("After deletion", self.song_dict)

    def search_song_in_favorites(self, song_name):
        self.cur.execute("select song_name from myfav where song_name=:1", (song_name,))
        song_tupple = self.cur.fetchone()
        if song_tupple is None:
            return False
        return True

    def add_song_to_favorites(self, song_name, song_path):
        is_song_present = self.search_song_in_favorites(song_name)
        if is_song_present:
            return "Song already present in favorites"
        self.cur.execute("select max(song_id) from myfav")
        last_song_id = self.cur.fetchone()[0]
        next_song_id = 1
        if last_song_id is not None:
            next_song_id = last_song_id + 1
        self.cur.execute("insert into myfav values(:1,:2,:3)", (next_song_id, song_name, song_path))
        self.conn.commit()
        return "Song successfully added to your Favorites"

    def load_songs_from_favourites(self):
        self.cur.execute("select song_name,song_path from myfav")
        song_present = False
        for song_name, song_path in self.cur:
            self.song_dict[song_name] = song_path
            song_present = True
        if song_present:
            return "List populated from favorites"
        else:
            return "No songs present"

    def remove_song_from_favourites(self, song_name):
        self.cur.execute("delete from myfav where song_name=:1", (song_name,))
        count = self.cur.rowcount
        if count == 0:
            return "This song is not present in your favorites"
        else:
            self.conn.commit()
            # self.remove_song(song_name)
            return "Deleted"
        # self.cur.execute("select song_id from myfav where song_name=:1", (song_name,))
        # song_id = self.cur.fetchone()
        # if song_id:
        #     self.cur.execute("delete from myfav where song_id=:1", song_id)
        #     self.conn.commit()
        #     self.remove_song(song_name)
        #     return "Song successfully removed from your Favorites"
        # else:
        #     return "This song is not present in your favorites"
