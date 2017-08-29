#!/usr/bin/python3
import zmq.green as zmq
import json
import gevent
from flask_sockets import Sockets
import flask
from flask import Flask, render_template
import logging
from gevent import monkey

from random import randint
import time

import urllib.request #python3 version   of   urllib

###############################
#    
#
#
###
import os
from shutil import copyfile  # COPY FROM TMP
import os,sys

monkey.patch_all()

#app = Flask(__name__, static_url_path = "/tmp", static_folder = "tmp" ) # disk location; 'static'
app = Flask(__name__, static_folder = "static" ) # disk location; 'static'
app.config['DEBUG'] = True

#app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sockets = Sockets(app)
context = zmq.Context()

ZMQ_LISTENING_PORT = 12003
HTTP_PORT=8900

HOMEMAPS=os.environ['HOME']+"/Maps/"

# @app.before_request
# def before_every_request():
#     logger.info("before request")
       
# ## No caching at all for API endpoints.
# @app.after_request
# def add_header(response):
#     logger.info('add header after request')
#     response.cache_control.no_store = True
#     response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
#     response.headers['Pragma'] = 'no-cache'
#     response.headers['Expires'] = '-1'
#     return response


@app.route('/')
def index():
    logger.info('Rendering index page')
    return render_template('maps.html', data="MAPS")


@app.route("/<zoom>/<lat>/<lonpng>")
def images(zoom,lat,lonpng):
    #logger.info('images from '+HOMEMAPS )
    appendix=zoom+"/"+lat+"/"+lonpng
    localdir=HOMEMAPS.rstrip('/')+"/"+zoom+"/"+lat
    fullpath = HOMEMAPS.rstrip('/')+"/"+appendix
    logger.info('images from '+fullpath )
    #
    if os.path.exists(fullpath):
        return flask.send_file(fullpath,
                     attachment_filename=lonpng,
                     mimetype='image/png')
    else:
        url=''
        zoom=int(zoom)
        if (zoom==15) or(zoom==12):
            url='http://a.tile.komoot.de/komoot-2/'+appendix
        elif (zoom==8) or(zoom==5):
            url='http://tile.openstreetmap.org/'+appendix
            #https://maps.wikimedia.org/#4/40.75/-73.96
        else:
            logger.error("NOT A ZOOM- aborting "+url)
            return flask.abort(404)
            #render_template('maps.html', data="ZOOM ERROR")
        logger.info("NOT ON DISK-getting from "+url)
        if not os.path.exists(localdir):
            logger.info("making dir: "+localdir)
            os.makedirs(localdir)
        try:
            urllib.request.urlretrieve( url , fullpath )
        except:
            logger.error('page '+appendix+' not downloaded ... @except')
            return flask.abort(404)
        if os.path.exists(fullpath):
            return  flask.send_file(fullpath,
                     attachment_filename=lonpng,
                     mimetype='image/png')
        else:
            logger.error('page '+appendix+' not ...not found localy')
            return flask.abort(404)



if __name__ == '__main__':
    logger.info('Launching web server')
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', HTTP_PORT), app, handler_class=WebSocketHandler)
    logger.info('Starting serving')
    server.serve_forever()
    
