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
	client = paho.mqtt.client.Client("personCounter", False)
	client.qos = 0
	client.connect(host = "localhost")
	minPer = 0
	maxPer = 10
	Actualtime = datetime.datetime.now().replace(minute = 0, second = 0, microsecond = 0)

	while(True):
		persons = round(random.uniform(minPer, maxPer), 0)
		data = {
			"date": str(Actualtime),
			"persons": str(persons)
		}
		client.publish("house/living_room/person_counter", json.dumps(data), qos = 0)
		print(data)

		if (persons > 5):
			data = {
			"date": str(Actualtime),
			"message": "Maximum number of people exceeded"
			}
			client.publish("house/living_room/person_counter", json.dumps(data), qos = 0)
			print(data)
			
		Actualtime += datetime.timedelta(minutes = 1)
		time.sleep(1)

if __name__ == "__main__":
	main()
	sys.exit(0)