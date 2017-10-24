# -*- coding: utf-8 -*-
import urllib,json,time,threading
import sys,subprocess
import SpeakHelper
import InfraredHelper
import ConfigHelper

oldList = []

# By Niuxuan(zuomu) QQ:79069622
class CheckGuest(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_stop = False
        
        self.oldList = []

    def run(self):
        while not self.thread_stop:
            try:
                rpm = "http://admin:q1q1q1@192.168.7.1/userRpm/WlanStationRpm.htm?Page=1 "
                mf = urllib.urlopen(rpm)
                html = mf.read()
                #html = html.decode('utf8')
                start = html.find("(", html.find("var hostList = new Array(")) 
                end = html.find(";", start)
                listjson = html[start:end].strip()

                listjson = listjson.replace("(\n","").replace(",\n0,0 )","").replace(",","")

                data = listjson.split("\n")

                count = 0;
                listmac = []
                guests = ""
                isKnower = False
                for i in range(0,len(data)/4):

                    listmac.append(data[i*4].replace("\"",""))

                if len(self.oldList)>0 and len(listmac)>len(self.oldList):
                    newmac = set( self.oldList ) ^ set( listmac )
                    for item in newmac:
                        if ConfigHelper.GetFamily(item) != "":
                            isKnower = True
                            guests += ConfigHelper.GetFamily(item)+"，"
                        elif ConfigHelper.GetFriend(item) != "":
                            guests += ConfigHelper.GetFriend(item)+"，"
                        elif ConfigHelper.GetNone(item) != "":
                            None
                        else:
                            guests += ConfigHelper.GetWord("myfriend")
                    if len(guests) > 0:
                        if isKnower:
                            SpeakHelper.Speak("zh-CN", guests + ConfigHelper.GetWord("backhome"))
                            guests += ConfigHelper.GetWord("iwelcome")
                            InfraredHelper.CheckInfrared(guests,3)
                        else:
                            if guests.find(ConfigHelper.GetWord("myfriend")) == -1:
                                time.sleep(20)
                            guests += ConfigHelper.GetWord("owelcome")
                            SpeakHelper.soundStart(guests, 1)

                        listmac = []
    
                self.oldList = listmac
            except Exception,e:
                SpeakHelper.Speak("zh-CN", ConfigHelper.GetWord("scanerror"))
                pass
            finally:
                time.sleep(5)

    def stop(self):
        self.thread_stop = True
