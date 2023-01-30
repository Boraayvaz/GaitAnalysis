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


prev_center_x = 0
prev_center_y = 0
prev_center_x1 = 0
prev_center_y1 = 0
prev_velocity_x = 0
prev_velocity_y = 0
prev_velocity_x1 = 0
prev_velocity_y1 = 0

broker="160.75.154.101" #mqtt cloud ip'si
port=1884
username="iturockwell"
password="963258741"
msg0 = ""
data = '0'
dataTopic = ''
topic1 = "topic1"
topic2 = "topic2"
Qos1 = 0
msg0 = ""

bbox = 0

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

def camView(capture, time_elapsed, pcx, pcy, pvx, pvy):
    global msg, accx
    _, frame = capture.read() # Read the frame from the camera
    qr_detector = cv2.QRCodeDetector()
    data, bbox, _ = qr_detector.detectAndDecode(frame)
    if bbox is not None:
        print(bbox)
        x, y, w, h = bbox
        center_x = x + w // 2
        center_y = y + h // 2
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
        accx = 0
        accy = 0
        center_x = 0
        center_y = 0
        x = 0
        y = 0
        w = 0
        h = 0
        
    msg = json.dumps({"AccX": accx,"AccY":  accy});
    
    return frame, center_x, center_y, x, y, w, h, msg, pcx, pcy, pvx, pvy




def Camera1(topic1, capt):
        global prev_center_x
        global prev_center_y
        global prev_velocity_x
        global prev_velocity_y
        Sample = 0.5
        frame, center_x, center_y, x, y, w, h, msg0, prev_center_x1, prev_center_y1,prev_velocity_x1 ,prev_velocity_y1  = camView(capt,1, prev_center_x, prev_center_y, prev_velocity_x,prev_velocity_y)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2) # Draw the bounding box around the yellow object
        cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
        cv2.imshow("Frame", frame) # Display the frame
        publish(topic1,msg0, 1)
        prev_center_x = prev_center_x1
        prev_center_y = prev_center_y1
        prev_velocity_x = prev_velocity_x1
        prev_velocity_y = prev_velocity_y1
        #time.sleep(0.5)

        
        #return prev_center_x, prev_center_y, prev_velocity_x, prev_velocity_y
# Open the camera
cap = cv2.VideoCapture(0)
time_elapsed = 1

if __name__ =="__main__": 
    while True:
        tCam1 = Thread(target=Camera1(topic1, cap))
        tCam1.start()

        
        
        #tsub = Thread(target=subscribe(topic2,Qos1))
        #tsub.start()
        
        #tpub = Thread(target=)
        #tpub.start()  
        
        #tCamView = Thread(target=camView(cap, upper_yellow, lower_yellow))
        #frame, center_x, center_y, x, y, w, h = tCamView.start()

        
        #frame, center_x, center_y, x, y, w, h = camView(cap, upper_yellow, lower_yellow)
        #acceleration_x, acceleration_y, msg0 = accCalc(prev_center_x,prev_center_y, prev_velocity_x, prev_velocity_y, center_x, center_y, frame, time_elapsed)

         
        if cv2.waitKey(1) & 0xFF == ord('q'): # Check if the user pressed the 'q' key
            tCam1.join()
            break
 
    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()
