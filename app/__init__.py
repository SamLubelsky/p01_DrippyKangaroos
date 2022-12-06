from flask import Flask             #facilitate flask webserving
from flask import render_template, request   #facilitate jinja templating
from flask import session, redirect, url_for, make_response 
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)
@app.route("/")
def home():
    