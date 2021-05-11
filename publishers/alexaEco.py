import ssl
import sys
import json
import random
import time
import paho.mqtt.client
import paho.mqtt.publish
import random
import datetime
import requests

def when_connect(client, userdata, flags, rc):
	print("Publisher Connected")

def main():
    client = paho.mqtt.client.Client("alexaEco", False)
    client.qos = 0
    client.connect(host = "localhost")
    Actualtime = datetime.datetime.now().replace(minute = 0, second = 0, microsecond = 0)
    minTemp = 0
    maxTemp = 1
    
    url = "https://api.openweathermap.org/data/2.5/weather?"
    api_key = "127782c6cbdc7abdbed266714daeeade"
    city = "Caracas,VE"

    querystring = url + "appid=" + api_key + "&q=" + city
    response = requests.get(querystring)
    jsonRes = response.json()
    temperature = round(jsonRes["main"]["temp"] - 273.15, 2)

    while(True):
        operation = bool(random.getrandbits(1))
        
        if(operation):
            temperature += round(random.uniform(minTemp, maxTemp), 2)
        else:
            temperature -= round(random.uniform(minTemp, maxTemp), 2)
        temperature = round(temperature,2)
        data = {
            "date": str(Actualtime),
            "temperature": str(temperature)
        }
        client.publish("house/living_room/alexa_eco", json.dumps(data), qos = 0)
        print(data)

        Actualtime += datetime.timedelta(minutes = 3)

        time.sleep(3)
    

if __name__ == "__main__":
	main()
	sys.exit(0)