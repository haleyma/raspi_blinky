#! /usr/bin/python
###################
# LED blinker class using multiprocessing library to control LED
#
# Copyright (C) Charles Shapiro Mar 2018
#
# This file is part of raspi_blinky.
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
###################
from ledController import LedControl
import time
import re
import multiprocessing
import Queue


class ledBlinker():
    """A class using python multiprocessing to blink an LED"""
    def __init__(self,pin):
        """Set up multiprocess and queue for communication"""
        self.ledQ=multiprocessing.Queue()
        self.theProcess=multiprocessing.Process(target=self.ledControlProcess,args=(pin,self.ledQ))
        self.theProcess.start()
        
    def ledControlProcess(self,pin,queue):
        """This is the process spawned off to actually blink the LED"""
        myLEDControl=LedControl(pin,True)
        current_state="OFF"
        prev_state="OFF"
        interval=0

        while (current_state != "QUIT"):
            try:
                current_state=queue.get(False)
            except Queue.Empty:
                pass
            if(current_state == "BLINK") and (prev_state == "BLINK"):
                time.sleep(interval)
                myLEDControl.on()
                time.sleep(interval)
                myLEDControl.off()
            if(current_state != prev_state):
                if (current_state == "ON"):
                    myLEDControl.on()
                    prev_state=current_state
                elif(current_state == "OFF"):
                    myLEDControl.off()
                    prev_state=current_state
                elif re.match("^BLINK",current_state):
                    interval=int(re.search("[0-9]+$",current_state).group(0))
                    current_state="BLINK"
                    prev_state=current_state
                    
        myLEDControl.cleanup()

    def on(self):
        """Turn LED ON"""
        self.ledQ.put("ON")

    def off(self):
        """Turn LED OFF"""
        self.ledQ.put("OFF")

    def blink(self,interval):
        """Blink LED at interval"""
        message="BLINK %d" % (interval)
        self.ledQ.put(message)

    def quit(self):
        """Shut LED down gracefully"""
        self.ledQ.put("QUIT")
    

        
if __name__ == "__main__":
    import sys
    
    # Test code
    myLEDBlinker=ledBlinker(11)
    myLEDBlinker.on()
    print("LED should be ON -- press enter")
    sys.stdin.readline()
    myLEDBlinker.off()
    print("LED should be OFF -- press enter")
    sys.stdin.readline()
    myLEDBlinker.blink(1)
    print("LED should be BLINKING at 1 sec -- press enter")
    sys.stdin.readline()
    myLEDBlinker.blink(3)
    print("LED should be BLINKING at 3 sec -- press enter")
    sys.stdin.readline()
    myLEDBlinker.quit()
    
