#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import os

class Player(object):
    def __init__(self):
        self.is_playing = False
        self.current_song = None
        self.player_process = None
        self.external_player = None
        self._detect_external_players()

    def _detect_external_players(self):
        supported_external_players = [
            ["mpv", "--really-quiet"],
            ["mplayer", "-really-quiet"],
            ["mpg123", "-q"],
        ]

        for external_player in supported_external_players:
            proc = subprocess.Popen(
                ["which", external_player[0]],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            player_bin_path = proc.communicate()[0].strip()

            if player_bin_path and os.path.exists(player_bin_path):
                self.external_player = external_player
                break

        else:
            print("No supported player(mpv/mplayer/mpg123) found. Exit.")
            raise SystemExit()

    def play(self, song):
        if self.is_playing:
            self.stop()

        self.current_song = song
        self.player_process = subprocess.Popen(
            self.external_player + [self.current_song.url],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        self.is_playing = True

    def stop(self):
        self.is_playing = False

        if self.player_process is None:
            return
        try:
            self.player_process.terminate()
        except:
            pass


