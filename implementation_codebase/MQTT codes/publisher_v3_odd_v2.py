"""Mod. version of "publisher_v3_even.py" so that this uses the desktop broker"""
import paho.mqtt.client as mqtt #import the client1
import time
###############################################################################
"""This method is a binding method. Basically this defines how we would handle the scenerio when some publisher client has just published a new message"""
"""def on_message(client,userdata,message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)"""
# the global variable below is the channel name.
CHANNEL_ID = "sensor2"
# The global variable below is the path name. Put it simply, this shows where a particular sensor is located
PATH_NAME = "/MQTT/myhome/room1/"
"""This method is another binding method. """
def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)
################################################################################
#broker_address="192.168.1.184" #An IP address
#broker_address="iot.eclipse.org"
mqtt.Client.connected_flag=False#create flag in class
print("creating new instance")
client = mqtt.Client("P3") #create new instance
#client.on_message=on_message #We attach a function to callback
client.on_connect = on_connect #We attached another function to callback
#Now we set up username and passwords and TLS
#client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
#client.username_pw_set("uhunypy", "Dxftornatu6f656r")
#client.loop_start() #start the loop
client.loop_start() #start the loop
print("connecting to broker")
# connect to HiveMQ Cloud on port 8883
client.connect("127.0.0.1", 1883) #connect to broker
while not client.connected_flag:#Wait in loop until properly connected
    print("In wait loop")
    time.sleep(1)

#print("Immediately after the connection loop, and the class connected var: ",mqtt.Client.connected_flag) # I just added
#print("Subscribing to topic","house/bulbs/bulb1")
#client.subscribe("house/bulbs/bulb1")

for i in range(100):
    print("Publishing message to topic",PATH_NAME+CHANNEL_ID)
    client.publish(PATH_NAME+CHANNEL_ID,str((2*i)+1))
    time.sleep(4) # wait
client.loop_stop() 
client.disconnect()
#client.loop_stop() #stop the loop
#client.disconnect()

#print("hello, after the MQTT portion")