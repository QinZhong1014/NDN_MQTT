## Note: NFD, and Python NDN, and MQTT Paho Python client must be installed before trying to run any code.
### MQTT-NDN demo proxy requires to run three files at a certain sequence as follows:
1. #### Run the NFD program. (should be installed before trying anything. This program is written in C++)
2. #### Run the ***/MQTT-NDN/Python MQTT-NDN/examples/demo5.py*** to launch the MQTT-NDN proxy. Note: We have not started the MQTT publisher yet!
3. #### To start a MQTT publisher that constantly publishes some message, we need to run: ***/MQTT-NDN/Python MQTT-NDN/examples/MQTT codes/publisher.py***
4. #### Now we will launch a subscriber. To do this run either: ***/Python NDN/python-ndn/examples/consumer.py*** or ***/MQTT-NDN/Python MQTT-NDN/examples/consumer_1.py***
