import sys
import ssl
import json
import psycopg2
import paho.mqtt.client
from sqlalchemy import create_engine

host='queenie.db.elephantsql.com'
user ='fvptfpjb'
password='HQV6fSyf4CBjvPgbx2br2V1Yn2qBzdRo'
dbname='fvptfpjb'

myConnection = psycopg2.connect(host = host, user= user, password =password, dbname= dbname)

def select(query, data):
    cur = myConnection.cursor()
    try:
        cur.execute(query, data)
    except Exception as e:
        myConnection.commit()
        print('Error en el query:', e)
    else:
    	cur.close()
    	print(myConnection.commit())

def on_connect(client, userdata, flags, rc):
	print('connected (%s)' % client._client_id)
	client.subscribe(topic='house/kitchen/#', qos=2)

def on_message(client, userdata, message):
	if("fridge" in message.topic):
		message = json.loads(message.payload)

		if("temperature" in message):
			query = 'INSERT INTO public.fridge_temperature(date , temperature) VALUES (%s, %s);'
			data = (message["date"],float(message["temperature"]))
			select(query, data)
			print(message)

		elif("ice_capacity" in message):
			query = 'INSERT INTO public.fridge_capacity(date , capacity) VALUES (%s, %s);'
			data = (message["date"],float(message["ice_capacity"]))
			select(query, data)
			print(message)
			
	elif("cooking_pot" in message.topic):
		message = json.loads(message.payload)

		if("temperature" in message):
			query = 'INSERT INTO public.cooking_pot(date , temperature) VALUES (%s, %s);'
			data = (message["date"],float(message["temperature"]))
			select(query, data)
			print(message)

		elif("message" in message):
			query = 'INSERT INTO public.message(date , message) VALUES (%s, %s);'
			data = (message["date"],message["message"])
			select(query, data)
			print(message)

def main():
	client = paho.mqtt.client.Client(client_id='kitchen', clean_session=False)
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(host='127.0.0.1', port=1883)
	client.loop_forever()

if __name__ == '__main__':
	main()

sys.exit(0)