from flask import Flask             #facilitate flask webserving
from flask import render_template, request   #facilitate jinja templating
from flask import session, redirect, url_for, make_response 
import os
import requests
import db_builder

app = Flask(__name__)
app.secret_key = os.urandom(32)
@app.route('/')
def index():
    if 'username' in session:
        return redirect("/landing")
    return render_template('login.html') 

@app.route('/login', methods = ['GET','POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if db_builder.verify(username,password):
        session['username'] = username
        session['password'] = password
        return redirect("/landing")
    if request.form.get('submit_button') is not None:
        return render_template("create_account.html")
    response = make_response(render_template('error.html',msg = "username or password is not correct"))
    return response

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    accounts = db_builder.get_table_list("User")
    if request.method == 'POST':
        userIn = request.form.get('username')
        passIn = request.form.get('password') 
        for account in accounts:
            if account[0]==userIn:
                return f"account with username {userIn} already exists"
        db_builder.add_account(userIn,passIn)
        return render_template("signed_in.html")
    return redirect(url_for('index'))
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))