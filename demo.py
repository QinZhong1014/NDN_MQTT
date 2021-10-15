import paho.mqtt.client as mqtt #import the client1
import time
###############################################################################
"""This method is the binding method. Basically this defines how we would handle the scenerio when some publisher client has just published a new message"""
def on_message(client,userdata,message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
################################################################################
broker_address="192.168.1.184" #An IP address
#broker_address="iot.eclipse.org"
print("creating new instance")
client = mqtt.Client("P1") #create new instance
client.on_message=on_message #We attach a function to callback
#Now we set up username and passwords and TLS
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
client.username_pw_set("uhunypy", "Dxftornatu6f656r")

print("connecting to broker")
# connect to HiveMQ Cloud on port 8883
client.connect("4ee9b4eed30441a0a568e4991a8971cc.s2.eu.hivemq.cloud", 8883) #connect to broker
client.loop_start() #start the loop
print("Subscribing to topic","house/bulbs/bulb1")
client.subscribe("house/bulbs/bulb1")
print("Publishing message to topic","house/bulbs/bulb1")
client.publish("house/bulbs/bulb1","OFF")
time.sleep(4) # wait
client.loop_stop() #stop the loop
