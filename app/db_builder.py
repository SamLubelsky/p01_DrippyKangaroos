import sqlite3
import newsapi
import csv
from datetime import date
users = ("(username TEXT, password TEXT, stocks TEXT)")
article = (
    "(title TEXT, url TEXT, imageUrl TEXT, summary TEXT, genre TEXT, source TEXT)")

t_stocks = []

def read_stocks(local_list):
    with open('S&P_500_companies.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, quotechar='|')
        for row in spamreader:
            local_list.append(row + ['False'])
    # print(local_list)
    local_list=local_list[2:]
    local_list[0][2] = 'True' # set random stocks to be tracked
    local_list[2][2] = 'True'
    local_list[5][2] = 'True'
    local_list = [",".join(stock_list) for stock_list in local_list]
    local_list = ';'.join(local_list)
    return local_list

t_stocks = read_stocks(t_stocks)
#print(t_stocks)


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
    if not exists(username, "User"):
        #default_stocks = ",".join([stock[0] for stock in ",".split((";".split(t_stocks)))])#"AAPL,MSFT,AMZN"
        data_query("INSERT INTO User VALUES (?, ?, ?)", (username, password, t_stocks))   #default_stocks))
        return True
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
              "Health", "Science", "Sports", "Technology",
              "Weather", "Stocks"]
    
    for i, genre in enumerate(genres):
        print(f"Adding Articles for {genre}")
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
    db = sqlite3.connect("database.db")
    c = db.cursor()
    output = c.execute(f'''SELECT stocks FROM User WHERE username = "{username}"''').fetchall()
    #print(f"output: {output}")
    db.commit()
    db.close()
    #print(f"processed output: {str(output[0])[2:-3].split(',')}")
    return(str(output[0])[2:-3].split(","))

#def get_stocks(username):
#    user_stocks = []
#    db = sqlite3.connect("database.db")
#    c = db.cursor()
#    output = c.execute(f'''SELECT stocks FROM User WHERE username = "{username}"''').fetchall()
#    #print(f"output: {output}")
#    db.commit()
#    db.close()
#    output = str(output[0])[2:-3].split(";")
#    #print(output)
#    for stock in output:
#        #print(stock) in stock name theres \\ where there's apostraphe
#        info = stock.split(",")
#        #print(info)
#        if info[0].find(".") == -1: #stock ticker names w periods don't work
#            stock = [info[0], stockapi.get_price(info[0]), info[2]]
#            print(stock)
#            user_stocks.append(stock)
#    return(user_stocks)

def add_stock(user, stock):
    user_stocks = ""
    for stck in get_stocks(user):
        user_stocks += stck + ","
    user_stocks += stock
    data_query("UPDATE User SET stocks = ? WHERE username = ?", (user_stocks, user))

# print(f'db stocks: {get_stocks("soft")}')
#add_account("soft", "dev")
#add_account("t", "te")
#print(get_stocks("t"))

if __name__== "__main__":
    reset_articles()
    add_all_genres()

