import sqlite3
import newsapi
from datetime import date

users = ("(username TEXT, password TEXT)")
article = ("(title TEXT, url TEXT, summary TEXT, genre TEXT, date TEXT)")

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
    data_query(f"CREATE TABLE IF NOT EXISTS {name} {outline}")

create_table("Article", article)
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
    if not(exists(username,"User")):
        data_query("INSERT INTO User VALUES (?, ?)", (username, password))
    else:
        return -1


def verify(username, password):
    accounts = get_table_list("User")
    for account in accounts:
        if account[0] == username and account[1] == password:
            return True
    return False

def exists(name,table):
    arr = get_table_list(table)
    for i in arr:
        if i[0] == name:
            return True
    return False

def clear_table(table):
    data_query(f"DELETE FROM {table}")

def reset_articles():
    clear_table("Article")

todate = ""
#can clean this up by ordering maybe
def check_date():
    todate = date.today()
    home_articles = get_table_list("Article")
    for article in home_articles:
        if home_articles[1] == date.today():
            return True
    todate = date.today()
    return False

def add_article(title, url, summary, genre):
    if (check_date()):
        data_query("INSERT INTO Article VALUES (?, ?, ?, ?, ?)", (title, url, summary, genre, todate))

def add_from_genre(genre):
    articles = newsapi.request_top_headlines(genre)
    for article in articles:
        title = article["title"]
        summary = article["description"]
        url = article["url"]
        add_article(title, url, summary, genre)

def add_all_genres():
    genres = ["Business", "Entertainment", "General", "Health", "Science", "Sports", "Technology"]
    for genre in genres: 
        add_from_genre(genre)

def get_from_genre(genre):
    db = sqlite3.connect("database.db")
    c = db.cursor()
    resp = c.execute("""SELECT "title", "url", "summary" FROM Article WHERE genre=?""",[genre])
    db.commit()
    db.close()
    print(resp)

#if __name__ == "__main__":
    #print(add_from_genre("Business"))

#get_from_genre("Business")
