#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import sys
import os 
if len(sys.argv) < 2:
	print(f"usage : \n {os.path.basename(__file__)} <pin>")
	sys.exit(0)

relay = int(sys.argv[1])
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay,GPIO.IN)
dur = 0.1
def toggle_relay():
	print("Turn on ")
	GPIO.setup(relay,GPIO.OUT)
	time.sleep(dur )
	print("turn off")
	GPIO.setup(relay,GPIO.IN)
	time.sleep(dur)

try:
	for _ in range(10):
		toggle_relay()
except:
	GPIO.cleanup()
