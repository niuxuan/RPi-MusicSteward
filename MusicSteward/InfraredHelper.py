# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import SpeakHelper
import time
import ConfigHelper

# By Niuxuan(zuomu) QQ:79069622
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(12, GPIO.IN)
GPIO.setup(16, GPIO.OUT)

def CheckInfrared(talk,cnt=3):
    flag = True
    count = 0
    
    GPIO.output(16, GPIO.HIGH)
    while flag and count < int(ConfigHelper.GetIni("infrared","60")):
        if(GPIO.input(12)==True):
            GPIO.output(16, GPIO.LOW)
            SpeakHelper.soundStart(talk, cnt)
            #time.sleep(3)
            flag = False
            count = int(ConfigHelper.GetIni("infrared","60"))

        count += 1
        time.sleep(1)
        
    if flag:
        SpeakHelper.Speak("zh-CN", ConfigHelper.GetWord("unfind"))#未扫描到对象

        
