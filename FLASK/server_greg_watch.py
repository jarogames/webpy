#!/usr/bin/python3
##################################
#
#  FLASK WEBSITE   port 25005
#      ACTUAL GREGORY SITUATION
#     zmq 12005
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
app.config['DEBUG'] = True
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sockets = Sockets(app)
context = zmq.Context()


HTML_PORT=25005
ZMQ_LISTENING_PORT = 12005 # 


@app.route('/')
def index():
    logger.info('Rendering index page')
    return render_template('currents.html')

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
        print("zeromqlog --- ", data )
        
        #recvd=socket.recv().decode("utf8").rstrip() # from c++ only num
        #recvd=socket.recv().decode("utf8") # from c++ only num
        #print("zeromq received: /{}/".format( recvd)  )
        
        #data.insert(0, recvd )
        #if len(data)>28:
        #    data.pop()
        #logger.info( str(received) + str(data) )
        #  courier.html has {{text|safe}}
        #mustr=render_template( "currents_table.html", data=data )
        ####print(mustr)
        #ws.send( recvd )

        for v,chan in data.items():
            #print(v)
            if v!='time':
                if int( chan['Rate'])>1.0:
                    data[ str(v) ]['Rcolor']='lightsalmon'
                if int( chan['Rate'])>2.0:
                    data[ str(v) ]['Rcolor']='coral'
                if int( chan['Rate'])>3.0:
                    data[ str(v) ]['Rcolor']='tomato'
                if int( chan['Rate'])>4.0:
                    data[ str(v) ]['Rcolor']='orangered'
                if int( chan['Rate'])>4.0:
                    data[ str(v) ]['Rcolor']='salmon'
                if int( chan['Rate'])>5.0:
                    data[ str(v) ]['Rcolor']='indianred'
                #-----------------------------------
                if int( chan['PileUp'])>1.0:
                    data[ str(v) ]['Pcolor']='lightsalmon'
                if int( chan['PileUp'])>2.0:
                    data[ str(v) ]['Pcolor']='coral'
                if int( chan['PileUp'])>3.0:
                    data[ str(v) ]['Pcolor']='tomato'
                if int( chan['PileUp'])>4.0:
                    data[ str(v) ]['Pcolor']='orangered'
                if int( chan['PileUp'])>4.0:
                    data[ str(v) ]['Pcolor']='salmon'
                if int( chan['PileUp'])>5.0:
                    data[ str(v) ]['Pcolor']='indianred'
        #d = json.loads( data )
        #d['time'] = 'green'
        #d['2']['Pcolor'] = 'red'
        #data.set_data(json.dumps(d))
        
        mustr=render_template( "gregory_run.html", data=data )
        ws.send( mustr )
        gevent.sleep()

if __name__ == '__main__':
    logger.info('Launching web server on '+str(HTML_PORT)+" zmq on 12005")
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server=pywsgi.WSGIServer(('',HTML_PORT),app,handler_class=WebSocketHandler)
    logger.info('Starting serving')
    server.serve_forever()
    
