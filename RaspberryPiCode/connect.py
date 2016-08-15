import paho.mqtt.client as mqtt
import os

configfile = '/home/pi/NestProject/data.log'

def replace_line(file_name, line_num, text):
   lines = open(file_name, 'r').readlines()
   lines[line_num] = text
   out = open(file_name, 'w')
   out.writelines(lines)
   out.close()


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("SetSensorState")
    client.subscribe("SetTemperature")

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+(msg.payload))
    
    if msg.topic == "SetTemperature":

		set_temp = 'set_temp = ' + msg.payload + '\n'
        	mode = 'a' if os.path.exists(configfile) else 'w'
        	with open(configfile, mode) as f:
            		replace_line(configfile, 0, set_temp)
	#print(set_temp)
    if msg.topic == "SetSensorState":
        
		state = 'state = ' + msg.payload + '\n'      
        	mode = 'a' if os.path.exists(configfile) else 'w'
        	with open(configfile, mode) as f:
            		replace_line(configfile, 1, state)

	#print sensor_state
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(host="52.26.17.88", port=1883, keepalive=60, bind_address="")



# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()