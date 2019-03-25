import paho.mqtt.client as mqtt
import json
import time
# This is the Publisher

client = mqtt.Client()
client.connect("192.168.43.116",1883,60)
arr = []*360
for j in range (0,100):
	for i in range (0,360):
		arr.append(j)
	data = json.dumps({"a":arr})
	client.publish("topic/test", data);
	time.sleep(1)
client.disconnect();
