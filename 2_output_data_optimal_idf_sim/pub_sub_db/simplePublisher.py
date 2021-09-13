import paho.mqtt.client as PahoMQTT
import time
import pandas as pd
import json
import datetime

class MyPublisher:
	def __init__(self, clientID):
		self.clientID = clientID
		# create an instance of paho.mqtt.client
		self._paho_mqtt = PahoMQTT.Client(self.clientID, False) 
		# register the callback
		self._paho_mqtt.on_connect = self.myOnConnect
		self.messageBroker = 'localhost'

	def start (self):
		#manage connection to broker
		self._paho_mqtt.connect(self.messageBroker, 1883)
		self._paho_mqtt.loop_start()

	def stop (self):
		self._paho_mqtt.loop_stop()
		self._paho_mqtt.disconnect()

	def myPublish(self, topic, message):
		# publish a message with a certain topic
		self._paho_mqtt.publish(topic, message, 2)

	def myOnConnect (self, paho_mqtt, userdata, flags, rc):
		print ("Connected to %s with result code: %d" % (self.messageBroker, rc))



if __name__ == "__main__":
	test = MyPublisher("MyPublisher")
	test.start()
	df  = pd.read_csv('/home/ict4bd/py3/project/2_output_data_optimal_idf_sim/pub_sub_db/data_2021.csv')

	df['Date/Time'] = '2021/' + df['Date/Time'].str.strip()
	df['Date/Time'] = df['Date/Time'].str.replace('24:00:00','23:59:59')

	df['Date/Time'] = pd.to_datetime(df['Date/Time'], format="%Y/%m/%d  %H:%M:%S")

    
	output=[]
	for i in df["Date/Time"]:
		output.append(time.mktime(datetime.datetime.strptime(str(i), "%Y-%m-%d %H:%M:%S").timetuple()))
	df.index = output
	df = df.drop("Date/Time", axis=1)
    
	GATEWAY_NAME="Athens"
	k=0
	for i in df.index:
		print(i)	
		
		for j in df.loc[i].items():
			print(k)
			k+=1
			
			print(j)
			nodeID=j[0]
			value=j[1]
			if nodeID=='Power':
				measurement="Power"
			elif nodeID=='Heating Power':
				measurement='Power'
			elif nodeID=='Cooling Power':
				measurement= 'Power'
			else:
				measurement="Temperature"
			payload={
						"location":str(GATEWAY_NAME),
						"measurement":measurement,
						"node":str(nodeID),
						"time_stamp":i,
						"value": value}
			try:
				test.myPublish ('ict4bd', json.dumps(payload)) 	
				time.sleep(0.1)
			
			except: 
				print("Error")
				print("node: ",nodeID)
				print("val: ", value)
				print(i)

	test.stop()
