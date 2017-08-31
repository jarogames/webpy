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


HTML_PORT=25005
ZMQ_LISTENING_PORT = 12005 # 

##### GREGORY DIR  ======================
gregorydata=os.environ.get('GREGORY_DATA')
if gregorydata!=None:
    print("+... going to GREGORY_DATA")
else:
    print('x... GREGORY_DATA path NOT defined')
    gregorydata="."

chanws1=glob.glob(gregorydata+'/Histo_0_*.txt')
maxch=len(chanws1)

SELECTHIST=0

def getListHist(board=0):
    global SELECTHIST
    finame='Histo_'+str(board)+'_'+str( SELECTHIST )+'.txt'
    ws=glob.glob(gregorydata+'/'+finame)
    print(ws)
    if ws==[]:return finame,[]
    nam=ws[ 0 ]
    try:
        with open( nam ,"r") as f:
            lis=list(map( str.strip , f ))
            lis=[x for x in lis if not x.startswith('#')]
            lis=list(map( int , lis ))
            f.close()
    except:
        return nam,[]
    return nam,lis






@app.route('/', methods=['GET', 'POST'])
def index():
    global SELECTHIST
    logger.info('At index page')
    if request.method == 'POST':
        #print("POST=====================")
        #print( request )
        print( "Selkecte Histo",request.form.get('hist') )
        SELECTHIST=request.form.get('hist')
    elif request.method == 'GET':
        print("GET=====================")
        #return render_template('contact.html', form=form)
    logger.info('Rendering index page')
    return render_template('gregory_main.html')



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
        #####################################
        #   HERE I HACK json - adding Pcolr Rcolor
        #
        #
        ccod=['white','chartreuse','lightgreen',
              'yellow','gold',
              'pink', 'lightsalmon',
              'coral'
              ]
        # I SELECT HERE 2 BOARDS ############################
        for v1,board in {'0':data['0'],'1':data['1']}.items():
            #print('# v1 and board:',v1,board)
            for v,chan in board.items(): 
                #print('## v and chan: ',v,chan)
                if v!='time' and v!='histox' and v!='histoy':
                    actcod=ccod[0]
                    if float( chan['Rate'])>0.0:actcod=ccod[1]
                    if float( chan['Rate'])>1.0:actcod=ccod[2]
                    if float( chan['Rate'])>2.0:actcod=ccod[3]
                    if float( chan['Rate'])>3.0:actcod=ccod[4]
                    if float( chan['Rate'])>4.0:actcod=ccod[5]
                    if float( chan['Rate'])>5.0:actcod=ccod[6]
                    if float( chan['Rate'])>6.0:actcod=ccod[7]
                    data[ str(v1) ][str(v)]['Rcolor']=actcod
                    #-----------------------------------
                    actcod=ccod[0]
                    if float( chan['PileUp'])>0.0:actcod=ccod[1]
                    if float( chan['PileUp'])>1.0:actcod=ccod[2]
                    if float( chan['PileUp'])>2.0:actcod=ccod[3]
                    if float( chan['PileUp'])>3.0:actcod=ccod[4]
                    if float( chan['PileUp'])>4.0:actcod=ccod[5]
                    if float( chan['PileUp'])>5.0:actcod=ccod[6]
                    if float( chan['PileUp'])>6.0:actcod=ccod[7]
                    data[ str(v1) ][str(v)]['Pcolor']=actcod
        #d = json.loads( data )
        #d['time'] = 'green'
        #d['2']['Pcolor'] = 'red'
        #data.set_data(json.dumps(d))
        ###################################
        #  adding histox
        #
        #HISTOGRAM FROM  .......... GREGORY_DATA
        #
        #for i,v in enumerate(data['histoy']):
            #print(i,v)
            #data['histox'].append(i)
        filename,histy=getListHist()
        print("--------",filename)
        data['histox']=[]
        data['histoy']=[]
        data['filename']=filename
        for i,v in enumerate(histy):
            #print(i,v)
            data['histox'].append(i)
            data['histoy'].append(v)
        
        ##################################    
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
    
