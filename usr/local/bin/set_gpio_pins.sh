#!/bin/bash
#
# Set GPIO pins to be accessible to webserver.
#  In fact, make them accessible to the web-server (www-data) and
#   the 'typical' user (pi).  The 'chmod' allows user 'pi' to write
#   Script originally from https://dissectionbydavid.wordpress.com/,
#   but modified to pass pin numbers on the command line.
#

# Set up a given pin
#
set_a_pin() {
   /usr/bin/env gpio export $1 out
   chown -R ${2}:pi /sys/class/gpio/gpio${1}
   chmod -R g+w /sys/class/gpio/gpio${1}
}

usage() {
   echo Usage: $1 -p "pin list" -g group -u user
cat <<EOU
   Make GPIO pins accessible to user user and group group.  Pin list is a 
   list of pin numbers as counted on the board (e.g. from pin 1).  The quotes 
   are mandatory if you are setting more than one pin:  
       set_gpio_pins.sh -p "11 12 14 18"
   Group and user default to www-data.
EOU
}

# Main Line
GROUP=www-data
USER=www-data

OPTSTRING="p:hg:u:"
while getopts ${OPTSTRING} O 
do
  case ${O} in 
	p)
		PIN_LIST=${OPTARG}
	 	;;
	g)	GROUP=${OPTARG}
		;;
	u)	USER=${OPTARG}
		;;
	h)
		usage $0
		exit 1
		;;
	*)
		usage $0
		exit 2
		;;
  esac
done
shift $((OPTIND-1))

if [ ${PIN_LIST:-NULL} = "NULL" ]
then
	usage $0
 	exit 1   
fi	

for pin in ${PIN_LIST}; do
   set_a_pin ${pin} $USER
done

# Karl's solution, slightly modified
chown root:${GROUP} /dev/gpiomem
chmod g+rw /dev/gpiomem
