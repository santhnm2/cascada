import sqlite3 as sql
database = "Cascada.db"

def insert_user(email, password, name, accountType):
	with sql.connect(database) as con:
	    cur = con.cursor()
	    cur.execute("INSERT INTO UserTable (Email, Password, Name, Type, Approved) VALUES (?,?,?,?,?)", (email, password, name, accountType, "Unapproved"))
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
	    result = cur.execute("SELECT * FROM UserTable WHERE Approved != 'Unapproved' AND Type = 'Professor'")
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
		result = cur.execute("SELECT Approved FROM UserTable WHERE Email = (?);", (emailAddress,))
		return result.fetchall()

def createClass(emailAddress, className, courseNumber, departmentName, courseDescription):
	with sql.connect(database) as con:
		cur = con.cursor()
		cur.execute("INSERT INTO ClassTable (Email, ClassName, CourseNumber, DepartmentName, CourseDescription) VALUES (?,?,?,?,?)", (emailAddress, className, courseNumber, departmentName, courseDescription))
		cur.execute("UPDATE UserTable SET Approved = 'ApprovedWithClass' WHERE Email = (?);", (emailAddress,))
		con.commit()

def getClass(emailAddress):
	with sql.connect(database) as con:
		cur = con.cursor()
		result = cur.execute("SELECT * FROM ClassTable WHERE Email = (?);", (emailAddress,))
		con.commit()
		return result.fetchall()

def getAllClasses():
	with sql.connect(database) as con:
		cur = con.cursor()
		result = cur.execute("SELECT * FROM ClassTable;")
		con.commit()
		return result.fetchall()








