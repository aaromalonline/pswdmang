import sqlite3
import random,string


dbconn = sqlite3.connect("./vault.db")
dbcur = dbconn.cursor()

def dbwriter():
    return dbcur

def initialisedb():
    dbcur.execute("CREATE TABLE IF NOT EXISTS ENTRIES (no INTEGER PRIMARY KEY AUTOINCREMENT, sitename TEXT NOT NULL, password TEXT)")
    dbcur.execute("CREATE TABLE IF NOT EXISTS USERS (user TEXT, masterpass TEXT)")

def currentuser():
    dbcur.execute("SELECT * FROM USERS")
    return dbcur.fetchone()

def registeruser(username, masterpass):
    dbcur.execute("INSERT INTO USERS(user,masterpass) VALUES (?,?)",(username,masterpass))
    return True

def authenticateuser(masterpass):
    user = currentuser()
    if masterpass == user[1]:
        return True
    else:
        return False

def checkentry(entryno):
    dbcur.execute("SELECT no FROM ENTRIES")
    entrynos = [item[0] for item in list(dbcur.fetchall())]
    return entryno in entrynos

def generatepass(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k = length))

def closevault():
    dbconn.commit()
    dbconn.close()

 