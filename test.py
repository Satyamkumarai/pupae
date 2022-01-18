import RPi.GPIO as GPIO
from time import sleep
import time
start = 0
GPIO.setmode(GPIO.BCM)
sensor = 21
GPIO.setup(sensor,GPIO.IN,pull_up_down=GPIO.PUD_UP)
interval = 5
def cb(*args,**kwargs):
	global start	
	val = GPIO.input(sensor)
	if not val:
		intv = time.time()- start 
		#print(intv, "time passed")
		if intv>interval:
			start=time.time()
			print("Ouch !",args,kwargs)
	
	#	print("Outch!")
GPIO.add_event_detect(sensor,GPIO.RISING,callback=cb,bouncetime=100)
#GPIO.wait_for_edge(sensor,GPIO.FALLING)
while 1 :
	sleep(12)
