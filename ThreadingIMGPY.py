#!/usr/bin/env python3
import cv2
import paho.mqtt.client as paho
from time import sleep
import numpy as np
import json
from threading import Thread
import time
import math
 
# Define the lower and upper bounds of the yellow color in the HSV color space
lower_yellow = np.array([22, 93, 0])
upper_yellow = np.array([45, 255, 255])


prev_center_x1 = 0
prev_center_y1 = 0
prev_center_x11 = 0
prev_center_y11 = 0
prev_velocity_x1 = 0
prev_velocity_y1 = 0
prev_velocity_x11 = 0
prev_velocity_y11 = 0

prev_center_x2 = 0
prev_center_y2 = 0
prev_center_x22 = 0
prev_center_y22 = 0
prev_velocity_x2 = 0
prev_velocity_y2 = 0
prev_velocity_x22 = 0
prev_velocity_y22 = 0

broker="160.75.154.101" #mqtt cloud ip'si
port=1884
username=""
password=""
msg0 = ""
data = '0'
dataTopic = ''
topic1 = "GA"
topic2 = "GA"
Qos1 = 0
msg0 = ""
i = 0

global msg
 
def on_message(client, userdata, message): #MQTT topic'e subscribe olma
    value = str(message.payload.decode("utf-8"))
    global data
    global dataTopic 
    data = str(message.payload.decode("utf-8"))
    print(data)
    dataTopic = str(message.topic)
    return data

client1= paho.Client("client-001")
client1.on_message=on_message
client1.username_pw_set(username, password)
client1.connect(broker, port)
client1.loop_start()

client2= paho.Client("client-002")
client2.on_message=on_message
client2.username_pw_set(username, password)
client2.connect(broker, port)
client2.loop_start() 


def subscribe(topic, Qos):
    client1.subscribe(topic,Qos)
    global PubSample
    PubSample = int(data)

def publish(topic, msg, Sample):
    client2.publish(topic,msg)
    #time.sleep(Sample)

def camView(capture,time_elapsed, pcx, pcy, pvx, pvy, num, dic ,par):
    global msg, accx, accy
    global StringX
    global StringY
    StringX = ""
    StringY = ""
    ret, frame = capture.read() # Read the frame from the camera
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frame, dic, parameters=par)
    if len(corners) > 0:
        c = corners[0][0]
        c11 = int(c[0][0])
        c12 = int(c[0][1])
        c21 = int(c[1][0])
        c22 = int(c[1][1])
        c31 = int(c[2][0])
        c32 = int(c[2][1])        
        c41 = int(c[3][0])
        c42 = int(c[3][1])
        xarray = [c11, c21, c31, c41]
        yarray = [c12, c22, c32, c42]
        #print( "(" + str(c11) + "," + str(c12) + ")," + "(" + str(c21) + "," + str(c22) + ")," + "(" + str(c31) + "," + str(c32) + ")," + "(" + str(c41) + "," + str(c42) + ")")
        x = min(xarray)
        y = min(yarray)
        w = max(xarray)
        h = max(yarray)
        center_x = (c11 + c41 + c31 + c21) //4
        center_y = (c12 + c22 + c32 + c42 ) //4
        print( str(x) + " " + str(y) + " " + str(w) + " " + str(h))
        #print( str(center_x) + " " + str(center_y))
        velocity_x = (center_x - pcx) / time_elapsed
        velocity_y = (center_y - pcy) / time_elapsed   
        accx = (velocity_x - pvx) / time_elapsed
        accy = (velocity_y - pvy) / time_elapsed
        #print(f"Acceleration: ({accx}, {accy})")  
        pvx = velocity_x # Update the previous velocity
        pvy = velocity_y
        pcx = center_x # Update the previous position of the center
        pcy = center_y
    else:
        x = 0
        y=0
        w=0
        h=0
        c=float(0)
        center_x = 0
        center_y = 0
        velocity_x = 0
        velocity_y = 0
        accx = 0
        accy = 0
        pvx = 0
        pvy = 0
        pcx = 0
        pcy = 0
        StringX = "0"
        StringY = "0"   
    StringX = "AccX" + str(num)
    StringY = "AccY" + str(num)
    msg = json.dumps({StringX: accx, StringY:  accy});
    return frame, center_x, center_y, x, y, w, h, msg, pcx, pcy, pvx, pvy, c




