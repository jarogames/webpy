#!/usr/bin/python3
##################################
#
#  FLASK WEBSITE   port 25001
#      just sending data from zmq
#     zmq 12001 
##################################
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

HTML_PORT=25001
ZMQ_LISTENING_PORT = 12001 # send log after push

@app.route('/')
def index():
    logger.info('Rendering index page')
    return render_template('log.html')

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
        #data = socket.recv_json()
        recvd=socket.recv().decode("utf8").rstrip()
        print("zeromq ", recvd)
        data.insert(0, recvd )
        if len(data)>28:
            data.pop()
        #print("zeromqlog --- ", data )
        #logger.info( str(received) + str(data) )
        #ws.send(json.dumps(data))
        #  courier.html has {{text|safe}}
        mustr=render_template( "courier.html", text="<br>\n".join( data ) )
        print(mustr)
        ws.send( mustr )
        gevent.sleep()

if __name__ == '__main__':
    logger.info('Launching web server on '+str(HTML_PORT))
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server=pywsgi.WSGIServer(('',HTML_PORT),app,handler_class=WebSocketHandler)
    logger.info('Starting serving')
    server.serve_forever()
    
