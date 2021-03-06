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
from random import randint   #  to really reload pictures
import time
from shutil import copyfile  # COPY FROM TO dir (not best solution)
import os,sys

HTTP_PORT = 25102
ZMQ_LISTENING_PORT = HTTP_PORT+1000

monkey.patch_all()  # for ZMQ

app = Flask(__name__) #app = Flask(__name__, static_url_path = "/tmp", static_folder = "tmp" ) 
app.config['DEBUG'] =  True  # DO NOT USE IN PRODUCTION  !!!!!!!!!!!!

logging.basicConfig(level=logging.INFO)  # INFO / DEBUG
logger = logging.getLogger(__name__)

sockets = Sockets(app)  # ZMQ PREPARATION
context = zmq.Context()  


##################################################
#  THESE TWO ARE NEEDED FOR AUTORELOAD 
#

@app.before_request
def before_every_request():
    logger.info("before request")
       
@app.after_request## No caching at all for API endpoints.
def add_header(response):
    logger.info('add header after request')
    response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


########################################
#              MAIN PAGE 
@app.route('/')
def index():   # gets from ./templates/
    logger.info('Rendering index page')
    return render_template('index.html')


################## this works for autoreload
#
@sockets.route('/send_data')   # AUTONOMOUS 
def send_data(ws):
    seconds=0.1
    logger.info('Got a websocket connection log ... send_data; reload every '+str(seconds)+' sec.')
    gevent.sleep()
    received = 0
    while True:
        received += 1
        MESSAGE=[]
        files=[ 'counters.jpg', 'streampic_00.jpg']
        print("i... in the loop before rand")
        data=[]
        j=0
        for i in range(10):
            rand=randint(0,9)
            data.append( [j,rand] )
            j=j+1
        #MESSAGE.append( "ahoj" )
        #MESSAGE="ahoj"
        ws.send(  json.dumps(data) )
        logger.info( json.dumps(data)  )
        time.sleep( seconds )
        gevent.sleep()
        ######################

        
###########################
#  READ and SEND  IMAGE
@app.route("/static/<path:path>")
def images(path):
    logger.info('image:')
    generate_img(path)
    fullpath = "./static/" + path
    resp = flask.make_response( open(fullpath).read() )
    resp.content_type = "image/jpeg"
    return resp




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
    
