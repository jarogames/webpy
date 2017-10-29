#!/usr/bin/python3
##################################
#
#  FLASK WEBSITE   port 250xx
#     zmq 120xx
#
#   this shows a static page templates                _main.html
#   and  it runs  a dynamic part  div latest_data from _run.html
#
#   zmq_xxxx   will send JSON data to the ZMQ port here
#            JSON data are processed and sent to template _run.html
##################################

import zmq.green as zmq
import json
import gevent
from flask_sockets import Sockets
from flask import Flask, render_template, request
import logging
from gevent import monkey

import os
import glob
monkey.patch_all()

app = Flask(__name__)
app.config['DEBUG'] = True
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sockets = Sockets(app)
context = zmq.Context()


HTML_PORT=25006
ZMQ_LISTENING_PORT = 12006 # 

SELECTHIST=0

def getListHist(board=0):
    global SELECTHIST
    return [1,2,3,4]


@app.route('/', methods=['GET', 'POST'])
def index():
    global SELECTHIST
    logger.info('At index page')
    if request.method == 'POST':
        print("POST=====================")
        print( request )
        print( "form get 'hist'",request.form.get('hist') )
        SELECTHIST=request.form.get('hist')
    elif request.method == 'GET':
        print("GET=====================")
        #return render_template('contact.html', form=form)
    logger.info('Rendering index page')
    return render_template('shownet_main.html')



##################
#   my flask ZMQ is always SUBscribe to PUBlisher
@sockets.route('/zeromqlog')   # from application_log.js
def send_data(ws):
    logger.info('Got a websocket connection log')
    socket = context.socket(zmq.SUB)
    socket.connect('tcp://localhost:{PORT}'.format(PORT=ZMQ_LISTENING_PORT))
    socket.setsockopt_string(zmq.SUBSCRIBE, "")
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)
    gevent.sleep()
    received = 0
    data=[]
    while True:
        received += 1
        # socks = dict(poller.poll())
        # if socket in socks and socks[socket] == zmq.POLLIN:
        
        data = socket.recv_json()
        print("ZMQ DATA:", data )
        #####################################
        #   HERE I HACK json - adding Pcolr Rcolor
        
        ##################################    
        mustr=render_template( "shownet_run.html", data=data )
        print( mustr )
        ws.send( mustr )
        gevent.sleep()

if __name__ == '__main__':



    
    logger.info('Launching web server on '+str(HTML_PORT)+" zmq on "+str(ZMQ_LISTENING_PORT))
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server=pywsgi.WSGIServer(('',HTML_PORT),app,handler_class=WebSocketHandler)
    logger.info('Starting serving')
    server.serve_forever()
    