def Camera1(topic1, capt1, d, p):
        global prev_center_x1
        global prev_center_y1
        global prev_velocity_x1
        global prev_velocity_y1
        Sample = 0.5
        #image = cv2.imread("mercedes.jpg", cv2.IMREAD_GRAYSCALE)
        frame1, center_x1, center_y1, x1, y1, w1, h1, msg0, prev_center_x11, prev_center_y11,prev_velocity_x11 ,prev_velocity_y11, c1  = camView(capt1,1, prev_center_x1, prev_center_y1, prev_velocity_x1,prev_velocity_y1,1,d,p)
        cv2.rectangle(frame1, (x1, y1), (w1, h1), (0, 255, 255), 2) # Draw the bounding box around the yellow object
        #cv2.drawContours(frame1, [np.int0(c1)], -1, (0, 255, 255), 5)
        cv2.circle(frame1, (center_x1, center_y1), 5, (0, 0, 255), -1)
        cv2.imshow("Frame", frame1) # Display the frame
        publish(topic1,msg0, 1)
        prev_center_x1 = prev_center_x11
        prev_center_y1 = prev_center_y11
        prev_velocity_x1 = prev_velocity_x11
        prev_velocity_y1 = prev_velocity_y11
        #time.sleep(0.5)
        

def Camera2(topic1, capt2, d,p ):
        global prev_center_x2
        global prev_center_y2
        global prev_velocity_x2
        global prev_velocity_y2
        Sample = 0.5
        #image = cv2.imread("mercedes.jpg", cv2.IMREAD_GRAYSCALE)
        frame2, center_x2, center_y2, x2, y2, w2, h2, msg2, prev_center_x22, prev_center_y22,prev_velocity_x22 ,prev_velocity_y22, c2  = camView(capt2,1, prev_center_x2, prev_center_y2, prev_velocity_x2,prev_velocity_y2,2,d,p)
        cv2.rectangle(frame2, (x2, y2), (w2, h2), (0, 255, 255), 2) # Draw the bounding box around the yellow object
        cv2.circle(frame2, (center_x2, center_y2), 5, (0, 0, 255), -1)
        cv2.imshow("Frame2", frame2) # Display the frame
        publish(topic1,msg2, 1)
        prev_center_x2 = prev_center_x22
        prev_center_y2 = prev_center_y22
        prev_velocity_x2= prev_velocity_x22
        prev_velocity_y2 = prev_velocity_y22
        #time.sleep(0.5)

        
        #return prev_center_x, prev_center_y, prev_velocity_x, prev_velocity_y
# Open the camera
img = cv2.imread("mercedes.png", cv2.IMREAD_GRAYSCALE)

dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters_create()
capt1 = cv2.VideoCapture(0)
capt2 = cv2.VideoCapture(1)
time_elapsed = 1

if __name__ =="__main__": 
    while True:
        tCam1 = Thread(target=Camera1(topic1, capt1, dictionary, parameters))
        tCam2 = Thread(target=Camera2(topic1, capt2 ,dictionary, parameters))
        tCam1.start()
        tCam2.start()
      
        #tsub = Thread(target=subscribe(topic2,Qos1))
        #tsub.start()
      
        if cv2.waitKey(1) & 0xFF == ord('q'): # Check if the user pressed the 'q' key
            tCam1.join()
            tCam2.join()
            break
 
    # Release the camera and close the window
    capt1.release()
    capt2.release()
    cv2.destroyAllWindows()
