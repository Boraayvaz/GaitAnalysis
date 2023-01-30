#!/usr/bin/env python3
import cv2
from flask import Flask, Response

app = Flask(__name__)

@app.route('/')
def index():
    with open("index.html", "r") as file:
        contents = file.read()
    return contents

def gen():
    cap = cv2.VideoCapture(1)
    while True:
        _, frame = cap.read()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(port=9999)
