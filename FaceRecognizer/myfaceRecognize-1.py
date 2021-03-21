import face_recognition
import cv2
import os
import matplotlib.pyplot as plt
print(cv2.__version__)
 

 

image = face_recognition.load_image_file("/home/anton/Desktop/PyPro/FaceRecognizer/demoImages/known/Donald Trump.jpg")
image_rgb=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
face_locations = face_recognition.face_locations(image)

for top,right,bottom,left in face_locations:
    cv2.rectangle(image,(left,top),(right,bottom),(0,0,255),2)

    crop_face = image_rgb[top:bottom,left:right]
    cv2.imshow('face',crop_face)
    cv2.waitKey(0)
    cv2.imwrite('test_crop_1.png',crop_face) 