#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
import requests
from song import *
import random
import ConfigParser

class DoubanFMApi:
    API_HOST_URL = "https://api.douban.com"
    TOKEN_HOST_URL = "https://www.douban.com"
    APP_NAME = "radio_android"
    VERSION = "642"
    KEY = "02f7751a55066bcb08e65f4eff134361"
    SECRET = "63cf04ebd7b0ff3b"
    UUID = '408428bc' + str(uuid.uuid4()).replace('-', '')
    REDIRECT_URI = 'http://douban.fm'

    def __init__(self):
        self.auth = None
        config = ConfigParser.ConfigParser()
        config.read('fm.cfg')       
        user = dict(config.items('douban'))
        email= user['email']
        password = user['password']
        self.cookie=user['cookie']
        self.login(email,password)
    def login(self,email,password):
        rsp = requests.post('%s/service/auth2/token' % DoubanFMApi.TOKEN_HOST_URL, data={
            'username': email,
            'password': password,
            'udid': DoubanFMApi.UUID,
            'client_id': DoubanFMApi.KEY,
            'client_secret': DoubanFMApi.SECRET,
            'redirect_uri': DoubanFMApi.REDIRECT_URI,
            'grant_type': 'password',
            'apikey': DoubanFMApi.KEY,
        }).json()
        try:
            self.auth = "Bearer %s" % rsp['access_token']
        except:
            print '[-]认证失败'
    def get_redheart_songs(self):
        if self.auth is None:
            return []

        auth_header = {'Authorization': self.auth}

        rsp = requests.get('%s/v2/fm/redheart/basic' % DoubanFMApi.API_HOST_URL, params={
            'app_name': DoubanFMApi.APP_NAME,
            'version': DoubanFMApi.VERSION,
        }, headers=auth_header).json()

        sids = ""
        for sid in rsp['songs']:
            if sid['playable'] is True:
                sids += sid['sid'] + '|'

        sids = sids[:-1]

        rsp = requests.post('%s/v2/fm/songs' % DoubanFMApi.API_HOST_URL, data={
            'sids': sids,
            'kbps': '128',
            'app_name': DoubanFMApi.APP_NAME,
            'version': DoubanFMApi.VERSION,
            'apikey': DoubanFMApi.KEY,
        }, headers=auth_header).json()
        
        return rsp[random.randint(0, len(rsp) - 1)]
        
    def get_MHz_songs(self,channel):
        if channel==-3:
            return Song(self.get_redheart_songs())
        auth_header = {'Cookie':self.cookie}
        rsp = requests.get('https://douban.fm/j/v2/playlist', params={
            'channel': str(channel),
            'kbps':'128',
            'client':'s:mainsite|y:3.0',
            'app_name':'radio_website',
            'version':'100',
            'type':'n'
        }, headers=auth_header).json()
        return Song(rsp['song'][0])
        
    def red_song(self,channel,ssid,like):
        param={
            'channel': str(channel),
            'kbps':'128',
            'client':'s:mainsite|y:3.0',
            'app_name':'radio_website',
            'version':'100',
            'sid':str(ssid),
            'pt':'',
            'pb':'128',
            'apikey':''
        }
        param['type']=( 'u' if like else 'r')
        auth_header = {'Cookie':self.cookie}
        rsp = requests.get('https://douban.fm/j/v2/playlist', params=param, headers=auth_header).json()
        return True

    def get_MHz_List(self):
        channel_list = [
            {'name': u'红心兆赫', 'channel': -3},
            {'name': u'我的私人兆赫', 'channel': 0},
            {'name': u'每日私人歌单', 'channel': -2},
            {'name': u'豆瓣精选兆赫', 'channel': -10},
            # 心情 / 场景
            {'name': u'工作学习', 'channel': 153},
            {'name': u'户外', 'channel': 151},
            {'name': u'休息', 'channel': 152},
            {'name': u'亢奋', 'channel': 154},
            {'name': u'舒缓', 'channel': 155},
            {'name': u'Easy', 'channel': 77},
            {'name': u'咖啡', 'channel': 32},
            # 语言 / 年代
            {'name': u'华语', 'channel': 1},
            {'name': u'欧美', 'channel': 2},
            {'name': u'七零', 'channel': 3},
            {'name': u'八零', 'channel': 4},
            {'name': u'九零', 'channel': 5},
            {'name': u'粤语', 'channel': 6},
            {'name': u'日语', 'channel': 17},
            {'name': u'韩语', 'channel': 18},
            {'name': u'法语', 'channel': 22},
            {'name': u'新歌', 'channel': 61},
            # 风格 / 流派
            {'name': u'流行', 'channel': 194},
            {'name': u'摇滚', 'channel': 7},
            {'name': u'民谣', 'channel': 8},
            {'name': u'轻音乐', 'channel': 9},
            {'name': u'电影原声', 'channel': 10},
            {'name': u'爵士', 'channel': 13},
            {'name': u'电子', 'channel': 14},
            {'name': u'说唱', 'channel': 15},
            {'name': u'R&B', 'channel': 16},
            {'name': u'古典', 'channel': 27},
            {'name': u'动漫', 'channel': 28},
            {'name': u'世界音乐', 'channel': 187},
            {'name': u'布鲁斯', 'channel': 188},
            {'name': u'拉丁', 'channel': 189},
            {'name': u'雷鬼', 'channel': 190},
            {'name': u'小清新', 'channel': 76}
        ]
        return channel_list
