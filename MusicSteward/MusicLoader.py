# -*- coding: utf-8 -*-
import urllib
import re,json,random,time
import ConfigHelper

# By Niuxuan(zuomu) QQ:79069622
fm = 'http://fm.baidu.com'
listurl = "http://fm.baidu.com/dev/api/?tn=playlist&format=json&id="
songurl = "http://music.baidu.com/data/music/fmlink?type=mp3&rate=320&songIds="

#屏蔽频道
disChannels = ConfigHelper.GetDisabled("disChannels")
#屏蔽歌手
disSinger = ConfigHelper.GetDisabled("disSinger")

def GetChannelList():
    #抓取频道列表
    mf = urllib.urlopen(fm)
    html = mf.read()
    html = html.decode('utf8')
    
    start = html.find("{", html.find("rawChannelList")) 
    end = html.find(";", start)
    listjson = html[start:end].strip()
    
    data = json.loads(listjson)
    channel_id_list = []
    for item in data['channel_list']:
        channel_id_list.append(item['channel_id'])
    
    #随机一个频道
    flag = True
    channelId = ""
    while flag:
        channelId = channel_id_list[random.randint(0, len(channel_id_list)-1)]
        if channelId not in disChannels:
            flag = False
    return GetSongList(channelId)

def GetSongList(channelid):
    mf = urllib.urlopen(listurl+channelid)
    html = mf.read()
    html = html.decode('utf8')
    data = json.loads(html)
    song_list = []
    for item in data['list']:
        song_list.append(str(item['id']))

    #随机一首歌曲
    flag = True
    singer = ""
    songInfo = ""
    while flag:
        singer,songInfo = GetSongLink(song_list[random.randint(0, len(song_list)-1)])
        if singer not in disSinger:
            flag = False
            
    return songInfo

def GetSongLink(songid):
    mf = urllib.urlopen(songurl+songid)
    html = mf.read()
    html = html.decode('utf8')
    
    jdata = json.loads(html)
    data = jdata['data']
    songList = data['songList']
    songLink = songList[0]['songLink']

    return (songList[0]['artistName'],songList[0]['songName']+"|"+songList[0]['artistName']+"|"+songLink)

def GetMusic():
    return GetChannelList()

if __name__ == "__main__":
    print GetMusic();
