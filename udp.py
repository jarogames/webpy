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

ojr@zotac:~$ echo BEAM_ON_ | nc -u -w 1  localhost 10050 
ojr@zotac:~$ echo BEAM_OFF | nc -u -w 1  localhost 10050 
ojr@zotac:~$ echo BEAM_ON_ | nc -u -w 1  localhost 10050 
ojr@zotac:~$ echo BEAM_OFF | nc -u -w 1  localhost 10050 
ojr@zotac:~$ echo DET_RDY_ | nc -u -w 1  localhost 10050 
ojr@zotac:~$ echo DET_NRDY | nc -u -w 1  localhost 10050

'''
from socket import *
import datetime
import threading  # to measure beamtime
import time
import os.path


import mmap
import contextlib
import time

CONTROLFILE=".mmap.1.vme"
CONTROLFILE=".mmap.4.counter"

#        Vadim UDP will run beam counter
#                  and  vme run start
#   PUT GREGORY_CNT INTO myservice script!
#    
#
gregoryCNT_DIR=os.environ.get('GREGORY_CNT')
if gregoryCNT_DIR!=None:
    print("+... GREGORY_CNT directory detected",gregoryCNT_DIR)
    gregoryCNT_DIR=gregoryCNT_DIR+"/"
else:
    print("x...       GREGORY_CNT dir NOT defined")
    #os.chdir( os.environ['GREGORY'] )
    gregoryCNT_DIR=""
mmapfileCNT=gregoryCNT_DIR+CONTROLFILE
#runnextfileCNT=gregoryCNT_DIR+"RUNNEXT"
print("i...CNT mmap file:", mmapfileCNT)
#print("i... RUNNEXT file:", runnextfileCNT)

gregoryVME_DIR=os.environ.get('GREGORY_VME')
if gregoryVME_DIR!=None:
    print("+... GREGORY_VME directory detected",gregoryVME_DIR)
    gregoryVME_DIR=gregoryVME_DIR+"/"
else:
    print("x...       GREGORY_VME dir NOT defined")
    #os.chdir( os.environ['GREGORY'] )
    gregoryVME_DIR=""
mmapfileVME=gregoryVME_DIR+CONTROLFILE
runnextfileVME=gregoryVME_DIR+"RUNNEXT"
print("i...VME mmap file:", mmapfileVME)
print("i... RUNNEXT file:", runnextfileVME)


deteonfile="deteon"
beamonfile="beamon"
logfile="log.log"

with open(deteonfile,"w") as f:
    f.write( "-" )
with open(beamonfile,"w") as f:
    f.write( "-" )


def getMM_CNT():
    mm_first_run=0
    print('?... trying to open ',mmapfileCNT,'......')
    if os.path.isfile( mmapfileCNT ):
        print('+... file',mmapfileCNT,'was detected')
        with open(mmapfileCNT, "r+b") as f:
            mm1 = mmap.mmap(f.fileno(), 0)# memory-map the file,size 0= whole
            qqqqq= mm1.readline()
            print("w...   MMAP : start/stop commands will be transmitted")
        return mm1
    else:
        print("x... NO ", mmapfileCNT)
        return 0
    
def getMM_VME():
    mm_first_run=0
    print('?... trying to open ',mmapfileVME,'......')
    if os.path.isfile( mmapfileVME ):
        print('+... file',mmapfileVME,'was detected')
        with open(mmapfileVME, "r+b") as f:
            mm1 = mmap.mmap(f.fileno(), 0)# memory-map the file,size 0= whole
            qqqqq= mm1.readline()
            print("w...   MMAP : start/stop commands will be transmitted")
        return mm1
    else:
        print("x... NO ", mmapfileVME)
        return 0

mmxCNT=getMM_CNT()    # HERE I OPEN FILE CNT
if mmxCNT!=0:mmxCNT.seek(0)
mmxVME=0
if gregoryVME_DIR!="":
    mmxVME=getMM_VME()    # HERE I OPEN FILE VME
    if mmxVME!=0:mmxVME.seek(0)
else:
    print("x... NO mmap FOR VME - NO vme start/stop")
    time.sleep(2)
    mmxVME=0
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
        with open(beamonfile,"w") as f:
            f.write( txt )
        time.sleep(1)
        txt=delta(btstart)
    print("beamtime ending")
    with open(beamonfile,"w") as f:
        f.write("-")
    with open(logfile,"a") as f:
        f.write(datetime.datetime.now().strftime("%H:%M:%S")+"  BEAM="+lastx+"\n")
    return

def detetime():
    global dtstart
    lastx=""
    txt=delta(dtstart)
    while "-" not in txt:
        lastx=txt
        print("DETE_ON",txt)
        with open(deteonfile,"w") as f:
            f.write( txt )
        time.sleep(1)
        txt=delta(dtstart)
    print("detector ending")
    with open(deteonfile,"w") as f:
        f.write( "-" )
    with open(logfile,"a") as f:
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
    #line=da2+" {:04d} ".format(i)+" "+data.decode("utf8").rstrip()
    line=da2+" "+data.decode("utf8").rstrip()
    with open(logfile,"a") as f:
        f.write( line+"\n" )
    print( line )
    if "BEAM_ON" in line:
        btstart=datetime.datetime.now()
        tbeam=threading.Thread( target=beamtime)
        tbeam.start()
        if mmxCNT!=0:
            mmxCNT[0:5]=b'start'
        else:
            print(CONTROLFILE," cannot be operated")
    if "BEAM_OFF" in line:
        btstart=beginme+datetime.timedelta(days=999.1)
        if mmxCNT!=0:
            mmxCNT[0:4]=b'stop'
        else:
            print(CONTROLFILE," cannot be operated")
    if "DET_RDY" in line:
        dtstart=datetime.datetime.now()
        tdete=threading.Thread( target=detetime)
        tdete.start()
        if mmxVME!=0:
            mmxVME[0:5]=b'start'
        else:
            print(CONTROLFILE," for VME cannot be operated")
    if "DET_NRDY" in line:
        dtstart=beginme+datetime.timedelta(days=999.1)
        if mmxVME!=0:
            mmxVME[0:4]=b'stop'
        else:
            print(CONTROLFILE, " for VME cannot be operated")
        
