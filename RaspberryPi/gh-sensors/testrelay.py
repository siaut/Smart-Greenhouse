#getting the main GPIO libraly
import RPi.GPIO as GPIO
#time and json
import time
import json

# setting a list of used pins 
pins = [5,6,13,19]

# setting GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#setting the mode for all pins so all will be switched on 
GPIO.setup(pins, GPIO.OUT)

#for loop where pin = 18 next 17 ,15, 14 
for pin in pins :
	#setting the GPIO to HIGH or 1 or true
	GPIO.output(pin,  GPIO.HIGH)
	#wait 0,5 second
	time.sleep(0.5)
	#setting the GPIO to LOW or 0 or false
	GPIO.output(pin,  GPIO.LOW)
	#wait 0,5 second
	time.sleep(0.5)

	#Checking if the current relay is running and printing it 
	if not GPIO.input(pin) : 
		print("Pin "+str(pin)+" is working" )
		

#same but the difference is that  we have 
#for loop where pin = 14 next 15,17,18
# backwards
for pin in reversed(pins) :
	GPIO.output(pin,  GPIO.HIGH)
	time.sleep(0.5)

	GPIO.output(pin,  GPIO.LOW)
	time.sleep(0.5)


#cleaning all GPIO's 
GPIO.cleanup()
print "Shutdown All relays"
