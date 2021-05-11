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
	client = paho.mqtt.client.Client("tankLevel", False)
	client.qos = 0
	client.connect(host = "localhost")
	waterLevel = 100
	minRedu = 5
	maxRedu = 15
	minInc = 15
	maxInc = 25
	Actualtime = datetime.datetime.now().replace(minute = 0, second = 0, microsecond = 0)

	while(True):
		for i in range(3):
			Actualtime += datetime.timedelta(minutes = 10)
			time.sleep(10)
			reduction = round(random.uniform(minRedu, maxRedu), 0)

			if(reduction < waterLevel):
				waterLevel -= reduction
			else:
				waterLevel = 0;

			data = {
				"date": str(Actualtime),
				"waterLevel": str(waterLevel)
			}
			client.publish("house/bathroom/tank", json.dumps(data), qos = 0)
			print(data)

			if (waterLevel == 0):
				data = {
				"date": str(Actualtime),
				"message": "Empty tank"
				}
				client.publish("house/bathroom/tank", json.dumps(data), qos = 0)
				print(data)
			elif (waterLevel <= 50):
				data = {
				"date": str(Actualtime),
				"message": "Less than half the tank"
				}
				client.publish("house/bathroom/tank", json.dumps(data), qos = 0)
				print(data)
	
		increase = round(random.uniform(minInc, maxInc), 0)

		if (waterLevel + increase < 100):
			waterLevel += increase
		else:
			waterLevel = 100;

		data = {
			"date": str(Actualtime),
			"waterLevel": str(waterLevel)
		}
		client.publish("house/bathroom/tank", json.dumps(data), qos = 0)
		print(data)

if __name__ == "__main__":
	main()
	sys.exit(0)