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
	client.subscribe(topic='house/living_room/#', qos=2)

def on_message(client, userdata, message):
	if("person_counter" in message.topic):
		message = json.loads(message.payload)

		if("persons" in message):
			query = 'INSERT INTO public.person_counter(date , persons) VALUES (%s, %s);'
			data = (message["date"],int(round(float(message["persons"]), 0)))
			select(query, data)
			print(message)

		elif("message" in message):
			query = 'INSERT INTO public.message(date , message) VALUES (%s, %s);'
			data = (message["date"],message["message"])
			select(query, data)
			print(message)
			
	elif("alexa_eco" in message.topic):
		message = json.loads(message.payload)

		if("temperature" in message):
			query = 'INSERT INTO public.alexa_eco(date , temperature) VALUES (%s, %s);'
			data = (message["date"],float(message["temperature"]))
			select(query, data)
			print(message)

def main():
	client = paho.mqtt.client.Client(client_id='living_room', clean_session=False)
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(host='127.0.0.1', port=1883)
	client.loop_forever()

if __name__ == '__main__':
	main()

sys.exit(0)