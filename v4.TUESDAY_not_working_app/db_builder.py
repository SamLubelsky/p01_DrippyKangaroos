import sqlite3
import newsapi
from datetime import date
users = ("(username TEXT, password TEXT, stocks TEXT)")
article = (
    "(title TEXT, url TEXT, imageUrl TEXT, summary TEXT, genre TEXT, source TEXT)")


def data_query(table, info=None, fetchall=False):
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
    if username == None or username == "" or password == None or password == "":
        return -2
    if not (exists(username, "User")):
        data_query("INSERT INTO User VALUES (?, ?, ?)", (username, password, "AAPL"))
        print(data_query(f'''SELECT * FROM User WHERE username = "{username}"''', fetchall = True))
    else:
        return -1


def verify(username, password):
    user = False
    accounts = get_table_list("User")
    for account in accounts:
        if account[0] == username and account[1] == password:
            return True
    return False


def exists(name, table):
    arr = get_table_list(table)
    for i in arr:
        if i[0] == name:
            return True
    return False


def clear_table(table):
    data_query(f"DELETE FROM {table}")


def reset_articles():
    clear_table("Article")


def new_day(cur_date):
    with open('update_date.txt', 'r') as f:
        old_date = f.read().strip()
    if cur_date != old_date:
        return True
    else:
        return False


def update_date(new_date):
    reset_articles()
    add_all_genres()
    with open('update_date.txt', 'w') as f:
        f.write(new_date)


def add_article(title, imageUrl, url, summary, genre, source):
    data_query("INSERT INTO Article VALUES (?, ?, ?, ?, ?, ?)",
               (title, url, imageUrl, summary, genre, source))


def add_from_genre(genre):
    # print("starting")
    articles = newsapi.request_top_headlines(genre)
    # print("done grabbing api")
    for article in articles:
        title = article["title"]
        summary = article["description"]
        url = article["urlToImage"]
        imageUrl = article["url"]
        source = article["source"]["name"]
        # print(title, type(title))
        # print(url, type(url))
        # print(summary, type(summary))
        # print(genre, type(genre))
        add_article(title, url, imageUrl, summary, genre, source)


def add_all_genres():
    print("Its a new day! I'm grabbing the newest headlines for today")
    genres = ["Business", "Entertainment", "General",
              "Health", "Science", "Sports", "Technology"]
    for i, genre in enumerate(genres):
        print(f"{((i / len(genres)) * 100):.2f}% done")
        add_from_genre(genre)

    print("Done.")


def get_from_genre(genre):
    resp = data_query(f'''
    SELECT
    title,
    url,
    imageUrl,
    summary,
    genre,
    source
    FROM 
    Article 
    WHERE 
    genre="{genre}"''', fetchall=True)
    return resp

def get_stocks(username):
    stocks = data_query(f'''SELECT stocks FROM User WHERE username = "{username}"''', fetchall = True)
    if stocks != []:
        return stocks[0].split(",")
    return []

def add_stock(user, stock):
    user_stocks = f"{get_stocks(user)},{stock}"
    data_query("UPDATE User SET stocks = ? WHERE username = ?", (user_stocks, user))
    return 1
    
add_account("soft", "dev")

if __name__ == "__main__":
    pass
    #reset_articles()
    #add_all_genres()
    # print(get_from_genre("Science"))
