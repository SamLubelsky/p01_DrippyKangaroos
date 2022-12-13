import sqlite3
import newsapi
from datetime import date

users = ("(username TEXT, password TEXT)")
home_article = ("(article_id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT)")
article_info = ("(article_id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, date_published TEXT, author TEXT, summary TEXT, url TEXT, image_url TEXT)")
article_tags = ("(article_id INTEGER PRIMARY KEY AUTOINCREMENT, topic TEXT)")

def data_query(table, info = None):
    db = sqlite3.connect("database.db")
    c = db.cursor()
    if info is None:
        output = c.execute(table)
    else:
        output = c.execute(table, info)
    db.commit()
    db.close()
    return output
    
def create_table(name, outline):
    #data_query(f"DROP TABLE IF EXISTS {name}")
    data_query(f"CREATE TABLE IF NOT EXISTS {name} {outline}")

create_table("Home", home_article)
create_table("News", article_info)
create_table("Tags", article_tags)
create_table("User", users)

def get_table_list(name):
    db = sqlite3.connect("database.db")
    c = db.cursor()
    curr = c.execute(f"SELECT * from {name}")
    output = curr.fetchall()
    db.commit()
    db.close()
    return output
    

def add_account(username, password):
    if not(used(username,"User")):
        data_query("INSERT INTO User VALUES (?, ?)", (username, password))
    else:
        return -1


def verify(username, password):
    accounts = get_table_list("User")
    for account in accounts:
        if account[0] == username and account[1] == password:
            return True
    return False

def used(name,table):
    arr = get_table_list(table)
    for i in arr:
        if i[0] == name:
            return True
    return False

todate = ""
def check_date(home):
    todate = date.today()
    if home == True:
        home_articles = get_table_list("Home")
        for article in home_articles:
            if home_articles[1] == date.today():
                return True
    return False
        

def articling(): #adds articles into db if it hasn't alr been added day of
    if not (check_date(True)):
        db = sqlite3.connect("database.db")
        c = db.cursor()
        categories = ["business", "entertainment", "general", "health", "sciences", "sports", "technology"]
        for cat in categories:
            for article in newsapi.request_top_headlines(cat, n = 10):
                url = newsapi.article_info(article)['url']
                title = newsapi.article_info(article)['title']
                desc = newsapi.article_info(article)['description']
                date = newsapi.article_info(article)['date']
                author = newsapi.article_info(article)['author']
                image_url = newsapi.article_info(article)['image']
                c.execute("INSERT INTO News (title, date_published, author, summary, url, image_url) VALUES (?, ?, ?, ?, ?, ?)", (title, date, author, desc, url, image_url))
                id = int(c.execute("SELECT article_id FROM News ORDER BY article_id DESC LIMIT 1;").fetchone()[0])
                c.execute("INSERT INTO Home VALUES (?, ?)", (id, f"{todate}"))
                c.execute("INSERT INTO Tags VALUES (?, ?)", (id, cat))          
        db.commit()
        db.close()

def articles(cat): #returns articles stored for topic cat (ex. business) as list
    articling()
    db = sqlite3.connect("database.db")
    c = db.cursor()
    topic_ids = c.execute('SELECT article_id FROM Tags WHERE topic = ?;', [cat]).fetchall()
    ids = []
    for id in topic_ids:
        ids.append(id[0])
    output = []
    for id in ids:
        output += c.execute(f"SELECT * FROM NEWS WHERE article_id = ?;", [id]).fetchall()
    db.commit()
    db.close()
    return output


