#!/usr/bin/python
####################################################################
# Turn an LED on or off
# copyright (c) Charles Shapiro  February 2018
#
#   This file is part of raspi_blinky.
#   raspi_blinky is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#   raspi_blinky is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#   You should have received a copy of the GNU General Public License
#   along with raspi_blinky.  If not, see <http://www.gnu.org/licenses/>.
####################################################################

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
		"""Set pin LED is on. """
		self.ledPin = LEDPin
		self.setup(LEDPin,warnings)

	def blink(self,interval,count):
		"""Mostly for testing.  Do blink forever in calling code."""
                self.Status = "BLINK"
		for kk in range(0,count):
			self.on()
  			time.sleep(interval)
			GPIO.output(self.ledPin,GPIO.LOW)
			time.sleep(interval)
                self.Status = "OFF"
                

	def on(self):
		"""Turn the LED on"""
                self.Status = "ON"
		GPIO.output(self.ledPin,GPIO.HIGH)

	def off(self):
		"""Turn the LED off"""
                self.Status = "OFF"
		GPIO.output(self.ledPin,GPIO.LOW)
	
	def cleanup(self):
		"""Leave GPIO library properly closed. This turns LED off"""
                self.Status = "OFF"
		GPIO.cleanup()

# Testing code below
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
		
