#!/usr/bin/python


#####################################################################
# Control an LED over CGI
#
# copyright (c) Charles Shapiro February 2018 
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
#
#####################################################################

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

