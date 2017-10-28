#!/usr/bin/python3
####################
# JUST ping port 12001
#    zmq   PUB socket
#      to server_log.py
####################
import zmq
import random
import sys
import time
import json
from random import randint

import datetime
import os
port = "12001"

##############################
#   I want GREGORY  dir
#
#    then -  tail -f :
#https://stackoverflow.com/questions/5419888/reading-from-a-frequently-updated-file

def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

LFILENAME="/gregory_run.log"
if __name__ == '__main__': 
##### GREGORY DIR  ======================
    gregorydir=os.environ.get('GREGORY')
    if gregorydir!=None:
        print("+... going to GREGORY directory")
        #os.chdir( os.environ['GREGORY'] )
    else:
        print('x... GREGORY path NOT defined')
        gregorydir="."
##### LOG FILE ====================
    LFILENAME=gregorydir+"/gregory_run.log"
    print( LFILENAME )
    logfile = open( LFILENAME  , "r")
    loglines = follow(logfile)
##### connect ==================
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%s" % port)
    time.sleep(0.5)
    for line in loglines:
        line=line.rstrip()
        mark=datetime.datetime.now().strftime("%H:%M:%S")
        message=json.dumps({'time':mark,'random':randint(0,999999),'line':line})
        print( "sending:" ,line )
        socket.send_string( line )


