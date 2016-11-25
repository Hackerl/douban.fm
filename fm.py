#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urwid
import random
import Queue
from api import *
from song import *
from player import *
from view import *

class UI:
    LOOP_MODE = {
        0: u'随机播放',
        1: u'单曲循环',

    }

    def __init__(self):
        self.player = Player()  #播放器
        self.btns = []
        self.playing_btn = None
        self.loop_mode = 0
        self.next_song_alarm = None
        self.main = None
        self.api=DoubanFMApi()
        self.playing_song=None
        self.history=Queue.LifoQueue(10)
        # 调色板
        self.palette = [
            ('reversed', '', '', '', 'standout', ''),
            ('playing', '', '', '', 'bold, g7', '#d06'),
            ('title', '', '', '', 'bold, g7', '#d06'),
            ('loop_mode', '', '', '', 'bold, g7', '#d06'),
            ('red', '', '', '', 'bold, #d06', ''),
        ]

        self._setup_ui()   #启动UI  ------------------------>
                                                 #          |
    def _setup_ui(self):                         #          |
        MHzList = self.api.get_MHz_List()    #获取api的歌曲列表

        # 头部
        self.title = urwid.Text('')   #调用urwid 赋值给self.title
        self._update_title()
        divider = urwid.Divider()
        header = urwid.Padding(urwid.Pile([divider, self.title, divider]), left=4, right=4)   #头设置

        # 频道列表
        for MHz in MHzList:
            self.btns.append(MHzButton(MHz, self._on_item_pressed))
        self.MHzListBox = MHzListBox(self.btns)

        # 页面
        self.main = urwid.Padding(
            urwid.Frame(self.MHzListBox, header=header, footer=divider),
            left=4, right=4)

        # 注册信号回调
        urwid.register_signal(
            MHzListBox, ['exit', 'stop','prev_song', 'next_song', 'change_mode'])
        urwid.connect_signal(self.MHzListBox, 'exit', self._on_exit)
        urwid.connect_signal(self.MHzListBox, 'stop', self.stop_song)
        urwid.connect_signal(self.MHzListBox, 'prev_song', self.prev_song)
        urwid.connect_signal(self.MHzListBox, 'next_song', self.next_song)
        urwid.connect_signal(self.MHzListBox, 'change_mode', self.change_mode)

        self.loop = urwid.MainLoop(self.main, palette=self.palette)
        self.loop.screen.set_terminal_properties(colors=256)

    def _update_title(self):
        text = [
            ('title', u' ❤ 豆瓣 FM 红心歌曲 '),
            ('red', u'   LOOP: '),
            ('loop_mode', u'%s' % UI.LOOP_MODE[self.loop_mode]),
            ('red',u'\nStop [-]'),
        ]

        if self.playing_btn is not None:
            playing_song = self.playing_song
            text[3]=('red', u'\n♫ %s - %s' % (playing_song.title, playing_song.artist)) #正在播放歌曲

        self.title.set_text(text)  #为text设置内容

    def stop_song(self):
        if self.playing_btn is not None:
            self.playing_btn.set_is_playing(False)
        self.playing_btn = None
        self.player.stop()
        self._update_title()

        if self.next_song_alarm is not None:
            self.loop.remove_alarm(self.next_song_alarm)
            
    def prev_song(self):
        if self.history.qsize() > 0:
            self.playing_song=self.history.get()
            self.player.play(self.playing_song)
            self._update_title()
            self.alarm()
        else:
            self.next_song()


    def next_song(self):
        if not self.playing_btn:
            pass
        else:
            # 随机播放
            self.history.put(self.playing_song)
            if not self.loop_mode:
                self._on_item_pressed(self.playing_btn)
            # 单曲循环
            else:
                self.player.play(self.playing_song)
                self.alarm()

    def change_mode(self):
        self.loop_mode = not self.loop_mode

        self._update_title()

    def _on_item_pressed(self, button):
        if self.playing_btn is not None:
            self.playing_btn.set_is_playing(False)
        self.playing_btn = button
        self.playing_btn.set_is_playing(True)

        self.playing_song = self.api.get_MHz_songs(self.playing_btn.MHz['channel'])
        self.player.play(self.playing_song)
        self._update_title()
        self.alarm()
    def alarm(self):
        # 循环播放定时设置
        if self.next_song_alarm is not None:
            self.loop.remove_alarm(self.next_song_alarm)

        self.next_song_alarm = self.loop.set_alarm_in(
            self.playing_song.length_in_sec,
            lambda loop, data: self.next_song(), None)

    def _on_exit(self):
        self.player.stop()
        raise urwid.ExitMainLoop()

    def run(self):
        self.loop.run()


if __name__ == '__main__':
    UI().run()
