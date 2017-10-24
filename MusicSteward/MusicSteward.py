# -*- coding: UTF-8 -*-
import time,threading
import sys,subprocess
import WeatherHelper
import SpeakHelper
import CheckWifiGuest
import ConfigHelper

# By Niuxuan(zuomu) QQ:79069622
reload(sys)
sys.setdefaultencoding('utf-8')

not_executed = 1

#报时/天气
def aClock():
    currentTime = time.strftime('%Y-%m-%d,%H:%M',time.localtime(time.time()))
    weatherInfo = WeatherHelper.getCityWeather_RealTime(ConfigHelper.GetIni("city"))

    SpeakHelper.Speak("zh-CN",ConfigHelper.GetWord("nowt"))#现在时间是
    SpeakHelper.SpeakOneTime("zh-CN",currentTime+","+weatherInfo)

def main():
    threadWifiCheck = None
    #定义问候语
    jday = ConfigHelper.GetWord("jday")

    eday = ConfigHelper.GetWord("eday")

    vday = ConfigHelper.GetWord("vday")

    #aClock();
    SpeakHelper.Speak("zh-CN", ConfigHelper.GetWord("start"))

    #定义闹钟时间
    while(not_executed):
        try:
            dt = list(time.localtime())
            hour = dt[3]
            minute = dt[4]
            wday = dt[6]
            
            if(wday == 5 or wday == 6):
                if hour == 8 and minute == 00:
                    aClock();
                    SpeakHelper.soundStart(eday)

                if hour == 8 and minute == 30:
                    aClock();
                    SpeakHelper.soundStart(eday)

            else:
                if hour == 6 and minute == 40:
                    aClock();
                    SpeakHelper.soundStart(jday, 3)

                if hour == 7 and minute == 00:
                    aClock();
                    SpeakHelper.soundStart(jday)

                if hour == 7 and minute == 30:
                    aClock();
                    SpeakHelper.soundStart(ConfigHelper.GetWord("bcdl"),3)
                    
                if hour == 8 and minute == 00:
                    aClock();
                    SpeakHelper.soundStart(ConfigHelper.GetWord("bcdl"),3)

            if hour == 22 and minute == 00:
                aClock();
                SpeakHelper.soundStart(ConfigHelper.GetWord("mlyt"))

            if hour == 20 and minute == 00:
                aClock();
                SpeakHelper.soundStart(ConfigHelper.GetWord("dsgb"))

            if(hour > int(ConfigHelper.GetIni("aclock","8")) and minute == 00):
                aClock();
                #避免同一分钟之内多次报时
                time.sleep(int(ConfigHelper.GetIni("smjg","30")))

            if threadWifiCheck is None:
                print "thread begin"
                threadWifiCheck = CheckWifiGuest.CheckGuest()
                threadWifiCheck.start()

        except Exception,e:
            print e
            pass
        finally:
            time.sleep(int(ConfigHelper.GetIni("smjg","30")))

if __name__ == '__main__':
    main()
