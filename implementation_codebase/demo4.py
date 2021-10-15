# -----------------------------------------------------------------------------
# Copyright (C) 2019-2020 The python-ndn authors
#
# This file is part of python-ndn.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
"""I pasted the producer code"""

"""Algo:
    1. First connect to the MQTT broker
    2. Upon receipt of an interest from NDN consumer:
        a. Send a subscription to the MQTT broker with the name 
            found in the interest
        b. Whenever a publisher publishes a message, send this 
            message back to the consumer 
        Note: To achieve step b we must solve the interest persistency problem
        """
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -----------------------------------------------------------------------------
from typing import Optional
from ndn.app import NDNApp
from ndn.encoding import Name, InterestParam, BinaryStr, FormalName, MetaInfo
import logging
import paho.mqtt.client as mqtt #import the client1
import time
# A global variable that saves the connection status to the MQTT broker
connected_flag=False
# Message global variable that stores the message we reciev via MQTT
received_message = ""

logging.basicConfig(format='[{asctime}]{levelname}:{message}',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    style='{')


app = NDNApp()

mqtt.Client.connected_flag=False
#  binding method for MQTT
def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)

def on_message(client,userdata,message):
    m = str(message.payload.decode("utf-8"))
    global received_message
    received_message = m
    print("message received via (in MQTT on_message)" ,str(message.payload.decode("utf-8")))
    print("message topic (in MQTT on_message)",message.topic)
    print("message qos (in MQTT on_message)",message.qos)
    print("message retain flag (in MQTT on_message)",message.retain)



client = mqtt.Client("P1") #create new instance
client.on_message=on_message #We attach a function to callback
client.on_connect = on_connect #We attached another function to callback
#Now we set up username and passwords and TLS
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
client.username_pw_set("uhunypy", "Dxftornatu6f656r")

print("connecting to broker")
# connect to HiveMQ Cloud on port 8883
client.connect("4ee9b4eed30441a0a568e4991a8971cc.s2.eu.hivemq.cloud", 8883) #connect to broker
client.loop_start() #start the loop
while not client.connected_flag:#Wait in loop until properly connected
    print("In wait loop")
    time.sleep(1)





@app.route('/example/testApp')
def on_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
    global received_message
    global app
    global client
    """I need to add codes here such that I can subscribe to the broker based on the interest name"""
    print(f'>> I: {Name.to_str(name)}, {param}') # Name of interest
    # Add code to get connected and, send the subscription to the broker
    if not client.connected_flag:#Wait in loop until properly connected
        print("In wait loop")
        time.sleep(1)
    # Now we extract the name from the interest we just received.
    subsription_name = Name.to_str(name)
    
    print("Subscribing to topic:",subsription_name)
    client.subscribe(subsription_name)
    time.sleep(4)
    
    # Now we gotta send the message we received by MQTT, to the NDN client which sent us the interest
    content = received_message.encode()
    client.loop_stop() 
    app.put_data(name, content=content, freshness_period=10000)
    

    """Above I just returned the data which I most recently recieved from the publisher"""
    print(f'<< D: {Name.to_str(name)}')
    print(MetaInfo(freshness_period=10000))
    print(f'Content: (size: {len(content)})')
    print('')


if __name__ == '__main__':
    app.run_forever()
