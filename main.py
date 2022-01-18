#!/usr/bin/python3
import cv2
import numpy as np
import time
import math
#from .utils import *
cap = cv2.VideoCapture(-1)
window = 'Threshold'
THRESHOLDS = [0,9000,11000,math.inf]
CLASSES = ['MALE','UNSEGREGATED','FEMALE']
#THRESHOLD_MALE = 20000//2
cv2.namedWindow(window)

def empty(pos):
	pass

def classify_range(val,THRESHOLDS =THRESHOLDS,CLASSES=CLASSES):
	if val==0:
		return CLASSES[0]
	for index, th in enumerate(THRESHOLDS):
		if val<=th:
			return CLASSES[index-1]
cv2.createTrackbar('Rl','Threshold',0,255,empty)
cv2.createTrackbar('Gl','Threshold',35,255,empty)
cv2.createTrackbar('Bl','Threshold',70,255,empty)
cv2.createTrackbar('Rh','Threshold',40,255,empty)
cv2.createTrackbar('Gh','Threshold',255,255,empty)
cv2.createTrackbar('Bh','Threshold',255,255,empty)

def getTh(window,low = True):
	r,g,b = 'Rl','Gl','Bl'
	if not low:
		r,g,b = 'Rh','Gh','Bh'
	r = cv2.getTrackbarPos(r,window)
	g = cv2.getTrackbarPos(g,window)
	b = cv2.getTrackbarPos(b,window)
	return np.array([r,g,b])

values = []
tot = 0
frameNo = 0
print("Recording first 10 values")
y1,y2,x1,x2 = 235,260,240,273
GREEN = (0,255,0)
thickness = 1


for i in range(10):
    _, frame = cap.read()
    
    cropped = frame[y1:y2,x1:x2]
    hsr_frame = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)
    
    low_R = getTh(window)
    high_r = getTh(window,False)
    image = cv2.inRange(hsr_frame,low_R,high_r)
    RED = cv2.bitwise_and(cropped, cropped, mask=image)
    sm = np.sum(RED)/10
    values.append(sm)
    tot+=sm


while True:
    st= time.time()
    _, frame = cap.read()
    #cropping the frame
    cropped = frame[y1:y2,x1:x2]
    hsr_frame = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)
    # setting the Threshold values
    low_R = getTh(window)
    high_r = getTh(window,False)
    image = cv2.inRange(hsr_frame,low_R,high_r)
    RED = cv2.bitwise_and(cropped, cropped, mask=image)
    
    sm = np.sum(RED)/10
    first_val = values.pop(0)
    tot-=first_val
    tot+=sm
    values.append(sm)

    print(f"Total=\t{sm}\tGender:{classify_range(sm)}",end = " ")
	
    #cv2.imshow("Frame", frame)
    cv2.imshow("red image", RED) 
    rectImage= cv2.rectangle(frame,(x1,y1),(x2,y2),GREEN, thickness)
    cv2.imshow("Frame Rect",rectImage)
    key = cv2.waitKey(1)
    if key == 27:
        break
    print(f"\t-\t{time.time()-st} s")   
    
cap.release()
cv2.destroyAllWindows()

