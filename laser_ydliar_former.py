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


# Firebase Initialization
def set_init():
    cred = credentials.Certificate("/home/erion/catkin_ros_ws/src/erion/erion_pi/src/script/erion_key.json")
    firebase_admin.initialize_app(cred)
    print("firebase certificated")

# min / max filter
def saturate(value,min,max):
    if value<min:
        return min
    elif value > max:
        return max
    else:
        return value

def callback(msg):
    deg_arr=[428,361,291]
    temp=10
    left_bcor = int(max(msg.ranges[deg_arr[0]-temp:deg_arr[0]+temp])*100)
    middle_bcor = int(max(msg.ranges[deg_arr[1]-temp:deg_arr[1]+temp])*100)
    right_bcor = int(max(msg.ranges[deg_arr[2]-temp:deg_arr[2]+temp])*100)
    #lidar_array = array(3, [left, middle, right])
    
    #collection
    left=saturate(left_bcor,20,300)
    middle=saturate(middle_bcor,20,300)
    right=saturate(right_bcor,20,300)

    print("deg(-30) : {:.0f}[cm], deg(0) : {:.0f}[cm], deg(30) : {:.0f}[cm]".format(left,middle,right))
    pub = rospy.Publisher('/erion_scan', Int16MultiArray, queue_size=10)
    data_to_send = Int16MultiArray()  # the data to be sent, initialise the array
    data_to_send.data = [left,middle,right] # assign the array with the value you want to send
    pub.publish(data_to_send)
    #firebase_lidar_set=upload_lidar_mode(left,middle,right)
    #print(f"firebase set complte : {firebase_lidar_set}")


    
# # firebase func
# #Upload Lidar Info
def upload_lidar_mode(left,middle,right):
    db = firestore.client()
    doc_ref = db.collection('pi').document('property')
    doc_ref.update({
    'range':[left,middle,right]
    })
    return True




if __name__ == "__main__":
    try:
        rospy.init_node("laser_ydlidar")
        set_init()
        sub=rospy.Subscriber("/scan",LaserScan,callback)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass