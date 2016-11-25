#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urwid

class MHzButton(urwid.Button):
    def __init__(self, MHz, on_pressed_callback):
        super(MHzButton, self).__init__('', on_pressed_callback)
        self.MHz = MHz
        self.is_playing = False

        self._text = urwid.SelectableIcon(
            u'• %s' % MHz['name'],
            cursor_position=0)
        self._w = urwid.AttrMap(self._text, None, focus_map='red')
        self.set_is_playing(self.is_playing)

    # 设置按钮播放状态
    def set_is_playing(self, is_playing):
        self.is_playing = is_playing

        if is_playing:
            self._text.set_text(u'♫' + self._text.text[1:])
            self._w.set_attr_map({None: 'red'})
        else:
            self._text.set_text(u'•' + self._text.text[1:])
            self._w.set_attr_map({'playing': None})

    def mouse_event(self, size, event, button, x, y, focus):
        # 屏蔽鼠标点击
        pass


class MHzListBox(urwid.ListBox):
    def __init__(self, btns):
        super(MHzListBox, self).__init__(urwid.SimpleFocusListWalker(btns))

        self._command_map['j'] = 'cursor down'
        self._command_map['k'] = 'cursor up'

    def keypress(self, size, key):
        if key in ('up', 'down', 'page up', 'page down', 'enter', ' ', 'j', 'k'):
            return super(MHzListBox, self).keypress(size, key)

        if key in ('q', 'Q', 'esc'):
            # 发送退出信号
            urwid.emit_signal(self, 'exit')

        if key in ('s', 'S'):
            # 停止播放
            urwid.emit_signal(self, 'stop')

        if key == 'left':
            # 下一首歌曲
            urwid.emit_signal(self, 'prev_song')
        if key == 'right':
            urwid.emit_signal(self, 'next_song')            
        if key in ('m', 'M'):
            # 切换模式
            urwid.emit_signal(self, 'change_mode')
