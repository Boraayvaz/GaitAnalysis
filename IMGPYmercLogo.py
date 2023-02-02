#!/usr/bin/env python3
import cv2
import paho.mqtt.client as paho
from time import sleep
import numpy as np
import json
from threading import Thread
import time 
 
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

broker="192.168.4.1" #mqtt cloud ip'si
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

def camView(capture,logo, upper_colour, lower_colour, time_elapsed, pcx, pcy, pvx, pvy, num):
    global msg, accx, accy
    global StringX
    global StringY
    StringX = ""
    StringY = ""
    #logo = cv2.imread("mercedes.jpg", cv2.IMREAD_GRAYSCALE)
    _, frame = capture.read() # Read the frame from the camera
    #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # Convert the frame to the HSV color space   
    #mask = cv2.inRange(hsv, lower_yellow, upper_yellow) # Create a mask for the yellow color
    #contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # Find the contours of the yellow object
    #if contours:
        #x, y, w, h = cv2.boundingRect(max(contours, key=cv2.contourArea)) # Find the bounding box of the largest contour
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Convert the frame to grayscale
    res = cv2.matchTemplate(gray, logo, cv2.TM_CCOEFF_NORMED) # Match the template of the logo in the grayscale frame
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res) # Find the location of the maximum correlation value
    #print(max_val)
    if max_val > 0.4: # Check if the correlation value is high enough to indicate a match
        x = max_loc[0]
        w = logo.shape[1]
        y = max_loc[1]
        h = logo.shape[0]
        #center_x = max_loc[0] + logo.shape[1] // 2
        #center_y = max_loc[1] + logo.shape[0] // 2
        center_x = max_loc[0] + logo.shape[1] // 2
        center_y = max_loc[1] + logo.shape[0] // 2
        #if pcx is not None and pcy is not None:
        velocity_x = (center_x - pcx) / time_elapsed
        velocity_y = (center_y - pcy) / time_elapsed   
        accx = (velocity_x - pvx) / time_elapsed
        accy = (velocity_y - pvy) / time_elapsed
        print(f"Acceleration: ({accx}, {accy})")  
        pvx = velocity_x # Update the previous velocity
        pvy = velocity_y
        pcx = center_x # Update the previous position of the center
        pcy = center_y

    else:
        x = 0
        y=0
        w=0
        h=0
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
    return frame, center_x, center_y, x, y, w, h, msg, pcx, pcy, pvx, pvy




def Camera1(topic1, capt1, image):
        global prev_center_x1
        global prev_center_y1
        global prev_velocity_x1
        global prev_velocity_y1
        lower_colour = np.array([22, 93, 0])
        upper_colour = np.array([45, 255, 255])
        Sample = 0.5
        #image = cv2.imread("mercedes.jpg", cv2.IMREAD_GRAYSCALE)
        frame1, center_x1, center_y1, x1, y1, w1, h1, msg0, prev_center_x11, prev_center_y11,prev_velocity_x11 ,prev_velocity_y11  = camView(capt1,image,upper_colour, lower_colour,1, prev_center_x1, prev_center_y1, prev_velocity_x1,prev_velocity_y1,1)
        cv2.rectangle(frame1, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 255), 2) # Draw the bounding box around the yellow object
        cv2.circle(frame1, (center_x1, center_y1), 5, (0, 0, 255), -1)
        cv2.imshow("Frame", frame1) # Display the frame
        publish(topic1,msg0, 1)
        prev_center_x1 = prev_center_x11
        prev_center_y1 = prev_center_y11
        prev_velocity_x1 = prev_velocity_x11
        prev_velocity_y1 = prev_velocity_y11
        #time.sleep(0.5)
        

def Camera2(topic1, capt2, image):
        global prev_center_x2
        global prev_center_y2
        global prev_velocity_x2
        global prev_velocity_y2
        lower_colour = np.array([22, 93, 0])
        upper_colour = np.array([45, 255, 255])
        Sample = 0.5
        #image = cv2.imread("mercedes.jpg", cv2.IMREAD_GRAYSCALE)
        frame2, center_x2, center_y2, x2, y2, w2, h2, msg2, prev_center_x22, prev_center_y22,prev_velocity_x22 ,prev_velocity_y22  = camView(capt2,image,upper_colour, lower_colour,1, prev_center_x2, prev_center_y2, prev_velocity_x2,prev_velocity_y2,2)
        cv2.rectangle(frame2, (x2, y2), (x2 + w2, y2 + h2), (0, 255, 255), 2) # Draw the bounding box around the yellow object
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
capt1 = cv2.VideoCapture(0)
capt2 = cv2.VideoCapture(1)
time_elapsed = 1

if __name__ =="__main__": 
    while True:
        tCam1 = Thread(target=Camera1(topic1, capt1, img))
        #tCam2 = Thread(target=Camera2(topic1, capt2, img))
        tCam1.start()
        #tCam2.start()
      
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
