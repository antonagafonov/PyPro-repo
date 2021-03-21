import cv2

print(cv2.__version__)
dispW=640
dispH=480
flip=2
#Uncomment These next Two Line for Pi Camera
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam1= cv2.VideoCapture(camSet)
 
#Or, if you have a WEB cam, uncomment the next line
#(If it does not work, try setting to '1' instead of '0')
# cam2=cv2.VideoCapture(0)

while True:
    ret, frame1 = cam1.read()
    # ret, frame2 = cam2.read()
    cv2.imshow('piCam',frame1)
    # cv2.imshow('webCam',frame2)
    cv2.moveWindow('piCam',0,0)
    # cv2.moveWindow('webCam',400,400)

    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()