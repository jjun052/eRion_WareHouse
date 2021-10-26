#!/usr/bin/env python3
import rospy
import std_msgs 
import array
from sensor_msgs.msg import LaserScan   
from std_msgs.msg import Int16MultiArray
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time
#import sched


#scheduler = sched.scheduler(time.time, time.sleep)

#def schedule_it(frequency, duration, callable, *args):
#    no_of_events = int( duration / frequency )
#    priority = 1 # not used, lets you assign execution order to events scheduled for the same time
#    for i in xrange( no_of_events ):
#        delay = i * frequency
#        scheduler.enter( delay, priority, callable, args)


# Firebase Initialization
def set_init():
    cred = credentials.Certificate("/home/erion/catkin_ros_ws/src/erion/erion_pi/src/script/erion_key.json")
    firebase_admin.initialize_app(cred)
    print("firebase certificated")



def callback(msg):
    deg_arr=[291,361,428]
    temp=10
    left = int(max(msg.ranges[deg_arr[0]-temp:deg_arr[0]+temp])*100)
    middle = int(max(msg.ranges[deg_arr[1]-temp:deg_arr[1]+temp])*100)
    right = int(max(msg.ranges[deg_arr[2]-temp:deg_arr[2]+temp])*100)
    #lidar_array = array(3, [left, middle, right])

    print("deg(-30) : {:.0f}[cm], deg(0) : {:.0f}[cm], deg(30) : {:.0f}[cm]".format(
        int(max(msg.ranges[deg_arr[0]-temp:deg_arr[0]+temp])*100),
        int(max(msg.ranges[deg_arr[1]-temp:deg_arr[1]+temp])*100),
        int(max(msg.ranges[deg_arr[2]-temp:deg_arr[2]+temp])*100)))
    #a = int(max(msg.ranges[deg_arr[2]-temp:deg_arr[2]+temp])*100)
    #print(type(a))
    pub = rospy.Publisher('/erion_scan', Int16MultiArray, queue_size=10)
    data_to_send = Int16MultiArray()  # the data to be sent, initialise the array
    data_to_send.data = [left,middle,right] # assign the array with the value you want to send
    pub.publish(data_to_send)
    #rospy.Timer(rospy.Duration(2), upload_lidar_mode(left,middle,right))
    
    firebase_lidar_set=upload_lidar_mode(left,middle,right)
    print(f"firebase set complte : {firebase_lidar_set}")


    
# #Firebase func
# #Upload Lidar Info
def upload_lidar_mode(left,middle,right):
    db = firestore.client()
    doc_ref = db.collection('pi').document('property')
    doc_ref.update({
    'range':[left,middle,right]
    })
    return True;


#schedule_it(1, 60, upload_lidar_mode)
#scheduler.run()



if __name__ == "__main__":
    try:
        rospy.init_node("laser_ydlidar")
        set_init()
        sub=rospy.Subscriber("/scan",LaserScan,callback)
        
        rospy.spin()
    except rospy.ROSInterruptException:
        pass