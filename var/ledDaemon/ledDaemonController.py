#!/usr/bin/python

#############################
#
#  Send messages to ledDaemon.py
#
############################
import sysv_ipc as IPC
import ConfigParser as CFP
import sys

configSection="ledDaemon"
configFile="./ledDaemon.cfg"
shmsize=20


#Main Line
myConfig=CFP.SafeConfigParser()
myConfig.read(configFile)
shmkeynum = myConfig.getint(configSection,"shmKeyNum")
shmsize = myConfig.getint(configSection,"shmSize")
try:
   mySHM=IPC.SharedMemory(shmkeynum,flags=0,size=0)
   mySHM.attach()
except Exception as e:
    print("Cannot grab shared memory: %s" % str(e))
    
mySHM.write(' ' * shmsize)    
mySHM.write(sys.argv[1])
foo=mySHM.read()
print foo
