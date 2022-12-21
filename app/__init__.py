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

def read_stocks(local_list):
    with open('S&P_500_companies.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, quotechar='|')
        for row in spamreader:
            local_list.append(row)
    # print(local_list)
    local_list=local_list[2:]
    return local_list

stocks = read_stocks(stocks)

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

        if request.form.get('create_acc_button2') is None:
            return render_template("create_account.html")
        else:
            result = db_builder.add_account(userIn, passIn)
            if result != True:
                if result == -2:
                    return render_template("create_account.html", error_msg="Username/Password cannot be empty")
                elif db_builder.add_account(userIn, passIn) == -1:
                    return render_template("create_account.html",
                        error_msg= f"Account with username {userIn} already exists")
            if passIn != passConfirm:
                return render_template("create_account.html", error_msg="Passwords don't match")
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
        # Sam's code:
        # stocks = db_builder.get_stocks(username)
        # print("stocks: " + str(stocks))
        # stocks_with_price = []
        # for stock in stocks:
        #     print("stock: " + stock)
        #     stocks_with_price.append([stock, stockapi.get_price(stock)])
        # return render_template("home.html", articles=articles, genres=genres, weather=weather_data, stocks=stocks_with_price)
        # if 'stock_choice' in session:
        #     stocks = [[session['stock_choice'], stockapi.get_price(session['stock_choice'])]]
        # else:
        stocks = [["aapl", stockapi.get_price("aapl")], ["tsla", stockapi.get_price("tsla")], ["googl", stockapi.get_price("googl")], ["amzn", stockapi.get_price("amzn")], ["meta", stockapi.get_price("meta")]]

        #print(f"stocks: {stocks}")
        #print(username)
        # stocks = db_builder.get_stocks(username)
        # for stock in stocks:
        #     stock.append(stockapi.get_price(stock[0]))
        return render_template("home.html", articles=articles, genres=genres, weather=weather_data, stocks=stocks)
    else:
        return render_template("error.html", msg="session could not be verifited")

@app.route("/explore")
def explore():
    query = request.args.get("query")
    articles = []
    if query is not None:
        articles = newsapi.request_articles(query, 15)
    if(verify_session()):
        return render_template("explore.html", genres=genres, articles = articles)
    else:
        return render_template("error.html", msg="Session could not be verifited")  

@app.route("/topic")
def topic():
    if(verify_session()):
        username = session['username']
        weather_data = weatherapi.get_weather_data()
        topic = request.args.get("topic")
        articles = db_builder.get_from_genre(topic)
        # if 'stock_choice' in session:
        #     stocks = [[session['stock_choice'], stockapi.get_price(session['stock_choice'])]]
        # else:
        stocks = [["aapl", stockapi.get_price("aapl")], ["tsla", stockapi.get_price("tsla")], ["googl", stockapi.get_price("googl")], ["amzn", stockapi.get_price("amzn")], ["meta", stockapi.get_price("meta")]]

        #stocks = # db_builder.get_stocks(username)
        return render_template("topic.html", articles=articles, topic=topic, genres=genres, weather = weather_data, stocks=stocks)
    else:
        return render_template("error.html", msg="session could not be verifited")

@app.route("/about")
def about():
    if(verify_session()):
        return render_template("about.html", genres=genres)
    else:
        return render_template("error.html", msg="session could not be verifited")

@app.route("/profile", methods=['GET', 'POST'])
def profile():
    if(verify_session()):
        username = session['username']
        # if request.method == 'POST':
        #     session['stock_choice']=(request.form.get('new_stock'))
        # if 'stock_choice' in session:
        #     print(session['stock_choice'])
        #     db_builder.add_stock(username, session['stock_choice'])
        # print(f"get_stocks: {get_stocks(username)}")
        # PROBLEM LINES:
        user_stocks = get_stocks(username)
        print(user_stocks)
        return render_template("profile.html", username=session['username'], genres=genres, stocks=stocks, user_stocks=user_stocks)
    else:
        return render_template("error.html", msg="session could not be verifited")
        
def verify_session():
    if 'username' in session and 'password' in session:
        if db_builder.verify(session['username'], session['password']):
            return True
    return False

def get_stocks(username):
    stocks = db_builder.get_stocks(username)
    stocks_with_price = []
    for stock in stocks:
        stocks_with_price.append([stock, stockapi.get_price(stock)])
    return stocks_with_price

if __name__ == "__main__":
    app.debug = True
    app.run()

