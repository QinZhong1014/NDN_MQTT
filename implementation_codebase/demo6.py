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
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -----------------------------------------------------------------------------
from queue import Empty, Full, Queue
from typing import Optional
from ndn.app import NDNApp
from ndn.encoding import Name, InterestParam, BinaryStr, FormalName, MetaInfo
import logging
import paho.mqtt.client as mqtt #import the client1
import time

#The name to which the proxy is about to subscribe to
SUBSCRIPTION_NAME = None
# The global variable below is the path name. Put it simply, this shows where a particular sensor is located
PATH_NAME = "/MQTT/myhome/room1/"

# A global variable that stores the most recent subscription name that proxy dealt with
previous_subscription_name = "" 
mqtt.Client.connected_flag=False
received_message = "dummy!!"
# An additional state variable to store the loop_start or stop state
loop_started:bool = False

# Below is a global variable that stores the message received via MQTT, it is thread safe
q = Queue(1)
#  binding method for MQTT
def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)

def on_message(client,userdata,message):
    m = str(message.payload.decode("utf-8"))
    # We might need to declare a semaphore here to prevent race condition
    global q
    #q.join()
    if (q.qsize()==1):
        # We first discard the old message
        #q.join()
        q.get()
        q.task_done
        q.put(m)
    else:
        q.put(m)
       

    #received_message = m
    print("message received via (in MQTT on_message)" ,str(message.payload.decode("utf-8")))
    print("message topic (in MQTT on_message)",message.topic)
    print("message qos (in MQTT on_message)",message.qos)
    print("message retain flag (in MQTT on_message)",message.retain)

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed to: ", SUBSCRIPTION_NAME)

    #global previous_subscription_name

client = mqtt.Client("P1") #create new instance
client.on_message=on_message #We attach a function to callback
client.on_connect = on_connect #We attached another function to callback
client.on_subscribe = on_subscribe
#Now we set up username and passwords and TLS
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
client.username_pw_set("uhunypy", "Dxftornatu6f656r")

print("connecting to broker")
# connect to HiveMQ Cloud on port 8883
client.connect("4ee9b4eed30441a0a568e4991a8971cc.s2.eu.hivemq.cloud", 8883) #connect to broker
if not loop_started:
    client.loop_start() #start the loop
    loop_started = True

while not client.connected_flag:#Wait in loop until properly connected
    print("In wait loop")
    time.sleep(1)

def start_loop():
    global loop_started
    if not loop_started:
        loop_started = True
    
def stop_loop():
    global loop_started
    if  loop_started:
        loop_started = False


def subscribe(name:str):
    global client
    print("Subscribing to topic","/example/testApp/randomData")
    # I could play with qos, since that is related to reliability
    client.subscribe("/example/testApp/randomData")
    time.sleep(4)

def unsubscribe(name:str):
    global client
    if name is None:
        return
    else:
        try:
            client.unsubscribe(name)
        except ValueError:
            print("Value error detected")
app = NDNApp()

#print("Hello")

@app.route(PATH_NAME)
def on_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
    global loop_started
    global q
    global previous_subscription_name
    global client
    global SUBSCRIPTION_NAME
    """if not loop_started:
        client.loop_start()
        loop_started = True"""
    subsription_name = Name.to_str(name)
    SUBSCRIPTION_NAME = subsription_name # Should I use deepcopy?? Maybe...
    if not (previous_subscription_name == subsription_name):
        loop_started = True
        client.loop_start()
        #subscribe(subsription_name)
        #print("Subscribing to topic",subsription_name) # I commented this out, because it's redundant
        # I could play with qos, since that is related to reliability
        client.subscribe(subsription_name)
        time.sleep(4)
    else:
        print("Subscribing to topic:",subsription_name)
        oop_started = True
        client.loop_start()
        client.subscribe(subsription_name)
        time.sleep(4)
    
    #q.join()
    received_message = q.get()
    q.task_done()
    content = received_message.encode()
    previous_subscription_name = subsription_name
    app.put_data(name, content=content, freshness_period=10000)
    client.loop_stop()
    loop_started = False

if __name__ == '__main__':
    app.run_forever()
