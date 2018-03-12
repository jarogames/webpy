# FLASK

  *Here are the tips and tricks to install run and use FLASK. It started rather simply, but after the complexity increased I see the need of  more structured document/manual/advices that would be repeatable.*


## Installation

## Howto install ZMQ comet

```
 pip3 install Flask
 pip3 install flask-sockets
 pip3 install gevent
 pip3 install karellen-geventws
 pip3 install pyzmq
```


#Running

##Howto RUN

`export FLASK_APP=hello.py flask run`

Worldwide:

`flask run --host=0.0.0.0`


It could be run like that or better deployed
with appache or other: http://flask.pocoo.org/docs/0.12/deploying/mod_wsgi/


O proxy the standalone from your web server: 
http://flask.pocoo.org/docs/0.12/deploying/wsgi-standalone/

##Running  directly

Like `./server.py`.

The line with host availability: `server = pywsgi.WSGIServer(('', HTTP_PORT),`

If the host ='' anybody ca connect. Use host='127.0.0.1' in danger.

To debug use the line 
`app.config['DEBUG'] =  True  # DO NOT USE IN PRODUCTION  !!!!!!!!!!!!`


#Organization

## Directories

- The dir starts with **a date tag** and a **flask** and tag(s) and **portnum**
- The dir contains a complete website that can be run
- async ZMQ codes to send info to client start with `zmq_`

This way each dir is a deplayable server and it is clear which files
are necessary, including templates/static structure








# Scattered comments....


## home-temp - autorefresh - weboscket autoreload

Autorefresh is `js` trick contained only in `templates` and `static`.

- `templates` - html file contains lines:
   -  the  `<div id="latest_data"></div>`
   - and at the very end....javascript
  ``` 
  <script>
   ws = new ReconnectingWebSocket("ws://"  + location.host + '/send_data')
   ws.onmessage = function(message) {
   //payload = JSON.parse(message.data);
   $('#latest_data').html( message.data );
		};
   </script>
`  ```
- the python server file should contain **before/after event** routes
```
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
```
- and the route that corresponds to reload function
```
@sockets.route('/send_data')   # AUTONOMOUS reload
def send_data(ws):
```



