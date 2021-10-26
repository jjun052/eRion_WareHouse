import jetson.inference
import jetson.utils

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)
#camera = jetson.utils.videoSource("csi://0")      # '/dev/video0' for V4L2
camera = jetson.utils.gstCamera(1280, 720, "0")
display = jetson.utils.videoOutput("display://0") # 'my_video.mp4' for file

#/while display.IsStreaming():
#	img = camera.Capture()
#	detections = net.Detect(img)
#	display.Render(img)
#	display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

img, width, height = camera.CaptureRGBA (zeroCopy = True)
jetson.utils.cudaDeviceSynchronize ()
# create a numpy ndarray that references the CUDA memory
# it won't be copied, but uses the same memory underneath
aimg = jetson.utils.cudaToNumpy (img, width, height, 4)
#print ("img shape {}".format (aimg1.shape))
aimg1 = cv2.cvtColor (aimg.astype (np.uint8), cv2.COLOR_RGBA2BGR)