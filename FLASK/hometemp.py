#!/usr/bin/python3
import zmq.green as zmq
import json
import gevent
from flask_sockets import Sockets
from flask import Flask, render_template
import logging
from gevent import monkey
from random import randint
###############################
#    chrome   Ctrl-F5 to refresh
#https://www.tutorialspoint.com/flask/flask_templates.htm
###

from shutil import copyfile  # COPY FROM TMP
import os,sys

monkey.patch_all()

#app = Flask(__name__, static_url_path = "/tmp", static_folder = "tmp" ) # disk location; 'static'
app = Flask(__name__, static_folder = "static" ) # disk location; 'static'

#app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sockets = Sockets(app)
context = zmq.Context()

ZMQ_LISTENING_PORT = 12000


@app.before_request
def before_every_request():
    logger.info("before request")
       
## No caching at all for API endpoints.
@app.after_request
def add_header(response):
    logger.info('add header after request')
    response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


@app.route('/')
def index():
    logger.info('Rendering index page')
    return render_template('hometemp.html')

# this is called from JS - using reconnecting  /zeromq
## This will be renamed to 5minutes zmq
# 
@sockets.route('/zeromq5min')
def send_data(ws):
    logger.info('Got a websocket connection, sending up data from zeromq5min HOME')
    socket = context.socket(zmq.SUB)
    socket.connect('tcp://localhost:{PORT}'.format(PORT=ZMQ_LISTENING_PORT))
    socket.setsockopt_string(zmq.SUBSCRIBE, "")
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)
    gevent.sleep()
    received = 0
    while True:
        received += 1
        # socks = dict(poller.poll())
        # if socket in socks and socks[socket] == zmq.POLLIN:
        data = socket.recv_json()
        logger.info('i dont care BUT copy : '+str(received)+str(data))
        MESSAGE=[]
        files=[ 'rain.jpg', 'tempin.jpg', 'dew.jpg', 'humid.jpg', 'degrees.jpg', 'camradar.gif' ]
        rand=randint(0,999999)
        for fi in files:
            copyfile("/tmp/{}".format(fi),   "./static/{}".format(fi) )
            MSG='<img width="350px" height="300px" src="/static/{}?a={:d}">'.format( fi, rand )
            MESSAGE.append( '<div class="floated_img">'+MSG+'</div>' )
        #ws.send(json.dumps(data))
        ws.send( "\n".join(MESSAGE) )
        logger.info("\n".join(MESSAGE)  )
        gevent.sleep()
        ############################

@app.route("/static/<path:path>")
def images(path):
    logger.info('images')
    generate_img(path)
    fullpath = "./static/" + path
    resp = flask.make_response(open(fullpath).read())
    resp.content_type = "image/jpeg"
    return resp





if __name__ == '__main__':
    logger.info('Launching web server')
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 25000), app, handler_class=WebSocketHandler)
    logger.info('Starting serving')
    server.serve_forever()
    
