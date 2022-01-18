import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
relay = 23
GPIO.setup(relay, GPIO.OUT) # output rf

# Initial state for LEDs:
print("Testing RF out, Press CTRL+C to exit")

try:
     print("set GIOP high")
     GPIO.output(relay, GPIO.HIGH)
     time.sleep(5)               
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
   print("Keyboard interrupt")

except:
   print("some error") 

finally:
   print("clean up") 
   GPIO.cleanup() # cleanup all GPIO 
