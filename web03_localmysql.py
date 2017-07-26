#!/usr/bin/python3
#from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from http.server import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import os.path
import cgi
import datetime
import logging
import argparse
import string

import re
import glob  # jpegs

import subprocess
###================================ end of logging config

mysqlhost="localhost"
mysqldb="test"
mysqltable="nfs"
mysqluser="ojr"
mysqlpass=""
with open( mysqltable+'.mysql') as f:
    mysqlhost=f.readline().rstrip()
    mysqluser=f.readline().rstrip()
    mysqlpass=f.readline().rstrip()

REDIRECT_TO="www.spiral2.eu"
PORT_NUMBER = 8011
WEBHOME='/home/spiral2/SharedDisk/spiral2-web/'
WEBHOME='/home/ojr/Maps'

parser=argparse.ArgumentParser(description="""
""")
import os

parser.add_argument('-w','--webhome',  default=os.environ["HOME"]+"/WEB/" , help='')
parser.add_argument('-p','--port',  default=8011,type=int , help='')
parser.add_argument('-r','--redirect_to',  default="spiral2.ujf.cas.cz", help='')

args=parser.parse_args()
WEBHOME=args.webhome
PORT_NUMBER=args.port
REDIRECT_TO=args.redirect_to


### LOGGER ====================================
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
def setup_logger(name, log_file, level=logging.INFO):
    """Function setup as many loggers as you want"""
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

log = setup_logger("normal",WEBHOME+'/web02.log')
loH = setup_logger("detail",WEBHOME+'/web02_details.log')
log.info('=======================Program started==========================')



### GLOB ===============================
def PrepareCNTS(WEBHOME, prefix):
    lines=[]
    now=datetime.datetime.now()

    #with open('/tmp/FARADAY','r') as f:
    #    faraday=f.read().rstrip()

    r=[0,0,0]
    rfa=[0,0,0]
    rde=[0,0,0]
    rel=[0,0,0]

        
    
    CMD='echo "select *  from '+mysqltable+' order by t desc limit 1;" | mysql -u '+mysqluser+'  -p'+mysqlpass+' -h '+mysqlhost+' '+mysqldb+' | tail -1'
    #print(CMD)
    rloc=subprocess.check_output( CMD,  shell=True ).decode('utf8').split()   
    #print(rloc)
    CMDCLONA='echo "select value,datetime from sensor1 order by datetime desc limit 1;" | mysql --connect-timeout=1 -u greis  -pgreis -h mojzis  monitoring | tail -1'
    r=subprocess.check_output( CMDCLONA,  shell=True ).decode('utf8').split()
    
    # CMDFARAD='echo "select value,datetime from sensor9 order by datetime desc limit 1;" | mysql -u greis  -pgreis -h mojzis  monitoring | tail -1'
    # rfa=subprocess.check_output( CMDFARAD,  shell=True ).decode('utf8').split()

    # CMDDEG='echo "select value,datetime from sensor8 order by datetime desc limit 1;" | mysql -u greis  -pgreis -h mojzis  monitoring | tail -1'
    # rde=subprocess.check_output( CMDDEG,  shell=True ).decode('utf8').split()

    # CMDELE='echo "select value,datetime from sensor7 order by datetime desc limit 1;" | mysql -u greis  -pgreis -h mojzis  monitoring | tail -1'
    # rel=subprocess.check_output( CMDELE,  shell=True ).decode('utf8').split()


    head="""<head>
<script type="text/javascript">
    <!--
    function updateTime() {
        var currentTime = new Date();
        var hours = currentTime.getHours();
        var minutes = currentTime.getMinutes();
        var seconds = currentTime.getSeconds();
        if (minutes < 10){
            minutes = "0" + minutes;
        }
        if (seconds < 10){
            seconds = "0" + seconds;
        }
        var v = hours + ":" + minutes + ":" + seconds + " ";
        setTimeout("updateTime()",100);
        document.getElementById('time').innerHTML=v;
    }
    updateTime();
    //-->
</script>
</head>
    """
    
    line=" <h3>COUNTERS - NFS/IC . <br>"
    lines.append(line)
    line=" <h3> <br>"+"Local PC time:  <span id=\"time\"/> </br></h3>"
    lines.append(line)
    line="Server time:  &nbsp "+now.strftime("%H:%M:%S")+" \n\n"
    lines.append(line)

    line=" <table><tr align \"right\"><td>          </td><td>:   nA  &nbsp MySQL time</td></tr>"
    lines.append(line)
    
    if len(r)>=3:
        line=" <tr align \"right\"  bgcolor=\"#AAFF55\"><td>CLONA    </td><td>: {:10.2f} &nbsp {}</td></tr>".format( float(r[0]),r[2])
        lines.append(line)
    line=" <tr align \"right\"><td>DEGRADER </td><td>: {:10.2f} &nbsp {}</td></tr>".format( float(rloc[4]), rloc[1] )
    lines.append(line)
    line=" <tr align \"right\"><td>ELEKTRODA</td><td>: {:10.2f} &nbsp {}</td></tr>".format( float(rloc[3]), rloc[1] )
    lines.append(line)
    line=" <tr align \"right\" font size=\"18\" bgcolor=\"#FFAA55\"><td> <bf>FARADAY</bf>  </td><td><bf>: {:.2f} &nbsp {} </bf></td></tr>".format( float(rloc[2]), rloc[1]  )
    lines.append(line)
    line=" <tr align \"right\"><td>T1       </td><td>: {:10.2f}</td></tr>".format( 0.0 )
    lines.append(line)
    line=" <tr align \"right\"><td>T2       </td><td>: {:10.2f}</td></tr>  </font>".format( 0.0 )
    lines.append(line)
 
    return  head+"<body>"+"\n".join(lines)+"</body>"



