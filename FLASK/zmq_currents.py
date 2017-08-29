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
port = "12002"

##############################
#   I want to read MySQL and fetch data with zmq
#
#

def getdif( nowserver, aa):
    t1=datetime.datetime.strptime(nowserver,"%H:%M:%S")
    t2=datetime.datetime.strptime(aa       ,"%H:%M:%S")
    dt=(t1-t2).total_seconds()   # earlier it was recorded to mysql
    if dt>=0. and dt<1.:return "palegreen"
    if dt>=1. and dt<2.:return "greenyellow"
    if dt>=2. and dt<3.:return "chartreuse"
    if dt>=3. and dt<4.:return "lime"
    if dt>=4. and dt<6.:return "springgreen"
    if dt>=6. and dt<8.:return "lightsalmon"
    if dt>=8. and dt<10.:return "coral"
    if dt>=10. and dt<12.:return "tomato"
    if dt>=12. and dt<14.:return "orangered"
    if dt>=14. and dt<16.:return "salmon"
    if dt>=16. and dt<18.:return "indianred"
    return "red"
    

if __name__ == '__main__': 
##### GREGORY DIR  ======================
    gregorydir=os.environ.get('GREGORY')
    if gregorydir!=None:
        print("+... going to GREGORY directory")
        #os.chdir( os.environ['GREGORY'] )
    else:
        print('x... GREGORY path NOT defined')
        gregorydir="."
##### connect ==================
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%s" % port)
    time.sleep(0.5)
    while(1):
        NOW=datetime.datetime.now()
        mark=NOW.strftime("%H:%M:%S")
        markclona=(NOW-datetime.timedelta(0,1)).strftime("%H:%M:%S")
        markdegrader=(NOW-datetime.timedelta(0,2)).strftime("%H:%M:%S")
        markfaraday=(NOW-datetime.timedelta(0,3)).strftime("%H:%M:%S")

        line="-"
        beamcolor="white"
        clonacolor=getdif( mark, markclona )
        degradercolor=getdif( mark, markdegrader )
        faradaycolor=getdif( mark, markfaraday )
        message=json.dumps({'time':mark,
                            'clona':randint(0,100),
                            'degrader':randint(0,100),
                            'electrode':randint(0,100),
                            'faraday':randint(0,100),
                            'line':line,
                            'clonatime': markclona ,
                            'degradertime': markdegrader ,
                            'electrodetime': mark ,
                            'faradaytime': markfaraday ,
                            'clonacolor':clonacolor,
                            'degradercolor':degradercolor,
                            'electrodecolor':beamcolor,
                            'faradaycolor':faradaycolor,
                            'log':["beam ON 1:00","beam OFF 3:2:1","dete ON 1:2:3"],
        })
        print( "sending:" ,message )
        socket.send_string( message )
        time.sleep(0.5)

