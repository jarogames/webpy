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
```