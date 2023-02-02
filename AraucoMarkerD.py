import cv2
import numpy as np

# Load the camera and initialize the aruco detector
cap = cv2.VideoCapture(0)
dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters_create()

while True:
    # Capture a new frame from the camera
    ret, frame = cap.read()

    # Detect aruco markers in the frame
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)

    # Draw a yellow square around the first detected marker
    if len(corners) > 0:
        c = corners[0][0]
        cv2.drawContours(frame, [np.int0(c)], -1, (0, 255, 255), 5)

    # Display the processed frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up and release resources
cap.release()
cv2.destroyAllWindows()