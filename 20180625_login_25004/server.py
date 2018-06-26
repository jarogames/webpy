#!/usr/bin/python3
#  - chrome   Ctrl-F5 to refresh the cache
#    https://www.tutorialspoint.com/flask/flask_templates.htm
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os

from string import ascii_lowercase
from random import choice

username = ''.join([choice(ascii_lowercase) for _ in range(4)])
print("username=",username)


HTTP_PORT = 25004

app = Flask(__name__)


@app.route('/')
def home():
    if not session.get('logged_in'):
        print("LOGINNOW")
        return render_template('index.html')
        return render_template('login2.html')
    else:
        print("LOG OUT NOW")
        return render_template('index.html')


    
@app.route('/logout2.html')
def logout2():
    session['logged_in'] = False
    return render_template('index.html')


@app.route('/login2.html')
def login():
    session['username']=username# each server run it is unique
    if not session.get('logged_in'):
        print("LOGINNOW")
        return render_template('login2.html')
    else:
        print("LOG OUT NOW")
        return render_template('index.html')

    
@app.route('/login', methods=['POST'])
def do_admin_login():
    print( request.form['password'], request.form['username'] )
    if request.form['password'] == 'password' and request.form['username'] == username:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

#@app.route("/logout", methods=['POST'])
#def logout():
#    session['logged_in'] = False
#    print("SERVING INDEX NOW")
#    return  render_template('index.html')
##home()


@app.route('/<any>')
def anypage(any):
    return render_template( any )


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    print( app.secret_key)
    app.run(debug=True,host='0.0.0.0', port=HTTP_PORT)


########    ###############
#http://flask-debugtoolbar.readthedocs.io/en/latest/
####### something interesting    
# @app.context_processor
# def get_legacy_var():
#     return dict(get_legacy_var=your_get_legacy_var_function())
# Then on your template:

# {{ get_legacy_var }}
