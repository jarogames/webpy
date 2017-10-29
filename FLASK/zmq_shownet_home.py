#!/usr/bin/python3
####################
#  port 120xx
#    zmq   PUB socket
#      to server_xxxxx.py
####################
import zmq
import random
import sys
import time
import json
from random import randint

import datetime
import os

import subprocess as sp
import pprint

ZMQ_LISTENING_PORT = "12006"

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
    

def ping( server ):
    ip=server
    #ip = "192.168.0.11"
    status,result = sp.getstatusoutput("ping -c1 -w2 " + ip)
    if status == 0: 
        print("System " + ip + " is UP !")
        return "Up","palegreen"
    else:
        print("System " + ip + " is DOWN !")
        return "Down","red"

######################################
#    ALL IP  for HOME
#
#
iplist=['fedo','router','antena_local','antena_remote','gateway','eurosigdns','googledns','seznam']
ipdict={ "fedo":"192.168.0.117", "router":"192.168.0.1", "antena_local":"192.168.1.20",
         "antena_remote":"10.11.13.89" , "gateway":"10.11.13.65" ,"eurosigdns":"10.0.2.1",
         "googledns":"8.8.8.8","seznam":"www.seznam.cz"}
#  10.11.13.89   10.11.13.65


iplist2=['fedo','pib','pi3','pix2','pix3','pix1','pix4']
ipdict2={'fedo':'192.168.0.117','pib':'192.168.0.14','pi3':'192.168.0.13','pix2':'192.168.0.16',
         'pix3':'192.168.0.17','pix1':'192.168.0.15','pix4':'192.168.0.18'}

#pix1  garage
#pix2 kuchyne
#pix3 new camera
#pix4 solar

if __name__ == '__main__': 
##### connect ==================
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%s" % ZMQ_LISTENING_PORT)
    time.sleep(0.5)
    while(1):
        NOW=datetime.datetime.now()
        mark=NOW.strftime("%H:%M:%S")
        #markclona=(NOW-datetime.timedelta(0,1)).strftime("%H:%M:%S")
        #clonacolor=getdif( mark, markclona )
        myjson='{"time":"'+mark+'","pings":['
        for i in iplist:
            res,col=ping( ipdict[i] )
            #myjson=myjson+""
            # double  curly brace {{    }} to have one
            myjson=myjson+'{{"name":"{}","ip":"{}","col":"{}","status":"{}"}},'.format(i,ipdict[i],col,res)
            # json.dump({'time':mark,
            #                 'name':i,
            #                 'ip':ipdict[i],
            #                 'status':res,
            #                 'color':col,
            # })+","
            #print(myjson)
        myjson=myjson[:-1] # remove ,
        myjson=myjson+'] '
        res,col=ping( ipdict2['fedo'] )
        myjson=myjson+',"fedo":"'+col+'"'
        res,col=ping( ipdict2['pib'] )
        myjson=myjson+',"pib" :"'+col+'"'
        res,col=ping( ipdict2['pi3'] )
        myjson=myjson+',"pi3" :"'+col+'"'
        res,col=ping( ipdict2['pix1'] )
        myjson=myjson+',"pix1":"'+col+'"'
        res,col=ping( ipdict2['pix2'] )
        myjson=myjson+',"pix2":"'+col+'"'
        res,col=ping( ipdict2['pix3'] )
        myjson=myjson+',"pix3":"'+col+'"'
        res,col=ping( ipdict2['pix4'] )
        myjson=myjson+',"pix4":"'+col+'"'
        myjson=myjson+' }'
        print(myjson)
        #message=json.dumps( myjson )
        print("i... loading json")
        ###message=json.loads( myjson )
        message=myjson 
        #pprint( message )
        print( "sending:" , message )
        socket.send_string( message )
        ###socket.send( message )
        time.sleep(10)

