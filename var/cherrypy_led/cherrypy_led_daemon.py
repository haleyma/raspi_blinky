#! /usr/bin/python
###################################################
# A daemon to control an LED from your browser, using the
# cherrypy web framework.
#
# Copyright (c) Charles Shapiro March 2018
#
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
###################################################


import cherrypy
import ledBlinker
import signal
import os
import re

class LEDCtrl(object):
    """The thing exposed to the web"""
    
    def sigUsr2Handler(signal,frame):
        """Handle sigusr2 from forked process"""
        self.the_led.cleanup()
        sys.exit(0)
    
    def __init__(self):
        """Initialize some important variables"""
        super(LEDCtrl,self).__init__()
        self.the_led=ledBlinker.ledBlinker(11)
        self.LEDStatus="OFF"
        
    @cherrypy.expose
    def index(self):
        """Put up the default web page."""
        return(""" <html>
        <head><title>Cherrypy LED Server</title></head>
        <body>
        <h1>Cherrypy LED Server</h1>
        <form method="get" action="doControl">
  <input type="radio" value="ON" name="ledctrl">Turn LED ON</input><br/>
  <input type="radio" value="off" name="ledctrl" checked>Turn LED off</input><br/>
  <input type="radio" value="Blink" name="ledctrl">Blink LED</input><br/>
  <h2>Select Blink Time</h2>
  <select name="blinktime">
    <option value="1" selected>1</option>
    <option value="2">2</option>
    <option value="3">3</option>
    <option value="4">4</option>
    <option value="5">5</option>
    <option value="6">6</option>
    <option value="7">7</option>
    <option value="8">8</option>
    <option value="9">9</option>

    <option value="10">10</option>
    <option value="11">11</option>
    <option value="12">12</option>
    <option value="13">13</option>
    <option value="14">14</option>
    <option value="15">15</option>
    <option value="16">16</option>
    <option value="17">17</option>
    <option value="18">18</option>
    <option value="19">19</option>
    <option value="20">20</option>
    <option value="21">21</option>
    <option value="22">22</option>
    <option value="23">23</option>
    <option value="24">24</option>
    <option value="25">25</option>
    <option value="26">26</option>
    <option value="27">27</option>
    <option value="28">28</option>
    <option value="29">29</option>
    <option value="30">30</option>
  </select><br/>
  <center><input type="submit" value="Go!"/></center>
  </form>
  <br/>
   <h2>LED is currently <b>%s</b></h2>
        """ % (self.LEDStatus) )

    @cherrypy.expose
    def doControl(self,ledctrl="off",blinktime="1"):
       """Respond to form in index()"""
       self.led_control(ledctrl,blinktime)
       retVal="<h1>LED Set</h1> <br/>"
       if(re.search("^BLINK",self.LEDStatus)):
           retVal += "LED is BLINKING at %s" % (blinktime)
       else:
           retVal += "LED is %s" % (self.LEDStatus)
       retVal += '<center><b><br/><a href="index">Back to top</a></center></b>'
       return retVal

    def led_control(self,state,blinktime):
       """Control LED from web"""
       if state == "off":
           self.the_led.off()
           self.LEDStatus="OFF"
       elif state == "ON":
           self.the_led.on()
           self.LEDStatus="ON"
       elif state == "Blink":
           self.LEDStatus="BLINK %s" % (blinktime)
           self.the_led.blink(int(blinktime))

# Main Line from command line..    
if __name__ == "__main__":
    cherrypy.config.update({'server.socket_host' : '0.0.0.0'})
    cherrypy.config.update({'server.socket_port' : 80})
## !!! Note that this filename must be the same as the PIDFILE in 
#  the cherrypyLedDeamon control script.   Ugh.
    pidfile=open('./cherrypy_led_daemon.pid','w')
    pidfile.write("%d" % (os.getpid()) )
    pidfile.close()
    
    cherrypy.quickstart(LEDCtrl())
