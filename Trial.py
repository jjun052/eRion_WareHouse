import jetson.inference
import jetson.utils
#import numpy as np
#import cv2

global index
global width
global location
global flag

index = 0
width = 0
location = 0
flag = 0
positionY = 0
positionX = 0



net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)
# For GOOGLENET,
# net = jetson.inference.imageNet("googlenet")
#camera = jetson.utils.videoSource("csi://0")      # '/dev/video0' for V4L2
camera = jetson.utils.videoSource("/dev/video0") 
display = jetson.utils.videoOutput("display://0") # 'my_video.mp4' for file

while display.IsStreaming():
	img = camera.Capture()
	detections = net.Detect(img)
	# cudaDrawRect(input, (left,top,right,bottom), (r,g,b,a), output=None)
	jetson.utils.cudaDrawRect(img, (300,600,900,50), (255,127,0,200))
	#FOR GOOGLENET,
	#detections = net.Classify(img)

	for detection in detections:
		# print(detection)
		index = detections[0].ClassID
		width = (detections[0].Width)
		height = (detections[0].Height)
		position = detections[0].Center


	# print index of item, width and horizonal location

	print(f"width:{width},height:{height},positon:_{position}")	



	display.Render(img)
	display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))



#Reference: 
# 
# https://github.com/XRobots/tracks/blob/master/DeepLearning/Python/camera01.py

