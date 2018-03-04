#!/usr/bin/python

# Turn an LED on or off

import RPi.GPIO as GPIO
import time

class LedControl:
        """A class to control an LED on Raspberry Pi from Python 2.7"""
        """Status is \"OFF\", \"ON\", or \"BLINK\"."""

        # thepin is the pin number by GPIO.BOARD (e.g. just numbered from the top)
        # warnings is True if you're using this persistently, else false
        def setup(self,thepin,warnings):
                self.Status = "OFF"
		GPIO.setmode(GPIO.BOARD)
		GPIO.setwarnings(warnings)
		GPIO.setup(thepin,GPIO.OUT) 

	def __init__(self,LEDPin,warnings):
		self.ledPin = LEDPin
		self.setup(LEDPin,warnings)

	def blink(self,interval,count):
                self.Status = "BLINK"
		for kk in range(0,count):
			self.on()
  			time.sleep(interval)
			GPIO.output(self.ledPin,GPIO.LOW)
			time.sleep(interval)
                self.Status = "OFF"
                

	def on(self):
                self.Status = "ON"
		GPIO.output(self.ledPin,GPIO.HIGH)

	def off(self):
                self.Status = "OFF"
		GPIO.output(self.ledPin,GPIO.LOW)
	
	def cleanup(self):
                self.Status = "OFF"
		GPIO.cleanup()

if __name__ == '__main__':
	from optparse import OptionParser
	parser=OptionParser()
	parser.add_option("-O","--ON",action="store_true", dest="ON",default=False,help="Turn LED on")
	parser.add_option("-F","--OFF",action="store_true",dest="OFF",default=False,help="Turn LED OFF") 
	parser.add_option("-B","--BLINK",action="store_true",dest="BLINK",default=False,help="Blink LED")
	(options,args) = parser.parse_args()
	
	the_led=LedControl(11,True)
   	if(options.ON):
		the_led.on()
	if(options.OFF):
		the_led.off()
	if(options.BLINK):  
		the_led.blink(1,40)
	
	#  the_led.cleanup()
		
