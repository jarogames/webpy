#!/usr/bin/python3
'''
 this program waits to UDP packet from VADIM
 - appends it to the log.log file
 - when it sees BEAM_START  starts a web counter
 - when it sees BEAM_STOP   stops a web counter
 - it writes start stop into
    .mmap.1.vme file in $GREGORY
    that drives serial_master.py
   !!! WARNING
   it cannot be the same as VME-GREGORY

ojr@zotac:~$ echo BEAM_ON | nc -u -w 1  localhost 10050 
ojr@zotac:~$ echo BEAM_OFF | nc -u -w 1  localhost 10050 
ojr@zotac:~$ echo BEAM_ON | nc -u -w 1  localhost 10050 
ojr@zotac:~$ echo BEAM_OFF | nc -u -w 1  localhost 10050 
ojr@zotac:~$ echo DET_READY | nc -u -w 1  localhost 10050 
ojr@zotac:~$ echo DET_NOT_READY | nc -u -w 1  localhost 10050

'''
from socket import *
import datetime
import threading  # to measure beamtime
import time
import os.path


import mmap
import contextlib
import time

gregoryDIR=os.environ.get('GREGORY')
if gregoryDIR!=None:
    print("+... GREGORY directory detected",gregoryDIR)
    gregoryDIR=gregoryDIR+"/"
else:
    print("x...       GREGORY dir NOT defined")
    #os.chdir( os.environ['GREGORY'] )
    gregoryDIR=""
mmapfile=gregoryDIR+".mmap.1.vme"
runnextfile=gregoryDIR+"RUNNEXT"
print("i...    mmap file:", mmapfile)
print("i... RUNNEXT file:", runnextfile)


def getMM():
    mm_first_run=0
    print('?... trying to open ',mmapfile,'......')
    if os.path.isfile( mmapfile ):
        print('+... file',mmapfile,'was detected')
        with open(mmapfile, "r+b") as f:
            mm1 = mmap.mmap(f.fileno(), 0)# memory-map the file,size 0= whole
            qqqqq= mm1.readline()
            print("w...   MMAP : start/stop commands will be transmitted")
        return mm1
    else:
        print("x... NO ", mmapfile)
        return 0
mmx=getMM()    # HERE I OPEN FILE
if mmx!=0:mmx.seek(0)
#quit()


beginme=datetime.datetime.now()  # not used

def delta(initime):
    dt=(datetime.datetime.now()-initime).total_seconds()
    txt= str(datetime.timedelta( seconds=round(dt) ) ) 
    return txt

def beamtime():
    global btstart
    lastx=""
    txt=delta(btstart)
    while "-" not in txt:
        lastx=txt
        print("BEAM_ON",txt)
        with open('beamon',"w") as f:
            f.write( txt )
        time.sleep(1)
        txt=delta(btstart)
    print("beamtime ending")
    with open('beamon',"w") as f:
        f.write("-")
    with open('log.log',"a") as f:
        f.write(datetime.datetime.now().strftime("%H:%M:%S")+"  BEAM="+lastx+"\n")
    return

def detetime():
    global dtstart
    lastx=""
    txt=delta(dtstart)
    while "-" not in txt:
        lastx=txt
        print("DETE_ON",txt)
        with open('deteon',"w") as f:
            f.write( txt )
        time.sleep(1)
        txt=delta(dtstart)
    print("detector ending")
    with open('deteon',"w") as f:
        f.write( "-" )
    with open('log.log',"a") as f:
        f.write(datetime.datetime.now().strftime("%H:%M:%S")+"  DETE="+lastx+"\n")
    return



IPv4 = ""
Port = 10050

ServerSock = socket(AF_INET, SOCK_DGRAM) # UDP
ServerSock.bind((IPv4, Port))
print("Socket is ready to receive data..")

i=0
while True:
    data, addr = ServerSock.recvfrom(1024) # buffer size is 1024 bytes
    i=i+1
    da2=datetime.datetime.now().strftime("%H:%M:%S")
    #da2=da.strftime("%H:%M:%S")
    line=da2+" {:04d} ".format(i)+" "+data.decode("utf8").rstrip()
    with open("log.log","a") as f:
        f.write( line+"\n" )
    print( line )
    if "BEAM_ON" in line:
        btstart=datetime.datetime.now()
        tbeam=threading.Thread( target=beamtime)
        tbeam.start()
        if mmx!=0:
            mmx[0:5]=b'start'
        else:
            print(".mmap.1.vme cannot be operated")
    if "BEAM_OFF" in line:
        btstart=beginme+datetime.timedelta(days=0.1)
        if mmx!=0:
            mmx[0:4]=b'stop'
        else:
            print(".mmap.1.vme cannot be operated")
    if "DET_READY" in line:
        dtstart=datetime.datetime.now()
        tdete=threading.Thread( target=detetime)
        tdete.start()
    if "DET_NOT_READY" in line:
        dtstart=beginme+datetime.timedelta(days=0.1)
        
