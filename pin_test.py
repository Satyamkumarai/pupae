import RPi.GPIO as GPIO
import time
relay = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay,GPIO.IN)

def toggle_relay():
	print("Turn on ")
	GPIO.setup(relay,GPIO.OUT)
	time.sleep(1)
	print("turn off")
	GPIO.setup(relay,GPIO.IN)
	time.sleep(1)

try:
	for _ in range(10):
		toggle_relay()
except:
	GPIO.cleanup()
