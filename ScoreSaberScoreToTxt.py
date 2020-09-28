from urllib.request import urlopen, Request
from datetime import datetime
import re
import time
import configparser
import sys
import os
def clear():
    os.system( 'cls' )



config = configparser.ConfigParser()
config.read('config.ini')
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}
confurl = config['(REQUIRED) Your ScoreSaber.com URL']['url']
if confurl == '' or not re.match('https://scoresaber.com/u/', confurl):
    print('PLEASE SPECIFY YOUR SCORESABER URL IN THE config.ini FILE')
    time.sleep(6)
    sys.exit()
req = Request(url=confurl, headers=headers)
oold = ""
rankglobal = {}
rankregional = {}
lastbool = config['(progress) bool']['last']
hourbool = config['(progress) bool']['1hour']
daybool = config['(progress) bool']['1day']
weekbool = config['(progress) bool']['1week']
weeksbool = config['(progress) bool']['4weeks']

rankglobal["last"] = ""
rankregional["last"] = ""






while(True):
   
    currenttime = datetime.now()
    html = urlopen(req).read()
    result = re.search('global">(#[0-9,.]+)</.*png" /> (#[0-9,.]+).*nts:</strong> ([0-9,.]+pp).*ount:</strong> ([0-9.,]+).* Score:</strong> ([0-9,]+)', str(html))
    onew = 'Score Saber Ranking:\nWorldwide: ' + result.group(1) + ' ' + config['(optional) Settings']['country'] + ': ' + result.group(2) + '\nPerformance Points: ' + result.group(3) + ' \nPlay Count: ' + result.group(4) + '\nTotal Score: ' + result.group(5)
    o2 = "timestamp: " + str(int(time.time())) + " global: " + result.group(1).replace("#", "") + " " + "regional: " + result.group(2).replace("#", "") + " last change: " + str(time.ctime())
    
    if onew != oold:
        f = open(config['(optional) Settings']['filename'], "w")
        f2 = open(config['(optional) Settings']['filename2'], "a")
        f.write(onew)
        f.close()
        f2.write(o2 + "\n") 
        f2.close()
        
        
        
        with open('tracker.txt') as f8:
            i=0
            for line in f8:
                temp = re.search('timestamp: (.+?)global: (.+?) regional: (.+?) last', line)
                month = 2419200 #seconds
                week = 604800 #seconds
                day = 86400 #seconds
                hour = 3600 #seconds
                
                if i == 0 and int(temp.group(1)) - int(time.time()) - month <= 0: rankglobal["month"] = temp.group(2)
                if i == 0 and int(temp.group(1)) - int(time.time()) - week <= 0: rankglobal["week"] = temp.group(2)
                if i == 0 and int(temp.group(1)) - int(time.time()) - day <= 0: rankglobal["day"] = temp.group(2)
                if i == 0 and int(temp.group(1)) - int(time.time()) - hour <= 0: rankglobal["hour"] = temp.group(2)
                if i == 0 and int(temp.group(1)) - int(time.time()) - month <= 0: rankregional["month"] = temp.group(3)
                if i == 0 and int(temp.group(1)) - int(time.time()) - week <= 0: rankregional["week"] = temp.group(3)
                if i == 0 and int(temp.group(1)) - int(time.time()) - day <= 0: rankregional["day"] = temp.group(3)
                if i == 0 and int(temp.group(1)) - int(time.time()) - hour <= 0: rankregional["hour"] = temp.group(3)

                i = i + 1
                
                
                if int(temp.group(1)) < int(time.time()) - month: rankglobal["month"] = temp.group(2)
                if int(temp.group(1)) < int(time.time()) - week: rankglobal["week"] = temp.group(2)
                if int(temp.group(1)) < int(time.time()) - day: rankglobal["day"] = temp.group(2)
                if int(temp.group(1)) < int(time.time()) - hour: rankglobal["hour"] = temp.group(2)
                if rankglobal["last"] != None: rankglobal["before"] = rankglobal["last"]
                rankglobal["last"] = temp.group(2)

                if int(temp.group(1)) < int(time.time()) - month: rankregional["month"] = temp.group(3)
                if int(temp.group(1)) < int(time.time()) - week: rankregional["week"] = temp.group(3)
                if int(temp.group(1)) < int(time.time()) - day: rankregional["day"] = temp.group(3)
                if int(temp.group(1)) < int(time.time()) - hour: rankregional["hour"] = temp.group(3)
                if rankregional["last"] != None: rankregional["before"] = rankregional["last"]
                rankregional["last"] = temp.group(3)

        #Begin distance
        rankglobal["now"] = result.group(1).replace("#", "").replace(",", "")
        rankregional["now"] = result.group(2).replace("#", "").replace(",", "")
        distanceglobal = int(rankglobal["month"].replace("#", "").replace(",", "")) - int(rankglobal["now"])
        distanceregional = int(rankregional["month"].replace("#", "").replace(",", "")) - int(rankregional["now"])
        if weeksbool == "true":
            f3 = open(config['(optional) Settings']['filename3'], "w")
            f3.write('%+d' %distanceglobal + "\n" +  '%+d' %distanceregional)
            f3.close()


        distanceglobal = int(rankglobal["week"].replace("#", "").replace(",", "")) - int(rankglobal["now"])
        distanceregional = int(rankregional["week"].replace("#", "").replace(",", "")) - int(rankregional["now"])
        if weekbool == "true":
            f4 = open(config['(optional) Settings']['filename4'], "w")
            f4.write('%+d' %distanceglobal + "\n" + '%+d' %distanceregional)
            f4.close()
            

        distanceglobal = int(rankglobal["day"].replace("#", "").replace(",", "")) - int(rankglobal["now"])
        distanceregional = int(rankregional["day"].replace("#", "").replace(",", "")) - int(rankregional["now"])
        if daybool == "true":
            f5 = open(config['(optional) Settings']['filename5'], "w")
            f5.write('%+d' %distanceglobal + "\n" + '%+d' %distanceregional)
            f5.close()
            

        distanceglobal = int(rankglobal["hour"].replace("#", "").replace(",", "")) - int(rankglobal["now"])
        distanceregional = int(rankregional["hour"].replace("#", "").replace(",", "")) - int(rankregional["now"])
        if hourbool == "true":
            f6 = open(config['(optional) Settings']['filename6'], "w")
            f6.write('%+d' %distanceglobal + "\n" + '%+d' %distanceregional)
            f6.close()
            

        distanceglobal = int(rankglobal["before"].replace("#", "").replace(",", "")) - int(rankglobal["now"])
        distanceregional = int(rankregional["before"].replace("#", "").replace(",", "")) - int(rankregional["now"])
        if lastbool == "true":
            f7 = open(config['(optional) Settings']['filename7'], "w")
            f7.write('%+d' %distanceglobal + "\n" + '%+d' %distanceregional)
            f7.close()
        
        clear()
        print("number of stored data: " + str(i))
        print("last Data:             ")
        print("                global " + rankglobal["now"])
        print("              regional " + rankregional["now"])

        oold = onew

    time.sleep(int(config['(optional) Settings']['refreshrate']))
    
