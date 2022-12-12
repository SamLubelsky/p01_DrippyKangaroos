import sqlite3
import newsapi
from datetime import date

users = ("(username TEXT, password TEXT)")
home_article = ("(articleId INTEGER PRIMARY KEY, date TEXT)")
article_info = ("(articleId INTEGER PRIMARY KEY, title TEXT, date_published TEXT, author TEXT, summary TEXT, url TEXT)")
past_queries = ("(query INTEGER PRIMARY KEY AUTOINCREMENT, query_text TEXT, date TEXT, articles INT)")
article_tags = ("(articleId INTEGER PRIMARY KEY, topic TEXT)")

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

create_table("Home", home_article)
create_table("News", article_info)
create_table("Tags", article_tags)
create_table("Query", past_queries)
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

def check_date(home):
    if home == True:
        home_articles = get_table_list("Home")
        for article in home_articles:
            if home_articles[1] == date.today():
                return True
    else: 
        queries = get_table_list("Query")
        for query in queries:
            if query[2] == date.today():
                return True
    return False
        
        
#def home():
    #if not (check_date(True)):
        #db = sqlite3.connect("database.db")
        #c = db.cursor()
        ## TO BE ADDED TO NEWSAPI MAYBE
            #def url(article):
            #    return article["url"]
            #def title(article):
            #    return article["title"]
            #def desc(article):
            #    return article["description"]
            #def date_published(article):
            #    return article["publishedAt"]{:10}
        ## END
        ## DOESN'T INCLUDE THE TOPICS (EX.BUSINESS) -> ALSO NO TAGS
            #for article in newsapi.headlines():
                #url = newsapi.url(article)
                #title = newsapi.title(article)
                #desc = newsapi.disc(article)
                #date = newsapi.date(article)
                #author = newsapi.author(article)
                #id = c.fetchone();
                #id = int(id[0])
                #c.execute("INSERT INTO News VALUES (?, ?, ?, ?, ?, ?)", (id, title, date, author, desc, url))
                #c.execute("INSERT INTO Home VALUES (?, ?)", (id, date.today()))
            #db.commit()
            #db.close()
    #return get_table_list("Home")