import paho.mqtt.client as mqtt #import the client1
import time
from typing import Optional
from ndn.app import NDNApp
from ndn.encoding import Name, InterestParam, BinaryStr, FormalName, MetaInfo
import logging
###############################################################################

# This is our global message variable. Whenever a new message is published we will update this variable
# then we will send this message to the NDN client
message_1 = "" # For some unknown reason 


"""This method is a binding method. Basically this defines how we would handle the scenerio when some publisher client has just published a new message"""
def on_message(client,userdata,  message):
    # We will ridirect the received data to the NDN client which sends us an interest
    # To do this we must launch a NDN producer code snippet here
    #print("message received " ,str(message.payload.decode("utf-8")))
    global message_1
    message_1 = str(message.payload.decode("utf-8")) 
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

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
client = mqtt.Client("P1") #create new instance
client.on_message=on_message #We attach a function to callback
client.on_connect = on_connect #We attached another function to callback
#Now we set up username and passwords and TLS
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
client.username_pw_set("uhunypy", "Dxftornatu6f656r")
client.loop_start() #start the loop
print("connecting to broker")
# connect to HiveMQ Cloud on port 8883
client.connect("4ee9b4eed30441a0a568e4991a8971cc.s2.eu.hivemq.cloud", 8883) #connect to broker
while not client.connected_flag:#Wait in loop until properly connected
    print("In wait loop")
    time.sleep(1)
print("Subscribing to topic","house/bulbs/bulb1")
client.subscribe("house/bulbs/bulb1")
print("Publishing message to topic","house/bulbs/bulb1")
client.publish("house/bulbs/bulb1","OFF")
time.sleep(4) # wait
client.loop_stop() #stop the loop
client.disconnect()


logging.basicConfig(format='[{asctime}]{levelname}:{message}',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    style='{')


app = NDNApp()


@app.route('/example/testApp')
def on_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
    print(f'>> I: {Name.to_str(name)}, {param}')
    global message_1
    content = message_1.encode()
    app.put_data(name, content=content, freshness_period=10000)
    print(f'<< D: {Name.to_str(name)}')
    print(MetaInfo(freshness_period=10000))
    print(f'Content: (size: {len(content)})')
    print('')


async def main():
    on_interest()
    
if __name__ == '__main__':
    app.run_forever()
