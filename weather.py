import json
import requests
import logging
import yaml
from datetime import datetime
from pytz import timezone


# CONFIG FILE
with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

# SERVER INFO
serverName = cfg["server"]["name"]
serverLang = cfg['server']['lang']
units = cfg['server']['units']

# LOCATION
latitude = cfg["location"]["latitude"]
longitude = cfg["location"]["longitude"]
owmCityId = cfg["location"]["owmCityId"]
yahooCityWOEID = cfg["location"]["yahooCityWOEID"]

# DATE AND TIME
fmt = ("%Y-%m-%d %H:%M:%S")
serverTimezone = cfg["server"]["timezone"]
fDate = datetime.now(timezone(serverTimezone)).strftime("%m-%d %H:%M:%S")  #Date and time format

# API KEYS
airlyApiKey = cfg["apiKeys"]["airlyKey"]
owmApiKey = cfg["apiKeys"]["owmKey"]
blynkApiKey = cfg["apiKeys"]["blynkKey"]

# BLYNK SERVER
blynkHostname = cfg["blynkServer"]["hostname"]
blynkPort = cfg["blynkServer"]["port"]

# OPENSTREETMAP
oUrl = 'http://api.openweathermap.org/data/2.5/weather?id=' + owmCityId + '&&lang=' + serverLang +'&units=' + units + '&appid=' + owmApiKey
oResp = requests.get(url=oUrl)
oData = json.loads(oResp.text)
oTemp = oData["main"]["temp"]
oHumidity = oData["main"]["humidity"]
oPressure = str(oData["main"]["pressure"])
oWindspeed = str(oData["wind"]["speed"])
oWinddeg = None
if "deg" in oData["wind"]:  #Sometimes deg parameter is missing
    oWinddeg = str(oData["wind"]["deg"])
oCond = oData["weather"][0]["description"]

# YAHOO WEATHER

yUrl = 'https://query.yahooapis.com/v1/public/yql?q=select%20item.condition%20from%20weather.forecast%20where%20woeid%20%3D%20' + yahooCityWOEID + '%20and%20u%3D\'c\'&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys'
yResp = requests.get(url=yUrl)
yData = json.loads(yResp.text)
yCondition = int(yData["query"]["results"]["channel"]["item"]["condition"]["code"])
yTemp = yData["query"]["results"]["channel"]["item"]["condition"]["temp"]
yDate = yData["query"]["results"]["channel"]["item"]["condition"]["date"]

# conditions to turn fan based on Yahoo codes
if cfg["devices"]["fan"]:
    if yCondition >24 and yCondition<37:
            fanState = '0' #fan on
    else:
            fanState = '1' #fan off
    logging.info("Fan state:" + fanState)
    logging.info("Yahoo code:" + str(yCondition))
else:
    fanState = None
    logging.info("Fan disabled")

# Yahoo condition code to Polish string
if serverLang is "pl":
    def ycondpl(yCondition):
        return {
            28: 'Zachmurzenie',
            26: 'Pochmurno',
            24: 'Wietrznie',
            31: 'Czyste niebo',
            32: 'Slonecznie',
            36: 'Goraco',
            20: 'Mgla',
            11: 'Deszcz',
            12: 'Deszcz',
            4: 'Burze',
            2: 'Huragany',
            0: 'Tornado',
            10: 'Marznacy deszcz',
            9: 'Mzawka',
            8: 'Marznaca mzawka',
            13: 'Sniezyca',
            17: 'Grad',
            18: 'Snieg z deszczem',
            25: 'Zimno',
            19: 'Pyl',
            23: 'Wietrznie',
            45: 'Deszcz piorunow',
            44: 'M. zachmurzenie',
            46: 'Opady sniegu'
        }.get(yCondition, str(yCondition))


# AIRLY
airlyUrl = 'https://airapi.airly.eu/v1/mapPoint/measurements?latitude=' + latitude + '&longitude=' + longitude + '&historyHours=1&historyResolutionHours=1&apikey=' + airlyApiKey
airlyResp = requests.get(url=airlyUrl)
airlyData = json.loads(airlyResp.text)

dpm25 = str(int(airlyData["currentMeasurements"]["pm25"]))
dpm10 = str(int(airlyData["currentMeasurements"]["pm10"]))
dpollution = str(int(airlyData["currentMeasurements"]["pollutionLevel"]))
dcond = str(int(airlyData["currentMeasurements"]["airQualityIndex"]))


# Select available temperature data
bTemp = None
if "temperature" in airlyData["currentMeasurements"]:
        bTemp = airlyData["currentMeasurements"]["temperature"]
        bTemp = str("%.1f" % bTemp)
else:
        if "temp" in oData["main"]:
                bTemp = str(oTemp)
        else:
                if yTemp:
                    bTemp = yTemp
                else:
                    logging.warning("No temperature data available!")

logging.info(fDate)
logging.info("PM2.5:" + dpm25)
logging.info("PM10:" + dpm10)
logging.info("Pollution:" + dpollution)
if bTemp:
    logging.info("Temp:" + bTemp)
logging.info("Air condition:" + dcond)

# SEND DATA TO BLYNK
blynkUrl = 'https://' + blynkHostname +':' + blynkPort + '/' + blynkApiKey +'/update/'
if dpm25:
    requests.get(blynkUrl + "V40?value=" + dpm25)
if dpm10:
    requests.get(blynkUrl + "V41?value=" + dpm10)
if dpollution:
    requests.get(blynkUrl + "V42?value=" + dpollution)
if bTemp:
    requests.get(blynkUrl + "V43?value=" + bTemp)
if dcond:
    requests.get(blynkUrl + "V44?value=" + dcond)
if oCond:
    requests.get(blynkUrl + "V70?value=" + oCond)
if yCondition:
    requests.get(blynkUrl + "V72?value=" + str(yCondition))
if oWindspeed:
    requests.get(blynkUrl + "V47?value=" + oWindspeed)
if oWinddeg:
    requests.get(blynkUrl + "V48?value=" + oWinddeg)
if oPressure:
    requests.get(blynkUrl + "V49?value=" + oPressure)
if fanState:
    requests.get(blynkUrl + "V45?value=" + fanState)
requests.get(blynkUrl + "V46?value=" + fDate)
requests.get(blynkUrl + "V71?value=" + serverName)
