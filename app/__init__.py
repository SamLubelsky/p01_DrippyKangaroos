from flask import Flask             #facilitate flask webserving
from flask import render_template, request   #facilitate jinja templating
from flask import session, redirect, url_for, make_response 
import os
import requests
import db_builder
import newsapi
from datetime import date
app = Flask(__name__)
app.secret_key = os.urandom(32)
cur_date = str(date.today())
if db_builder.new_day(cur_date):
    db_builder.update_date(cur_date)
@app.route('/')
def index():
    if 'username' in session:
        if db_builder.verify(session['username'], session['password']):
            return redirect("/home")
    return render_template('login.html') 

@app.route('/login', methods = ['GET','POST'])
def login():
    # print(request.form)
    username = request.form.get('username')
    password = request.form.get('password')
    if db_builder.verify(username,password):
        session['username'] = username
        session['password'] = password
        return redirect("/home")
    if request.form.get('submit_button') is not None:
        return render_template("create_account.html")
    response = make_response(render_template('error.html', msg="username or password is not correct"))
    return response

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    accounts = db_builder.get_table_list("User")
    if request.method == 'POST':
        userIn = request.form.get('username')
        passIn = request.form.get('password') 
        passConfirm = request.form.get('password2')
        if passIn != passConfirm:
            return render_template("create_account.html", error_msg="passwords don't match")
        if userIn == None:
            return render_template("create_account.html")
        if db_builder.add_account(userIn, passIn) == -1:
            return render_template("create_account.html",
            error_msg= f"Account with username {userIn} already exists")
        return render_template("sign_up_success.html")
    return redirect(url_for('index'))
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('password', None)
    return redirect(url_for('index'))

@app.route("/home", methods=['GET', 'POST'])
def home():
    if(verify_session()):
        articles = db_builder.get_from_genre("General")
        return render_template("home.html", articles=articles)
    else:
        return render_template("error.html", msg="session could not be verifited")

@app.route("/explore")
def explore():
    if(verify_session()):
        return render_template("explore.html")
    else:
        return render_template("error.html", msg="Session could not be verifited")

@app.route("/topic")
def topic():
    genre = request.args.get("topic")
    articles = db_builder.get_from_genre(genre)
    if(verify_session()):
        return render_template("topic.html", articles=articles)
    else:
        return render_template("error.html", msg="session could not be verifited")

@app.route("/about")
def about():
    if(verify_session()):
        return render_template("about.html")
    else:
        return render_template("error.html", msg="session could not be verifited")

@app.route("/profile")
def profile():
    if(verify_session()):
        return render_template("profile.html", username=session['username'])#, articles = articles) 
    else:
        return render_template("error.html", msg="session could not be verifited")
        
def verify_session():
    if 'username' in session and 'password' in session:
        if db_builder.verify(session['username'], session['password']):
            return True
    return False

if __name__ == "__main__":
    app.debug = True
    app.run()

