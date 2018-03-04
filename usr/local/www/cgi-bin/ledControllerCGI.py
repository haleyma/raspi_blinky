#!/usr/bin/python
#
# Control an LED over CGI
#

import cgi
from ledController import LedControl
import cgitb
import shutil
import os.path

on_file="/var/www/html/images/ON.png"
off_file="/var/www/html/images/OFF.png"
current_file="/var/www/html/images/current.png"

current_file_url="images/current.png"

# Main Line
cgitb.enable()  # Allow error reporting to browser

myForm = cgi.FieldStorage()

ledPin=int(myForm["pin"].value)

myLED = LedControl(ledPin,False)


if myForm["radio_onoff"].value == "ON":
    shutil.copyfile(on_file,current_file)
    myLED.on()
else:
    shutil.copyfile(off_file,current_file)
    myLED.off()
    
print("<h1>Your Wish is My command</h1>")
print('<a href="/index.html">More Commands</a>')

print('</html>')
    


# cgi.test()

