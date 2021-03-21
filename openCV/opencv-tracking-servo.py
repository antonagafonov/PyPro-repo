# Anton Agafonov
import cv2
import matplotlib.pyplot as plt
print(cv2.__version__)
import numpy as np
import time
from adafruit_servokit import ServoKit
kit=ServoKit(channels=16)
from threading import Thread
# Raise this flag to 0 to disable the servos
flagB=0
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
flagA=1

while True:
    ret, frame = cam.read()
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    hueLow=cv2.getTrackbarPos('hueLower', 'Trackbars')
    hueUp=cv2.getTrackbarPos('hueUpper', 'Trackbars')
    hue2Low=cv2.getTrackbarPos('hue2Lower', 'Trackbars')
    hue2Up=cv2.getTrackbarPos('hue2Upper', 'Trackbars')
    Ls=cv2.getTrackbarPos('satLow', 'Trackbars')
    Us=cv2.getTrackbarPos('satHigh', 'Trackbars')
    Lv=cv2.getTrackbarPos('valLow', 'Trackbars')
    Uv=cv2.getTrackbarPos('valHigh', 'Trackbars')

    l_b=np.array([hueLow,Ls,Lv])
    u_b=np.array([hueUp,Us,Uv])
    l_b2=np.array([hue2Low,Ls,Lv])
    u_b2=np.array([hue2Up,Us,Uv])

    FGmask=cv2.inRange(hsv,l_b,u_b)
    FGmask2=cv2.inRange(hsv,l_b2,u_b2)
    FGmaskComp=cv2.add(FGmask,FGmask2)
    cv2.imshow('FGmaskComp',FGmaskComp)
    cv2.moveWindow('FGmaskComp',0,530)

    contours,_=cv2.findContours(FGmaskComp,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contours=sorted(contours,key=lambda x:cv2.contourArea(x),reverse=True)
    for cnt in contours[:1]:
        area=cv2.contourArea(cnt)
        (x,y,w,h)=cv2.boundingRect(cnt)
        if(flagA):
            previusX,previusY,previusW,previusH=x,y,w,h
            flagA=0    
        if area>=80:
            # cv2.drawContours(frame,[cnt],0,(255,0,0),3)
            prop_Pre=0.2
            prop_Cur=1-prop_Pre
            sx,sy,sw,sh=int(prop_Cur*x + prop_Pre*previusX),int(prop_Cur*y + prop_Pre*previusY),int(prop_Cur*w + prop_Pre*previusW),int(prop_Cur*h + prop_Pre*previusH)
            VectorX.append(sx)
            VectorY.append(sy)
            VectorW.append(sw)
            VectorH.append(sh)
            cv2.rectangle(frame,(sx,sy),(sx+sw,sy+sh),(255,0,0),3)
            previusX,previusY,previusW,previusH=sx,sy,sw,sh
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
    cv2.moveWindow('nanoCam',0,0)
    
    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
