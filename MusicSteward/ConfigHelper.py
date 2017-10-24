#-*- coding: utf-8 -*-
import ConfigParser

# By Niuxuan(zuomu) QQ:79069622
iniPath = "/home/pi/MyPrograms/MusicSteward/Configs/base.ini"

#获取基础配置
def GetIni(key,value="",title="base"):
    try:
        config = ConfigParser.ConfigParser()
        config.readfp(open(iniPath),"rb")
        return config.get(title,key).decode("gbk")
    except Exception,e:
        return value
        pass

#获取屏蔽信息
def GetDisabled(key,title="disabled"):
    try:
        result = GetIni(key,"",title)
        return result.split(",")
    except Exception,e:
        return []
        pass

#获取语音词组
def GetWord(key,title="word"):
    try:
        return GetIni(key,"突然不知道该说啥好呢",title)
    except Exception,e:
        print e
        return "突然不知道该说啥好呢"
        pass

#获取家人mac
def GetFamily(key):
    return GetIni(key,"","familyList")

#获取朋友mac
def GetFriend(key):
    return GetIni(key,"","friendList")
    
#获取忽略mac
def GetNone(key):
    return GetIni(key,"","noneList")

def SetValue(title,key,value):
    config = ConfigParser.ConfigParser()
    config.readfp(open(iniPath),"rb")
    config.set(title, key, value)
    config.write(open(iniPath, "w"))
    
if __name__ == "__main__":
    print GetWord("smjg")
