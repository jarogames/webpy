#!/usr/bin/python3
#  - chrome   Ctrl-F5 to refresh the cache
#    https://www.tutorialspoint.com/flask/flask_templates.htm
import zmq.green as zmq
import json
import gevent
from flask_sockets import Sockets
from flask import Flask, render_template
import logging
from gevent import monkey
#-------------------------- basic for the server
from random import randint
import time
from shutil import copyfile  # COPY FROM TO dir (not best solution)
import os,sys

HTTP_PORT = 25100
ZMQ_LISTENING_PORT = HTTP_PORT+1000

monkey.patch_all()  # for ZMQ

app = Flask(__name__) #app = Flask(__name__, static_url_path = "/tmp", static_folder = "tmp" ) 

logging.basicConfig(level=logging.INFO)  # INFO / DEBUG
logger = logging.getLogger(__name__)

sockets = Sockets(app)  # ZMQ PREPARATION
context = zmq.Context()  


@app.route('/')
def index():   # gets from ./templates/
    logger.info('Rendering index page')
    return render_template('index.html')

###############################################################
#
#  M A I N                 FLASK_DEBUG=1 ./server.py        
#
##############################################################
if __name__ == '__main__':
    logger.info("===================================================")
    logger.info('Launching web server;  port='+str(HTTP_PORT)+' zmq_port='+str(ZMQ_LISTENING_PORT) )
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', HTTP_PORT), app, handler_class=WebSocketHandler)
    server.serve_forever()
    
