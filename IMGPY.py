#!/usr/bin/env python3
import cv2
import paho.mqtt.client as paho
from time import sleep
import numpy as np
import json
 
# Define the lower and upper bounds of the yellow color in the HSV color space
lower_yellow = np.array([22, 93, 0])
upper_yellow = np.array([45, 255, 255])
msg0 = 1
# Open the camera
cap = cv2.VideoCapture(0)
prev_center_x = None
prev_center_y = None
prev_velocity_x = 0
prev_velocity_y = 0

broker="160.75.154.101" #mqtt cloud ip'si
port=1884
username="iturockwell"
password="963258741"
msg0 = 5
data = '0'
dataTopic = ''

 
def on_message(client, userdata, message): #MQTT topic'e subscribe olma
    ##time.sleep(1)
    #global IntVal
    value = str(message.payload.decode("utf-8"))
    #print(value)
    #IntVal = int(value)
    global data #bağlanılan topicten gelen veri
    global dataTopic #bağlanılan topic ismi
    data = str(message.payload.decode("utf-8"))
    dataTopic = str(message.topic)

client= paho.Client("client-001")
######Bind function to callback
client.on_message=on_message
#####
client.username_pw_set(username, password)
client.connect(broker, port)#connect
client.loop_start() #start loop to process received messages
#client.subscribe("BoraDeneme",0)#subscribe    
 
while True:
    # Read the frame from the camera
    _, frame = cap.read()
 
    # Convert the frame to the HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
    # Create a mask for the yellow color
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
 
    # Find the contours of the yellow object
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
 
    if contours:
        # Find the bounding box of the largest contour
        x, y, w, h = cv2.boundingRect(max(contours, key=cv2.contourArea))
 
        center_x = x+w//2
        center_y = y+h//2
        
        if prev_center_x is not None and prev_center_y is not None:
            # Assume that the time elapsed is 1 second
            time_elapsed = 1
            velocity_x = (center_x - prev_center_x) / time_elapsed
            velocity_y = (center_y - prev_center_y) / time_elapsed
            # Calculate the acceleration using the previous and current velocity
            acceleration_x = (velocity_x - prev_velocity_x) / time_elapsed
            acceleration_y = (velocity_y - prev_velocity_y) / time_elapsed
            print(f"Acceleration: ({acceleration_x}, {acceleration_y})")
            
            msg0 = acceleration_x
            client.publish("BoraDeneme1",msg0)
            
            # Update the previous velocity
            prev_velocity_x = velocity_x
            prev_velocity_y = velocity_y
 
        # Update the previous position of the center
        prev_center_x = center_x
        prev_center_y = center_y           
        # Draw the bounding box around the yellow object
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
        cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
 
    # Display the frame
    cv2.imshow("Frame", frame)
 
    # Check if the user pressed the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
