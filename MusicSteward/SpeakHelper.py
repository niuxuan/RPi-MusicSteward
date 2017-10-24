# -*- coding: UTF-8 -*-
import time  
import sys,subprocess,urllib,os,requests
import MusicLoader
import ConfigHelper

# By Niuxuan(zuomu) QQ:79069622
googleAPIurl = "http://translate.google.cn/translate_tts?tl=%s&"
player = "mplayer"
player2 = "omxplayer"

#语音播报(临时)
def SpeakOneTime(lan, words):
    
    param = {'q':words}

    data = urllib.urlencode(param)

    if(lan=="en"):
        """
        subprocess.call([player, (googleAPIurl%lan)+data],
                                  shell=False,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
                                  """
        play(player,(googleAPIurl%lan)+data)
    else:
        try:
            s = requests.Session()
            s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:17.0) Gecko/20100101 Firefox/17.0','Connection': 'Keep-Alive'})

            ret = s.post((googleAPIurl%lan)+data)
            ext = ret.headers["content-type"].split("/")[1]
            filename =("songinfo.%s" % ext)
        
            with open(filename, "wb") as f:
                f.write(ret.content)
                """
            log_file = "./mplayer.log"
            #with open(log_file, "w") as f:
                #subprocess.call([player, filename], stdout=f, stderr=f)
            subprocess.call([player, filename],
                            shell=False,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
            """
            play(player,filename)
        except Exception,e:
            Speak("zh-CN", ConfigHelper.GetWord("speakerror"))#语音异常
            pass

#语音播报(记录)
def Speak(lan, words):
    
    param = {'q':words}

    data = urllib.urlencode(param)

    if(lan=="en"):
        """
        subprocess.call([player, (googleAPIurl%lan)+data],
                                  shell=False,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
        """
        play(player,(googleAPIurl%lan)+data)
    else:
        s = requests.Session()
        s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:17.0) Gecko/20100101 Firefox/17.0','Connection': 'Keep-Alive'})

        filename = r'/home/pi/MyPrograms/MusicSteward/Sounds/%s.mpeg'%words
        if os.path.exists(filename):
            """
            subprocess.call([player, filename],
                                  shell=False,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
            """
            play(player,filename)
        else:
            ret = s.post((googleAPIurl%lan)+data)
            if ret.status_code == 200:
                ext = ret.headers["content-type"].split("/")[1]
                
                with open(filename, "wb") as f:
                    f.write(ret.content)
                """
                log_file = "./"+player+".log"
                with open(log_file, "w") as f:
                    subprocess.call([player, filename], stdout=f, stderr=f)
                    """
                
                play(player,filename)

#播放音乐
def soundStart(talk, cnt = 3):
    dt = list(time.localtime())
    hour = dt[3]
            
    Speak("zh-CN", talk)
    
    count = 0

    if hour < int(ConfigHelper.GetIni("quiettime","6")):
        Speak("zh-CN",ConfigHelper.GetWord("toolate"))#太晚了
        return

    IsPlay = int(ConfigHelper.GetIni("isplay","0"))

    if IsPlay == 1:
        Speak("zh-CN","正在播放")#正在播放
        return
    else:
        while(count<cnt):
            try:
                ConfigHelper.SetValue("base","IsPlay","1")
                #获取音乐信息
                songInfo = (MusicLoader.GetMusic())
                song = songInfo.split("|")
        
                Speak("zh-CN",ConfigHelper.GetWord("exsonginfo"))#即将播放
            
                SpeakOneTime("zh-CN",song[0]+"。歌手："+song[1])
                """
                rec = subprocess.call([player2, song[2]],
                                      shell=False,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
                                      """
                
                rec = play(player2,song[2])
                if(rec == 1 or rec == 0):
                    count += 1
            except Exception,e:
                Speak("zh-CN",ConfigHelper.GetWord("musicerror"))#音乐播放异常
                print e
                pass
        Speak("zh-CN",ConfigHelper.GetWord("musicend"))#音乐结束
        ConfigHelper.SetValue("base","IsPlay","0")

#播放音乐
def play(player, url):
    log_file = "./"+player+".log"
    with open(log_file, "w") as f:
        rec = subprocess.call([player, url], stdout=f, stderr=f)
    return rec
