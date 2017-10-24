# -*- coding: UTF-8 -*-
import sys,urllib2,json

# By Niuxuan(zuomu) QQ:79069622
cityList = [
    {'code':"101280601", 'name':"深圳"},
    {'code':"101250501", 'name':"郴州"}
]

def getCityWeather_RealTime(cityName):
    cityID = getCityCodeFromName(cityName)
    url = "http://www.weather.com.cn/data/sk/" + str(cityID) + ".html"  
    try:  
        req=urllib2.Request(url)  
        stdout = urllib2.urlopen(url)  
        weatherInfomation = stdout.read().decode('utf-8')          
          
        data=json.loads(weatherInfomation)
        msg = data["weatherinfo"]

        result = u"气温:%s摄氏度，风向:%s，湿度:%s"%(msg["temp"],msg["WD"],msg["SD"])

        
    except (SyntaxError) as err:  
        return u"天气获取异常"
    except:  
        return u"天气获取失败"
    else:  
        return result  
    finally:  
        None  
          
def getCityCodeFromName(cityName):  
    for item in cityList:  
        #n = unicode(item['name'],'utf-8')  
        #print n,cityName  
        if item['name']==cityName:  
            #print 'equal'  
            return item['code']  
    return ''

