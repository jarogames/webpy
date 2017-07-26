#!/usr/bin/python3
from socket import *
import datetime
IPv4 = ""
Port = 10050

ServerSock = socket(AF_INET, SOCK_DGRAM) # UDP
ServerSock.bind((IPv4, Port))
print("Socket is ready to receive data..")

i=0
while True:
    data, addr = ServerSock.recvfrom(1024) # buffer size is 1024 bytes
    i=i+1
    da=datetime.datetime.now()
    da2=da.strftime("%H:%M:%S")
    line=da2+"{:6d}".format(i)+" "+data.decode("utf8").rstrip()
    with open("log.log","a") as f:
        f.write( line )
    print( line )
