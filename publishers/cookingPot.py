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
	client = paho.mqtt.client.Client("cookingPot", False)
	client.qos = 0
	client.connect(host = "localhost")
	minTemp = 0
	maxTemp = 150
	Actualtime = datetime.datetime.now().replace(minute = 0, second = 0, microsecond = 0)

	while(True):
		temperature = round(random.uniform(minTemp, maxTemp), 2)
		data = {
			"date": str(Actualtime),
			"temperature": str(temperature)
		}
		client.publish("house/kitchen/cooking_pot", json.dumps(data), qos = 0)
		print(data)

		if(temperature >= 100):
			for i in range(60):
				data = {
				"date": str(Actualtime),
				"message": "The water boild"
				}
				client.publish("house/kitchen/cooking_pot", json.dumps(data), qos = 0)
				print(data)
				Actualtime += datetime.timedelta(seconds = 1)
		else:
			Actualtime += datetime.timedelta(minutes = 1)
		
		time.sleep(1)

if __name__ == "__main__":
	main()
	sys.exit(0)