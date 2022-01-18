#!/usr/bin/python3
import cv2
import numpy as np
import time
import math
from utils import *
import threading 
sensor = 21
import RPi.GPIO as GPIO
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor,GPIO.IN,pull_up_down=GPIO.PUD_UP)
interval = 2
start=0
DELAY_FOR_SYNC = 2.25

def cb(*args,**kwargs):
	global start 
	val = GPIO.input(sensor)
	if not val:
		intv = time.time()- start 
		print(intv, "time passed")
		if intv>interval:
			start=time.time()
			print("Triggered at Value: ",sm)
			time.sleep(DELAY_FOR_SYNC)
			print("Now active",sm)
			activate_relay(sm)
	
	#	print("Outch!")
GPIO.add_event_detect(sensor,GPIO.RISING,callback=cb,bouncetime=300)

#GPIO.setup( GPIO.IN)  
def toggle_relay(ind,pinlist=RELAY_PINS):
    pin = pinlist[ind]
    for p in RELAY_PINS:
        if p!=pin:
            GPIO.setup(p,GPIO.IN)
    print("Turn on ",pin)
    GPIO.setup(pin,GPIO.OUT)
    #time.sleep(1)
    #print("turn off",pin)
    #GPIO.setup(pin,GPIO.IN)
def activate_relay(val=sm):
    global sm
    out_ind,out_class = classify_range(val)
    toggle_relay(out_ind)
    #threading.Timer(DURATION,activate_relay,[sm]).start()
def main():
    global tot,values,frameNo,y1,y2,x1,x2,GREEN,thickness,DURATION,sm
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

    print("Starting the relay ")
#    init_relay()

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
        out_ind,out_class = classify_range(sm)
        print(f"Total=\t{sm}\tGender:{out_class}",end = " ")
        
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
    import sys
    try:
        main()
        GPIO.cleanup()
        sys.exit(0)
    except:
        sys.exit(0)



