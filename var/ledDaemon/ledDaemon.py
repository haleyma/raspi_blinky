#! /usr/bin/python
#####################################################
#
# Daemon to control LED.  Allows transient programs to make it blink.
#
#
# Read shared memory segment for current states:
# "ON" = LED is on
# "OFF" = LED is off
# "BLINK" = LED is blinking
# "BLINK 99" = LED blinks at 99 second interval
#
#  Reads ledDaemon.cfg for configuration values.
#
# Copyright (c) Charles Shapiro Feb 2018
#
# This file is part of ledDaemon.
#    ledDaemon is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#    ledDaemon is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    You should have received a copy of the GNU General Public License
#    along with ledDaemon.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################
import sysv_ipc as IPC
import time
from ledController import LedControl
import ConfigParser as CFP
import re

configSection="ledDaemon"
configFile="./ledDaemon.cfg"
shmSize=20
Verbose=False


## Just compile once, for efficiency.  Used only in findState.
quit = re.compile("^QUIT")
blink=re.compile("^BLINK")
blinkNum=re.compile("[0123456789]+$")
on=re.compile("^ON")
off=re.compile("^OFF")

DefaultBlinkTime=2

def blankSHM(shmHandle) :
   shmHandle.write(' ' * shmSize)
   return

def findState(theStr):
    retVal="OFF"
    theStr = theStr.strip()
    theblinktime=0
    if blink.match(theStr):
      theblinktime=DefaultBlinkTime
      bnFound = blinkNum.search(theStr)
      if(bnFound):
         theblinktime=int(bnFound.group(0))
      if(Verbose):
         print("theStr: [%s]; theblinktime: %d" % (theStr,theblinktime))
      retVal="BLINK"
    if(on.match(theStr)):
       retVal = ("ON")
    if(off.match(theStr)):
       retVal="OFF"
    if(quit.match(theStr)):
       retVal = "QUIT"
    return (retVal,theblinktime)

#Main Line

myConfig=CFP.SafeConfigParser()
myConfig.read(configFile)
shmkeynum= myConfig.getint(configSection,"shmKeyNum")
pinNumber=myConfig.getint(configSection,"pinNumber")
shmsize=myConfig.getint(configSection,"shmSize")
if True == myConfig.has_option(configSection,"verbose"):
   Verbose = True
DefaultBlinkTime=myConfig.getint(configSection,"blinkTime")
theLed=LedControl(pinNumber,True)
CurrentState="OFF"
blinkTime=DefaultBlinkTime

# Kill any shm hanging around from previous abended runs.  
try:
   mySHM=IPC.SharedMemory(shmkeynum,flags=0)
   mySHM.detach()
   mySHM.remove()
except IPC.ExistentialError:
   pass

mySHM = None
try:
   mySHM=IPC.SharedMemory(shmkeynum,flags=IPC.IPC_CREAT | IPC.IPC_EXCL,size=shmSize,init_character=' ',mode=0666)
   mySHM.attach()
except Exception as e:
   print("Cannot grab shared memory: %s" % str(e))
   mySHM.destroy()


blankSHM(mySHM)

shmStr=mySHM.read()
while CurrentState != "QUIT":
    shmStr=mySHM.read()
    if (shmStr[0] != ' ' ) and (Verbose is True):
       print(shmStr)
    prevState=CurrentState
    (CurrentState,blinkTime) = findState(shmStr)
#    blankSHM(mySHM)
    if ("ON" == CurrentState) and (prevState != "ON"):
       theLed.on()
    if("OFF" == CurrentState) and (prevState != "OFF"):
       theLed.off()
    if("BLINK" == CurrentState):
       if(Verbose):
          print("Sleeping %d" % (blinkTime))
       time.sleep(blinkTime)
       theLed.on()
       time.sleep(blinkTime)
       theLed.off()
       
theLed.cleanup()
mySHM.detach()
mySHM.remove()
    
