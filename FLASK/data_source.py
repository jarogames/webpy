#!/usr/bin/python3
import zmq
import random
import sys
import time
import json
from random import randint

import datetime

port = "12000"

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % port)
time.sleep(0.5)
while True:
    mark=datetime.datetime.now().strftime("%H:%M:%S")
#    first_data_element = random.randrange(2,20)
#    second_data_element = random.randrange(0,360)
#    message = json.dumps({'First Data':first_data_element, 'Second Data':second_data_element,'time':mark})
    message = json.dumps({'time':mark,'random':randint(0,999999) })
    print(message)
    socket.send_string(message)
    for i in range(100):
        time.sleep(0.5)
        print(i," ",end="", flush=True)
    print("")
    
