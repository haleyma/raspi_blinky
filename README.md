# raspi_blinky
## Blink an LED from your browser two different ways

### What is this About?

This code is designed to show three different ways to control an LED
attached to a Raspberry Pi from a remote browser. Two are with cgi-bin
and a web server, and one is with a stand-alone python daemon using
the [Cherry Py web framework]( http://cherrypy.org).


### Prerequisites

This project uses the current stock Python on Raspian Stretch (9.0),
which as of this writing is 2.7.13.

I used 2017-11-29-Raspbian_stretch_lite for this project, directly
from the
[Raspbian downloads
page](https://www.raspberrypi.org/downloads/raspbian/).  I assume an
already set up Raspberry Pi. You will need to install the lighttpd
package:
``` apt-get install lightttpd ```


You will also need Cherry Py 14.0.0 or better. The version in the
Stretch repository is seriously out of date, so I downloaded it from
cherrypy.org and installed from source.  Fortunately it is all-python,
so installation is not too hirsute.  I experimented with the python
pip installer but was not able to make this work.

### Making Stuff Work

#### From lightttpd

Install everything in the mirrored directories (e.g. stuff in `./etc`
goes to `/etc`). I assume that you have your LED connected to pin 11
of your RasPi.  Out of the box, you'll have to allow www-data to
connect to the GPIO pins:

```set_gpio_pins -p 11 -u www-data -g www-data```

After executing this command, connecting to the root on your Raspi
should allow you to turn the LED on and off, but not blink it.  To
blink the LED from the web server, turn on the blinker daemon in
`/var/ledDaemon`:
```
cd /var/ledDaemon
./ledDaemon start
```
You should be able to go to
`http:<yourmachine>/daemon_index.html` to get the option to blink the
LED.

You can edit /etc/rc.local to force the appropriate commands to
execute on every boot.

#### From cherry py

Make sure that lighttpd is turned off.  Then execute:
```
cd /var/cherrypy_led
./cherrypyLedDaemon start
```

Connecting to your machine should then give you a web page where you
can blink, turn on, or turn off the LED

### Where to change the LED Pin

If your LED is not connected to pin 11 of your raspberry pi, you can
change these lines to the correct pin number:

For the CGI on-off page:
```
vi /var/www/html/index.html
<input type=hidden name="pin" value="11">
```

For the Daemon on-off-blink page:
```
vi /var/ledDaemon/ledDaemon.cfg
pinNumber=11
```

For the cherrypy on-off-blink page:
```
vi /var/cherrypy_led/cherrypy_led_daemon.py
self.the_led=ledBlinker.ledBlinker(11)
```







