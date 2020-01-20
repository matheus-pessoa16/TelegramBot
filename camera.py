import numpy as np
import cv2
from threading import Thread

signal = False

def stop(value):
    signal = value

def start():
    stop(False)
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface.xml')
    while(True):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        if(len(faces)):
            for (x,y,w,h) in faces:
                frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            cv2.imwrite('foto.png',frame)
            break
    cap.release()
