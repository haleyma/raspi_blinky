#!/usr/bin/python
#
# Send messages to the led controller daemon from CGI.
#

import cgi
import cgitb
import shutil
import os.path
import sysv_ipc as IPC
import ConfigParser as CFP

from ledController import LedControl

configFile="ledDaemon.cfg"
configSection="ledDaemon"

on_file="/var/www/html/images/ON.png"
off_file="/var/www/html/images/OFF.png"

current_file="/var/www/html/images/current.png"
status_fdir="/var/www/html/images/blinkpictures"
SUCCESS=True

# Main Line


cgitb.enable()  # Allow error reporting to browser
myForm=cgi.FieldStorage()

ledCtrl=myForm["ledctrl"].value
blinkTime=myForm["blinktime"].value

myConfig=CFP.SafeConfigParser()
myConfig.read(configFile)
shmkeynum=myConfig.getint(configSection,"shmKeyNum")

ctrlStr=""

if ledCtrl == "off":
    ctrlStr="OFF"
    inStatusFN=off_file
elif ledCtrl == "ON":
    ctrlStr="ON"
    inStatusFN=on_file 
elif ledCtrl == "Blink":
    ctrlStr="BLINK " + blinkTime
    inStatusFN=os.path.join(status_fdir,"blink"+blinkTime+".png")


    
shmsize = myConfig.getint(configSection,"shmSize")
try:
   mySHM=IPC.SharedMemory(shmkeynum,flags=0,size=0)
   mySHM.attach()
except Exception as e:
    print("<h1>Oops. Cannot find shared memory: %s<h1><br/>You sure that daemon is running?" % str(e))
    SUCCESS=False


if SUCCESS is True:    
   mySHM.write(' ' * shmsize)    
   mySHM.write(ctrlStr)
   shutil.copyfile(inStatusFN,current_file)
   
# cgi.test()

print("<h1>Your Wish is My command</h1>")
print('<a href="/daemon_index.html">More Commands</a>')

print('</html>')
    




