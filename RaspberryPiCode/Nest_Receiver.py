import RPi.GPIO as GPIO, time, os
import paho.mqtt.client as mqtt
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
from pi_switch import RCSwitchReceiver

receiver = RCSwitchReceiver()
receiver.enableReceive(7)
s_temp=0
s_state=True
GPIO.setup(18,GPIO.OUT)
hvac_pin = GPIO.PWM(18,100) 

configfile = '/home/pi/NestProject/data.log'
def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))  


def hvac_control(set_temp,current_temp,flag,start):
    print set_temp
    print current_temp
    print flag		
    if(current_temp < set_temp):
	print("Here")
        if(flag ==False):
		hvac_pin.start(20)
		flag=True
		print("turn heater on")
		start=time.clock()
	return(0,flag,start)
    if(current_temp > set_temp):
        print("do someting")
    	return(0,flag,0)
    if(current_temp==set_temp):
        hvac_pin.stop()
        print("turn heater off")
	print "flag= ",flag	
        if(flag==True):
			on_duration = (time.clock())-start	
			flag= False
			return(on_duration,flag,0)
	else :
		return(0,flag,0)

client = mqtt.Client()
client.on_connect = on_connect

client.connect(host="52.26.17.88", port=1883, keepalive=60, bind_address="")



count=0

while True:
    conf = open(configfile, 'r')
    ln = conf.readlines()
    sen_temp = ln[0].split("=")
    sen_state = ln[1].split("=")
    s_temp = str(sen_temp[1].strip())
    s_state = str(sen_state[1].strip())
    #print "Set Temp : ",s_temp 
    #print "SensorState : " ,s_state
   	
    if(s_state=="true"):
	sensor_state= True
    if(s_state=="false"):
	sensor_state=False		 
    #print("receiver.available : " + str(receiver.available()))
    #print sensor_state
    conf.close()
    if(sensor_state):
		if (count==0):
			start=0
			flag=False
			count=1			
		if receiver.available():
			received_value = receiver.getReceivedValue()
			#print(received_value)  
			#print "state = ",sensor_state
			#print "s_temp = ",s_temp 
			number_string = str(received_value)
			data_type = int(number_string[1])
		
			checksumVal = (int(number_string[0]) + int(number_string[1]) + int(number_string[2]) + int(number_string[3])) * int(number_string[4])
			#print(checksumVal)
			if(checksumVal == int(number_string[-3:])):
                		current_time = time.strftime("%H%M")
				#print("Checksum is equal")
				if(data_type == 1):
					
					
					time_on,flag,start_u=hvac_control(int(s_temp),int(number_string[2:4]),bool(flag),start)
					start=start_u
					#print "timeon= ",time_on
					print "flag = ", flag
                    			sensor_CurrentState = '{"SensorState":"' + str(sensor_state) + '"}'
					client.publish("sensorState", sensor_CurrentState)
					sensorMessage_temperature = '{"Time":' + str(current_time) + ',"Temperature":' + number_string[2:4] + '}'
					#client.publish("sensorData", sensorMessage_temperature, qos=2, retain=True)
					client.publish("sensorTemp", sensorMessage_temperature)
				if(data_type == 2):
					sensorMessage_humidity = '{"Time":' + str(current_time) + ',"Humidity":' + number_string[2:4] + '}'
					#client.publish("sensorData", sensorMessage_humidity, qos=2, retain=True)
					client.publish("sensorHumidity", sensorMessage_humidity)
			receiver.resetAvailable()
			time.sleep(2)
    
    else:
		Defaultstate= '{"SensorState":"' + str(sensor_state) + '"}'
		client.publish("sensorState", Defaultstate)
		time.sleep(2)
		conf.close()