def PrepareJPGS(WEBHOME, prefix):

    COLUMNS=2
    WIDTH=450
    
    lines=[]
    topline=["| "]*(COLUMNS)
    midline=["|-"]*(COLUMNS) 
    #print( "".join(topline) )
    #print( "".join(midline) )
    
    photos=" ".join(topline) + '|\n' + " ".join(midline) + ' |\n'
    photos=""
    i=1
    for jpg in glob.glob(WEBHOME+"/*.jpg"):
        njpg=prefix+'/'+os.path.basename(jpg)
        print('i... ',i,'.  JPG FILE', jpg, njpg )
        line='<a href="'+njpg+'" target="_blank"><img src="'+njpg+'" width="'+str(WIDTH)+'"></img></a>'
        #line='<img src="'+njpg+'" width="'+str(450)+'"></img>'
        lines.append( line )
        if i%COLUMNS==0:
            print('i... preparing line')
            photos=photos+"| "+"|".join(lines)+'|\n <br> \n <br>\n'
            lines=[]
        i=i+1

    if len(lines)!=0:
        print('i... preparing last incomplete line')
        photos=photos+"| "+"|".join(lines)+'|\n'
    
    print(photos)
    return photos

#================================== CLASS  HANDLER========
#This class will handles any incoming request from
#the browser
class myHandler(BaseHTTPRequestHandler):

    #Handler for the GET requests ====+++++GET++++=====
    def do_GET(self):
        """
        when redirected: client_addres=127.0.0.1
        X-Forwarded-For:
        """
        # FAKE SERVER VERSION
        self.server_version = "Server: Apache 13.2"
        self.sys_version = ""
        #LOG STUFF
        remoteIP=re.findall('X-Forwarded-For:\s+([\d\.]+)', str(self.headers) )
        #remoteIP=re.findall(r'Connection:(.+)', str(self.headers) )
        print( 'remoteIP=',remoteIP )
        log.info( datetime.datetime.now().strftime(" %a  - ")+self.client_address[0]+'   '+' '.join(remoteIP)+' # '+self.requestline )
