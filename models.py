import sqlite3 as sql
database = "Cascada.db"

def insert_user(email, password, name, accountType):
	with sql.connect(database) as con:
	    cur = con.cursor()
	    cur.execute("INSERT INTO UserTable (Email, Password, Name, Type) VALUES (?,?,?,?)", (email, password, name, accountType))
	    con.commit()

def get_user_password(email):
	with sql.connect(database) as con:
	    cur = con.cursor()
	    result = cur.execute("SELECT Password FROM UserTable WHERE Email = (?)", (email,))
	    con.commit()
	    return result.fetchall()