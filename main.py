#!/usr/bin/python3
import cv2
import numpy as np
import time
import math
from utils import *

def main():
    global tot,values,frameNo,y1,y2,x1,x2,GREEN,thickness
    print("Recording first 10 values")
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

if __name__=='__main__':
    main()