#        log.info( datetime.datetime.now().strftime("%Y%m%d_%a_%H%M%S")+' '+self.client_address[0]+' '+ '#' +' '+self.requestline )
        loH.info( self.headers)
        #print('GET ', end='')
        #self.path=
        #print( re.sub( r'\.\.','', self.path ) )
        ###############################
        # basic security /amateur level/ :  \b backspaces
        #  .. path
        self.path=self.path.replace( '\b', '')
        self.path=self.path.replace( '..', '')
        if self.path.find('\.\.')>=0:  # no cd ..
            print('ERROR .. ', self.path)
            log.error(' .. found')
            self.send_error(404,'File Not Found: %s' % self.path)
            return
        if self.path.find('/')!=0:  # always start with /
            print('ERROR / ', self.path)
            log.error(' / ')
            self.send_error(404,'File Not Found: %s' % self.path)
            return
        if self.path=="/":  # just translate / to /index.html
            self.path="/index.html"
        #===== now: if not nastro:redirect =================
        #print('i... before nastro check', self.path)
        if self.path.find('/nastro'):   # not ZERO? => redirect
            #self.send_error(404,'File Not Found: %s' % self.path)
            #return
            self.send_response(301)
            self.send_header('Location','http://'+REDIRECT_TO)
            log.info(' ... redirected to '+REDIRECT_TO)
            self.end_headers()
            return
        #===== now: if not nastro:redirect =================
        #print('i... succeeded to NASTRO', self.path)
        self.path=re.sub('/nastro','', self.path )    # remove /nastro
        if len(self.path)==0: self.path='/'
        print('i... succeeded to NASTRO', self.path)
        #if self.path=="/":  # just translate
        #    self.path="/index.html"
        try:
            sendFile = False
            if self.path.endswith(".html"):
                mimetype='text/html'
                sendFile = True
            if self.path.endswith(".jpg"):
                mimetype='image/jpg'
                sendFile = True
            if self.path.endswith(".gif"):
                mimetype='image/gif'
                sendFile = True
            if self.path.endswith(".ico"):
                mimetype='image/ico'
                sendFile = True
            if self.path.endswith(".js"):
                mimetype='application/javascript'
                sendFile = True
            if self.path.endswith(".css"):
                mimetype='text/css'
                sendFile = True
            if sendFile and (os.path.isfile(WEBHOME+self.path)):
                f = open(WEBHOME + self.path,'rb')
                print('serving = '+str( f.name )+'  '+str(not(f.closed)))
                self.send_response(200)
                self.send_header('Content-type',mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            elif sendFile:   # KNOWN EXTENSION AT LEAST
                print('....file doesnot exist...')
                log.error('file doesnot exist')
                self.send_error(404,'File Not Found: %s' % self.path)
            else:  # UNKNOWN EXTENSION OR EMPTY after /nastro
                # MY OWN CODES =================================
                if self.path.find('nfs'):
                    print('NFS CODE')
                    self.send_response(200)
                    self.send_header('Content-type','text/html')
                    self.end_headers()
                    responseNFS=PrepareCNTS(WEBHOME,'/nastro')
                    self.wfile.write(
                        bytes('<META HTTP-EQUIV="refresh" CONTENT="1"><html><body>'+responseNFS+'</body></html>','utf-8'))
                else:
                    print('NASTRO - own code')
                    self.send_response(200)
                    self.send_header('Content-type','text/html')
                    self.end_headers()
                    response=PrepareJPGS(WEBHOME,'/nastro')
                    self.wfile.write(
                        bytes('<html><body>'+response+'</body></html>','utf-8'))
            return

        except IOError:
            print('send ioerror')
            self.send_error(404,'File Not Found: %s' % self.path)

    #Handler for the POST requests
    def do_POST(self):
        print('POST entered : path=',self.path )
        log.error('Unallowed POST ')
        self.send_error(404,'File Not Found: %s' % self.path)
        return
        # if self.path=="/send":   # this is a section in POST
        #         form = cgi.FieldStorage(
        #                 fp=self.rfile,
        #                 headers=self.headers,
        #                 environ={'REQUEST_METHOD':'POST',
        #                  'CONTENT_TYPE':self.headers['Content-Type'],
        #         })
        #         print( form.keys() )
        #         print( "Your name is: %s" % form["your_name"].value)
        #         self.send_response(200)
        #         self.send_header('Content-type','text/html')
        #         self.end_headers()
        #         aaa=''
        #         for k in form.keys() :
        #                 aaa=aaa + form[k].value +'\n' ;
        #                 print( k, form[ k].value )
        #         self.wfile.write( bytes('<html><body>'+
        #                 'WE ARE IN POST PART NOW<br><br>Thanks '+ form["your_name"].value + '. <br>'+
        #                 str(form.keys())+aaa+
        #                 '</body></html>','utf-8') )
        #         return
try:
    #Create a web server and define the handler to manage the
    #incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print( 'Started httpserver on port ' , PORT_NUMBER)

    #Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print( '^C received, shutting down the web server')
    server.socket.close()
