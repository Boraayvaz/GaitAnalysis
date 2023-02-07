import cv2
from flask import Flask , render_template , Response
from threading import Thread


app = Flask(__name__)
cap = cv2.VideoCapture(1)
dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters_create()

def TakeFrame(capt,d,p):
    ret,frame1=capt.read()

    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frame1, d,parameters=p)
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
        x = min(xarray)
        y = min(yarray)
        w = max(xarray)
        h = max(yarray)
        center_x = (c11 + c41 + c31 + c21) //4
        center_y = (c12 + c22 + c32 + c42 ) //4
    else:
        x=int(0)
        y=int(0)
        w=int(0)
        h=int(0)
        center_x = int(-1)
        center_y = int(-1)        
    image1 = cv2.rectangle(frame1, (x, y), (w, h), (0, 255, 255), 2) # Draw the bounding box around the yellow object
    image = cv2.circle(image1, (center_x, center_y), 5, (0, 0, 255), -1)
    return image 
    

def get_frame():
    while True:
        frame = TakeFrame(cap, dictionary, parameters)
        _,buffer=cv2.imencode(".jpg",frame)
        frame=buffer.tobytes()
        yield(b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n'+ frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(get_frame(),mimetype='multipart/x-mixed-replace;boundary=frame')
def videoThread():
    app.run(debug=True)

if __name__=='__main__':
    #app.run(debug=True)
    tvideo = Thread(target=videoThread())
    tvideo.start()

