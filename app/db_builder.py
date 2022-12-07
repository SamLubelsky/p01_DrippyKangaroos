import sqlite3


users = ("(username TEXT, password TEXT)")
article = 
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
    if not(used(username,"User")):
        data_query("INSERT INTO User VALUES (?, ?)", (username, password))
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
