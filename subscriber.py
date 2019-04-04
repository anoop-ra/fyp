import threading 
import json
import paho.mqtt.client as mqtt
import rospy
import time
arr = []

#####################ROS communication ##########################
from sensor_msgs.msg import LaserScan

rospy.init_node('laser_scan_publisher')

scan_pub = rospy.Publisher('scan', LaserScan, queue_size=50)

num_readings = 360
laser_frequency = 40


r = rospy.Rate(1.0)

def ros_pub(): 
    
    current_time = rospy.Time.now()
    global arr
    scan = LaserScan()
    print "ROS OK!"
    scan.header.stamp = current_time
    scan.header.frame_id = 'laser'
    scan.angle_min = -3.14
    scan.angle_max = 3.14
    scan.angle_increment = 3.14*2 / num_readings
    scan.time_increment = (1.0 / laser_frequency) / (num_readings)
    scan.range_min = 0.0
    scan.range_max = 100.0
    scan.ranges = []
    scan.intensities = []  
    scan.ranges = arr
    for i in range(0, num_readings):
        #scan.ranges.append(10*i)  # fake data
        scan.intensities.append(50)  # fake data
    
    scan_pub.publish(scan)
    
    r.sleep()
#################################Ros Communication end #########
# This is the Subscriber

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("topic/test")

def on_message(client, userdata, msg):
  #if msg.payload.decode() == "Hello world!":
    data = msg.payload.decode()
    print type(msg.payload.decode())
    data = json.loads(data.decode())
    global arr
    arr = []*360	
    arr = data.get("a")
    print len(arr)
    # print type(arr)
    client.disconnect()
while True:
	client = mqtt.Client()	
	client.connect("10.42.0.1",1883,60)
	client.subscribe("topic/test")

	# client.on_connect = on_connect
	client.on_message = on_message

	t1 = threading.Thread(target=ros_pub, name='t1')
	t1.start()
	t1.join()	

	client.loop_forever()
