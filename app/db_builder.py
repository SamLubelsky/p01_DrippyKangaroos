import sqlite3
import newsapi
from datetime import date
users = ("(username TEXT, password TEXT)")
article = ("(title TEXT, url TEXT, imageUrl TEXT, summary TEXT, genre TEXT)")
def data_query(table, info = None, fetchall=False):
    db = sqlite3.connect("database.db")
    c = db.cursor()
    if info is None:
        output = c.execute(table)
    else:
        output = c.execute(table, info)
    if fetchall:
        output = output.fetchall()
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
def check_date():
    todate = date.today()
    home_articles = get_table_list("Article")
    for article in home_articles:
        if home_articles[1] == date.today():
            return True
    todate = date.today()
    return False

def add_article(title, imageUrl, url, summary, genre):
    data_query("INSERT INTO Article VALUES (?, ?, ?, ?, ?)", (title, url, imageUrl, summary, genre))
def add_from_genre(genre):
    print("starting")
    articles = newsapi.request_top_headlines(genre)
    print("done grabbing api")
    for article in articles:
        title = article["title"]
        summary = article["description"]
        url = article["urlToImage"]
        imageUrl = article["url"]
        #print(title, type(title))
        #print(url, type(url))
        #print(summary, type(summary))
        #print(genre, type(genre))
        add_article(title, url, imageUrl, summary, genre)
def add_all_genres():
    genres = ["Business", "Entertainment", "General", "Health", "Science", "Sports", "Technology"]
    for genre in genres: 
        add_from_genre(genre)

def get_from_genre(genre):
    resp = data_query(f'''
    SELECT
    title,
    url,
    imageUrl,
    summary,
    genre
    FROM 
    Article 
    WHERE 
    genre="{genre}"''', fetchall=True)
    return resp

add_account("soft", "dev")

if __name__ == "__main__":
    #reset_articles()
    add_all_genres()
    #print(get_from_genre("Science"))

