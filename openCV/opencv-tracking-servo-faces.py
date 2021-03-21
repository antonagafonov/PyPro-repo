import cv2
import matplotlib.pyplot as plt
print(cv2.__version__)
import numpy as np
import time
from adafruit_servokit import ServoKit
kit=ServoKit(channels=16)
from threading import Thread
# Raise this flag to 0 to disable the servos
flagB=1
# use ggplot style for more sophisticated visuals
plt.style.use('ggplot')
line1=[]

print('adafruit_servokit kit loaded')
pan,tilt=(90,135)
kit.servo[0].angle=pan
kit.servo[1].angle=tilt
print('positioned to zero')

VectorX = list()
VectorY = list()
VectorW = list()
VectorH = list()

def nothing(x):
    pass

cv2.namedWindow('Trackbars')
cv2.moveWindow('Trackbars',1320,0)

cv2.createTrackbar('hueLower', 'Trackbars',0,179,nothing)
cv2.createTrackbar('hueUpper', 'Trackbars',35,179,nothing)

cv2.createTrackbar('hue2Lower', 'Trackbars',170,179,nothing)
cv2.createTrackbar('hue2Upper', 'Trackbars',130,179,nothing)

cv2.createTrackbar('satLow', 'Trackbars',100,255,nothing)
cv2.createTrackbar('satHigh', 'Trackbars',182,255,nothing)

cv2.createTrackbar('valLow','Trackbars',90,255,nothing)
cv2.createTrackbar('valHigh','Trackbars',160,255,nothing)

dispW=640
dispH=480
flip=0
#Uncomment These next Two Line for Pi Camera
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam= cv2.VideoCapture(camSet)

#Or, if you have a WEB cam, uncomment the next line
#(If it does not work, try setting to '1' instead of '0')
#cam=cv2.VideoCapture(0)
width=cam.get(cv2.CAP_PROP_FRAME_WIDTH)
height=cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
print('width:',width,'height:',height)
face_cascade=cv2.CascadeClassifier('/home/anton/Desktop/PyPro/cascades/haarcascade_frontalface_default.xml')
# eye_cascade=cv2.CascadeClassifier('/home/anton/Desktop/pyPro/cascades/eye.xml')

flagA=1

while True:
    ret, frame = cam.read()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces=face_cascade.detectMultiScale(gray,1.3,5)
    x,y,w,h = width/2,height/2,0,0 
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2) 
        roi_gray=gray[y:y+h,x:x+w]
        Roi_color=frame[y:y+h,x:x+w]
        # eyes=eye_cascade.detectMultiScale(roi_gray)        
    error=10
    ratio=70
    center_X,center_Y = x + w/2,y + y/2
    delta_X,delta_Y = width/2 - center_X, height/2 - center_Y

    if(flagB):
        try:
            if (abs(delta_X) > error ):
                pan = pan + delta_X/ratio
            if (abs(delta_Y) > error ):           
                tilt = tilt - delta_Y/ratio
            if pan>180:
                pan=180
                print("Pan Out of  Range")   
            if pan<0:
                pan=0
                print("Pan Out of  Range") 
            if tilt>180:
                tilt=180
                print("Tilt Out of  Range") 
            if tilt<0:
                tilt=0
                print("Tilt Out of  Range")                  
            kit.servo[0].angle = pan
            kit.servo[1].angle = tilt
            # time.sleep(.1)
        except NameError as error:
            print('sx still not defined')        
    cv2.imshow('nanoCam',frame)
    cv2.moveWindow('nanoCam',1200,600)
    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
