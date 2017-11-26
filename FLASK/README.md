## Howto RUN



`export FLASK_APP=hello.py flask run`

Worldwide:

`flask run --host=0.0.0.0`


It could be run like that or better deployed
with appache or other: http://flask.pocoo.org/docs/0.12/deploying/mod_wsgi/


O proxy the standalone from your web server: 
http://flask.pocoo.org/docs/0.12/deploying/wsgi-standalone/


## Howto install ZMQ comet

```
 pip3 install Flask
 pip3 install flask-sockets
 pip3 install gevent
 pip3 install karellen-geventws
 pip3 install pyzmq
```


## home-temp - autorefresh

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

```
@sockets.route('/zeromq1min')   # AUTONOMOUS AS IN hometemp:
def send_data(ws):
```

in template/aaron.html  
```
    <script type="text/javascript" src="static/js/application1min.js"></script>
```

in static/js/application1min.js
```
 spec reload
```


