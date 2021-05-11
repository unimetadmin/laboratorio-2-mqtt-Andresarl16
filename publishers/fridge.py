import ssl
import sys
import json
import random
import time
import paho.mqtt.client
import paho.mqtt.publish
import random
import datetime

def when_connect(client, userdata, flags, rc):
	print("Publisher Connected")

def main():
	client = paho.mqtt.client.Client("fridge", False)
	client.qos = 0
	client.connect(host = "localhost")
	minTemp = 8
	maxTemp = 12
	minIce = 0
	maxIce = 10
	Actualtime = datetime.datetime.now().replace(minute = 0, second = 0, microsecond = 0)
	sendIceData = True

	while(True):
		temperature = round(random.uniform(minTemp, maxTemp), 2)
		data = {
			"date": str(Actualtime),
			"temperature": str(temperature)
		}
		client.publish("house/kitchen/fridge", json.dumps(data), qos = 0)
		print(data)

		if(sendIceData):
			iceCapacity = round(random.uniform(minIce, maxIce), 2)
			data = {
			"date": str(Actualtime),
			"ice_capacity": str(iceCapacity)
			}
			client.publish("house/kitchen/fridge", json.dumps(data), qos = 0)
			print(data)
		
		Actualtime += datetime.timedelta(minutes = 5)
		sendIceData = not sendIceData
		time.sleep(5)

if __name__ == "__main__":
	main()
	sys.exit(0)