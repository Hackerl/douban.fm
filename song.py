#!/usr/bin/python
# encoding: utf-8

class Song(object):
    def __init__(self, song_json):
        try:
            self._parse(song_json)
        except KeyError:
            self.like=1
            
    def _parse(self, song_json):
        self.sid = song_json['sid']
        self.picture = song_json['picture']
        self.artist = song_json['artist']
        self.title = song_json['title']
        if self.title.isupper():
            self.title = self.title.title()

        self.length_in_sec = song_json['length']
        self.url = song_json['url']
        self.like = song_json['like']
    @staticmethod
    def parse(song_json):
        return Song(song_json)

            
