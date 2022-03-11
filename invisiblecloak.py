import cv2
import time
import numpy

fourcc = cv2.VideoWriter_fourcc(*'XVID')
outputFile = cv2.VideoWriter('out.avi',fourcc,20.0,(640,480))

cap = cv2.VideoCapture(0)
time.sleep(2)

bg = 0

for i in range(60):
    ret,bg = cap.read()
bg = numpy.flip(bg, axis = 1)

while(cap.isOpened()):
    ret,img = cap.read()

    if not ret:
        break
    img=numpy.flip(img, axis = 1)

    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    lowerRed = numpy.array([0,120,50])
    upperRed = numpy.array([10,245,255])
    mask1 = cv2.inRange(hsv,lowerRed,upperRed)

    lowerRed2 = numpy.array([170,120,70])
    upperRed2 = numpy.array([180,255,255])
    mask2 = cv2.inRange(hsv,lowerRed2,upperRed2)

    mask1 = mask1 + mask2
    mask1 = cv2.morphologyEx(mask1,cv2.MORPH_OPEN,numpy.ones((3,3),numpy.uint8))
    mask1 = cv2.morphologyEx(mask1,cv2.MORPH_DILATE,numpy.ones((3,3),numpy.uint8))

    mask2 = cv2.bitwise_not(mask1)

    resolution1 = cv2.bitwise_and(img,img,mask = mask2)
    resolution2 = cv2.bitwise_and(bg,bg,mask = mask2)

    finalOutput = cv2.addWeighted(resolution1,1,resolution2,1,0)
    outputFile.write(finalOutput)
    cv2.imshow('magic',finalOutput)
    cv2.waitKey(1)
cap.release()
out.release()
cv2.destroyAllWindow()