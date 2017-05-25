#!/usr/bin/python3
#from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from http.server import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import os.path
import cgi
import datetime
import logging


###================================ end of logging config

PORT_NUMBER = 8011
WEBHOME='/home/spiral2/SharedDisk/spiral2-web/'
WEBHOME='/home/ojr/Maps'


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
log.info('Program started')


#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):

        #Handler for the GET requests
        def do_GET(self):
                log.info( datetime.datetime.now().strftime("%Y%m%d_%a_%H%M%S")+' '+self.client_address[0]+' '+'#'+' '+self.requestline )
                loH.info( self.headers)
                #print('GET ', end='')
                if self.path=="/":
                        self.path="/index.html"
                        response='<meta http-equiv="refresh" content="0; url=http://example.com/" />'
                try:
                        #Check the file extension required and
                        #set the right mime type
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
                        #if sendFile and (os.path.isfile(WEBHOME+self.path)):
                        #        print('sendFile at get  = ',sendFile, '. Filename=',self.path)
                        #else:
                        #        print('no sendfile')
                        if sendFile and (os.path.isfile(WEBHOME+self.path)):
                                f = open(WEBHOME + self.path,'rb')      
                                print('serving = '+str( f.name )+'  '+str(not(f.closed)))
                                self.send_response(200)
                                self.send_header('Content-type',mimetype)
                                self.end_headers()
                                self.wfile.write(f.read())
                                f.close()
                        elif sendFile:
                                print('....file doesnot exist...')
                                log.error('file doesnot exist')
                                self.send_error(404,'File Not Found: %s' % self.path)
                        else:
                                # MY OWN CODES =================================
                                if self.path=='/nastro/':
                                        print('NASTRO')
                                        self.send_response(200)
                                        self.send_header('Content-type','text/html')
                                        self.end_headers()
                                        response='HELLO. THIS SCRIPT SHOWS inline http code and is example for a server with GET(normal html) and POST(form sending) PARTS<hr>'
                                        self.wfile.write(
                                        bytes('<html><body>'+response+'</body></html>','utf-8'))
                                else:
                                        log.error('Unknown CODE')
                        return

                except IOError:
                        print('send ioerror')
                        self.send_error(404,'File Not Found: %s' % self.path)

        #Handler for the POST requests
        def do_POST(self):
                print('POST entered : path=',self.path )
                log.error('Unallowed POST ')
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
