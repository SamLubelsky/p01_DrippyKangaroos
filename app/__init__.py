from flask import Flask             #facilitate flask webserving
from flask import render_template, request   #facilitate jinja templating
from flask import session, redirect, url_for, make_response 
import os
import requests
import json
import db_builder
import weatherapi
import newsapi
import stockapi
from datetime import date
import csv
app = Flask(__name__)
app.secret_key = os.urandom(32)
genres = ["Business", "Entertainment", "General", "Health", "Science", "Sports", "Technology"]

stocks = []

def read_stocks():
    temp = []
    with open('S&P_500_companies.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, quotechar='|')
        for row in spamreader:
            temp.append(row)
    stocks = temp

read_stocks()

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
    if request.form.get('create_acc_button') is not None:
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
            return render_template("create_account.html", error_msg="Passwords don't match")
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
    if (verify_session()):
        username = session['username']
        weather_data = weatherapi.get_weather_data()
        articles = db_builder.get_from_genre("General")
        # stocks = db_builder.get_stocks(username)
        return render_template("home.html", articles=articles, genres=genres, weather=weather_data, stocks=stocks)
    else:
        return render_template("error.html", msg="session could not be verifited")

@app.route("/explore")
def explore():
    query = request.args.get("query")
    if(verify_session()):
        articles = []
        default_text = ""
        if query is not None:
            articles = newsapi.request_articles(query, 5)
            if len(articles) == 0:
                default_text = f"No articles could be found for the search term {query}"
        return render_template("explore.html", genres=genres, articles = articles, text = default_text)
    else:
        return render_template("error.html", msg="Session could not be verifited")  

@app.route("/topic")
def topic():
    if(verify_session()):
        weather_data = weatherapi.get_weather_data()
        topic = request.args.get("topic")
        articles = db_builder.get_from_genre(topic)
        return render_template("topic.html", articles=articles, topic=topic, genres=genres, weather = weather_data)
    else:
        return render_template("error.html", msg="session could not be verifited")

@app.route("/about")
def about():
    if(verify_session()):
        return render_template("about.html", genres=genres)
    else:
        return render_template("error.html", msg="session could not be verifited")

@app.route("/profile")
def profile():
    if(verify_session()):
        return render_template("profile.html", username=session['username'], genres=genres, stocks=stocks)
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

