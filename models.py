import sqlite3 as sql
database = "Cascada.db"

def insert_user(email, password, name, accountType):
	with sql.connect(database) as con:
	    cur = con.cursor()
	    cur.execute("INSERT INTO UserTable (Email, Password, Name, Type) VALUES (?,?,?,?)", (email, password, name, accountType))
	    con.commit()

def get_user(email):
	with sql.connect(database) as con:
	    cur = con.cursor()
	    result = cur.execute("SELECT * FROM UserTable WHERE Email = (?)", (email,))
	    con.commit()
	    return result.fetchall()

def get_approved_professors():
	with sql.connect(database) as con:
	    cur = con.cursor()
	    result = cur.execute("SELECT * FROM UserTable WHERE Approved == 'Approved' AND Type = 'Professor'")
	    con.commit()
	    return result.fetchall()

def get_unapproved_professors():
	with sql.connect(database) as con:
	    cur = con.cursor()
	    result = cur.execute("SELECT * FROM UserTable WHERE Approved == 'Unapproved' AND Type = 'Professor'")
	    con.commit()
	    return result.fetchall()

def approveProfessor(emailAddress):
	with sql.connect(database) as con:
		cur = con.cursor()
		cur.execute("UPDATE UserTable SET Approved = 'Approved' WHERE Email = (?);", (emailAddress,))
		con.commit()

def checkApproved(emailAddress):
	with sql.connect(database) as con:
		cur = con.cursor()
		print emailAddress
		result = cur.execute("SELECT Approved FROM UserTable WHERE Email = (?);", (emailAddress,))
		return result.fetchall()