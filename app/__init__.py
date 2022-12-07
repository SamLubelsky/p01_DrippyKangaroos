from flask import Flask             #facilitate flask webserving
from flask import render_template, request   #facilitate jinja templating
from flask import session, redirect, url_for, make_response 
import os
import requests

app = Flask(__name__)
app.secret_key = os.urandom(32)
@app.route("/")
def home():
    if verify_session():   
        pass 

def verify_session():
    return True
    #if username & pwd in cookies
    if 'username' in session and 'password' in session:
        if db_tools.verify_account(session['username'], session['password']):
            return True
    return False