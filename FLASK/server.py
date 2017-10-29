#!/usr/bin/python3
##############################
#  FALSK SERVER  port 25000
#  zmq   port 12000
#  sending data from 12000 to 25000
##############################
import zmq.green as zmq
import json
import gevent
from flask_sockets import Sockets
from flask import Flask, render_template
import logging
from gevent import monkey

monkey.patch_all()

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sockets = Sockets(app)
context = zmq.Context()
HTML_PORT=24999
ZMQ_LISTENING_PORT = 11999

@app.route('/')
def index():
    logger.info('Rendering index page')
    return render_template('index.html')

@sockets.route('/zeromq')
def send_data(ws):
    logger.info('Got a websocket connection, sending up data from zmq')
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
        logger.info(str(received)+str(data))
        ws.send(json.dumps(data))
        gevent.sleep()

if __name__ == '__main__':
    logger.info('Launching web server')
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', HTML_PORT), app, handler_class=WebSocketHandler)
    logger.info('Starting serving')
    server.serve_forever()
    
