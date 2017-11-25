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


from random import randint
from shutil import copyfile  # COPY FROM TMP
import time

monkey.patch_all()

app = Flask(__name__)
app.config['DEBUG'] = True  # DO NOT USE IN PRODUCTION 


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sockets = Sockets(app)
context = zmq.Context()

HTTP_PORT=25006
ZMQ_LISTENING_PORT = 12006 # send log after push

############################## THIS IS EXTRA HOOMETEMP
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
########################################

@app.route('/')
def index():
    logger.info('Rendering index page')
    return render_template('aaron.html')

##################
#   my flask ZMQ is always SUBscribe to PUBlisher
@sockets.route('/zeromq1min')   # AUTONOMOUS AS IN hometemp:
def send_data(ws):
    logger.info('Got a websocket connection log')
    gevent.sleep()
    received = 0
    while True:
        received += 1
        MESSAGE=[]
        files=[ 'counters.jpg', 'streampic_00.jpg']
        print("i... in the loop before rand")
        rand=randint(0,999999)
        for fi in files:
            print("i... file",fi)
            copyfile("/tmp/{}".format(fi),   "./static/{}".format(fi) )
            MSG='<img width="350px" height="300px" src="/static/{}?a={:d}">'.format( fi, rand )
            MESSAGE.append( '<div class="floated_img">'+MSG+'</div>' )
        ws.send(  "\n".join(MESSAGE) )
        logger.info("\n".join(MESSAGE)  )
        time.sleep(15)
        gevent.sleep()
        ######################

@app.route("/static/<path:path>")
def images(path):
    logger.info('images')
    generate_img(path)
    fullpath = "./static/" + path
    resp = flask.make_response(open(fullpath).read())
    resp.content_type = "image/jpeg"
    return resp

if __name__ == '__main__':
    logger.info('Launching web server on '+str(HTTP_PORT))
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server=pywsgi.WSGIServer(('',HTTP_PORT),app,handler_class=WebSocketHandler)
    logger.info('Starting serving')
    server.serve_forever()
    
