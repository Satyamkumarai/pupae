#!/usr/bin/python3
import cv2
import numpy as np
import time
import math
from utils import *
import threading 
import RPi.GPIO as GPIO
from time import sleep
sensor = 21
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor,GPIO.IN,pull_up_down=GPIO.PUD_UP)
interval = 2
start=0
DELAY_FOR_SYNC = 2.25
TRIG_FLAG =0 # not yet triggered


RECORD_RESET = False

#+++++++++++++++++++++++++++++++++++++++++
# Extra trigger for the IR sensor :
RELAY_WAIT_DURATION = 0.1
TRIG_RELAY_PIN = 20
GPIO.setup(TRIG_RELAY_PIN , GPIO.IN)
def trig_relay(pin= TRIG_RELAY_PIN):
    #print("Triggering Relay!")
    GPIO.setup(TRIG_RELAY_PIN , GPIO.OUT)
    sleep(RELAY_WAIT_DURATION)
    GPIO.setup(TRIG_RELAY_PIN , GPIO.IN)
    sleep(RELAY_WAIT_DURATION)
    
#+++++++++++++++++++++++++++++




# the Call back for the hardware interrupt 
def cb(*args,**kwargs):
	global start,RECORD_RESET , sm 
	val = GPIO.input(sensor)
	# only trigger on low value
	if not val:
		intv = time.time()- start 
		#print(intv, "time passed")
		# and if the "bounce period " has  exceeded
		if intv>interval:
			start=time.time()
			#print("Triggered at Value: ",sm)
			# trigger a relay
			trig_relay()
			# set reset of record values
			RECORD_RESET = True
			#print(f"Record Reset ? :{RECORD_RESET}")
			#print("Exit from call back ")
			# run the main function
# 			activate_relay(sm)



# event to trigger the callback when the IR sensor gets triggered
GPIO.add_event_detect(sensor,GPIO.RISING,callback=cb,bouncetime=300)


# function used to toggle the correspinding relay based on classification (ind is the classification index of CLASSES)
def toggle_relay(ind,pinlist=RELAY_PINS):
    pin = pinlist[ind]
    for p in RELAY_PINS:
        if p!=pin:
            GPIO.setup(p,GPIO.IN)
    #print("Turn on ",pin , "and turn others off")
    GPIO.setup(pin,GPIO.OUT)

#function used to activate one of the three relays based on value (sm)
def activate_relay(val=sm):
    global sm
    out_ind,out_class = classify_range(val)
    toggle_relay(out_ind)




# sm holds the total sm values till current frame ( between two triggers )
# frame number records the number of values recored ( between two triggers )


def main():
    global tot,values,frameNo,y1,y2,x1,x2,GREEN,thickness,DURATION,sm,RECORD_RESET
    print("main")
    while 1:
        # first capture the frame and get the sum
        _, frame = cap.read()
        #print(f"frame:{frameNo}, sm:{sm} ")
#, startof newframe: {RECORD_RESET}
        # read a new frame
        frameNo+=1
        # cropping and image transformations
        cropped = frame[y1:y2,x1:x2]
        hsr_frame = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)
        low_R = getTh(window)
        high_r = getTh(window,False)
        image = cv2.inRange(hsr_frame,low_R,high_r)
        # RED is the actual transformed image
        RED = cv2.bitwise_and(cropped, cropped, mask=image)
        
        # show the actual frames
        cv2.imshow("red image", RED) 
        rectImage= cv2.rectangle(frame,(x1,y1),(x2,y2),GREEN, thickness)
        cv2.imshow("Frame Rect",rectImage)
        key = cv2.waitKey(1)
        if key == 27:
            break
        
        
        sm += np.sum(RED)
        # the IR sensor has been triggerd
        if RECORD_RESET:
            # calc sum
            avg = sm / frameNo
            
            #print the average values:
            print(f"Average val:{avg}, ",classify_range(avg))
            # classify Pupae 
            activate_relay(val=avg) 
            #reset calc
            sm,frameNo=0,0
            #print(f"Setting Record reset {RECORD_RESET} to false")
            RECORD_RESET=False
        else :
            continue

# while True:
#         
#         
#         
#         
#         
#         
#         
#         st= time.time()
#         _, frame = cap.read()
#         #cropping the frame
#         cropped = frame[y1:y2,x1:x2]
#         hsr_frame = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)
#         # setting the Threshold values
#         low_R = getTh(window)
#         high_r = getTh(window,False)
#         image = cv2.inRange(hsr_frame,low_R,high_r)
#         RED = cv2.bitwise_and(cropped, cropped, mask=image)
#         sm = np.sum(RED)/10
#         first_val = values.pop(0)
#         tot-=first_val
#         tot+=sm
#         values.append(sm)
#         out_ind,out_class = classify_range(sm)
#         print(f"Total=\t{sm}\tGender:{out_class}",end = " ")
#         #cv2.imshow("Frame", frame)
#         print(f"\t-\t{time.time()-st} s")   
    
    
if __name__=='__main__':
    import sys
    try:
        main()
        # close all windows and release the capture obj clean up all gpios
        cap.release()
        cv2.destroyAllWindows()
        GPIO.cleanup()
        sys.exit(0)
    except:
        sys.exit(0)



