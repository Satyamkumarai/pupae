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
# sensor Desensitize period
interval = 2
# start timer for proximity sensor
start=0

DELAY_FOR_SYNC = 2.25

# start timer for recording
start_rec_time = 0

# time after trigger to stop recording 
rec_interval_high = 2.0
# time after triger to start recording 
rec_interval_low = 1.0

# Is it recording 
RECORDING = False

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
    
#++++++++++++++++++++++++++++

# the Call back for the hardware interrupt
def cb(*args,**kwargs):
	global start,RECORDING , sm , start_rec_time
	val = GPIO.input(sensor)
	#print("TRIO")
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
			#print("start Rec")
			RECORDING = True




# event to trigger the callback when the IR sensor gets triggered
GPIO.add_event_detect(sensor,GPIO.FALLING,callback=cb,bouncetime=300)


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




# sm           : total sm values till current frame ( between two triggers )
# frame number : number of values recored ( between two triggers )


def main():
    print("Starting..")
    create_color_threshold_window()
    global tot,values,frameNo,y1,y2,x1,x2,GREEN,thickness,DURATION,sm,RECORD_RESET, start_rec_t
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
        # Recording start
        if RECORDING:


	    # reset the timer
	    start_rec_t = time.time()
            # calc sum
            avg = sm / frameNo
            #print the average values:
            print(f"Average val:{avg}, ",classify_range(avg))
            # classify Pupae 
            activate_relay(val=avg) 
            #reset calc
            sm,frameNo=0,0
            #print(f"Setting Record reset {RECORD_RESET} to false")
            RECORDING=False
        else :
            continue

    
    
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



