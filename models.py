import sqlite3 as sql
from Post import Post
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

def getClassesForStudent(emailAddress):
	with sql.connect(database) as con:
		cur = con.cursor()
		result = cur.execute("SELECT * FROM StudentClasses WHERE Email = (?);", (emailAddress,))
		con.commit()
		return result.fetchall()

def getTasksForStudent(emailAddress):
	with sql.connect(database) as con:
		cur = con.cursor()
		result = cur.execute("SELECT * FROM AssignmentTable WHERE Email = (?) AND Completed='Not Completed';", (emailAddress,))
		con.commit()
		return result.fetchall()

def getCompletedTasksForStudent(emailAddress):
	with sql.connect(database) as con:
		cur = con.cursor()
		result = cur.execute("SELECT AssignmentName, DueDate, Graded, Grade, Feedback FROM AssignmentTable WHERE Email = (?) AND Completed='Completed';", (emailAddress,))
		con.commit()
		return result.fetchall()	

def getClassAssignments(courseNumber, departmentName):
	with sql.connect(database) as con:
		cur = con.cursor()
		result = cur.execute("SELECT * FROM AssignmentList WHERE CourseNumber = (?) AND DepartmentName = (?);", (courseNumber, departmentName, ))
		con.commit()
		return result.fetchall()

def getMyCourse(professorEmail):
	with sql.connect(database) as con:
		cur = con.cursor()
		result = cur.execute("SELECT CourseNumber, DepartmentName FROM ClassTable WHERE Email = (?);", (professorEmail,))
		con.commit()
		return result.fetchall()[0]


def getStudents(professorEmail, courseNumber, departmentName):
	with sql.connect(database) as con:
		cur = con.cursor()
		result = cur.execute("SELECT Email FROM StudentClasses WHERE CourseNumber = (?) AND DepartmentName = (?);", (courseNumber, departmentName,))
		con.commit()
		return result.fetchall()

def createTask(studentEmails, assignmentName, dueDate, assignmentDescription, courseNumber, departmentName):
	with sql.connect(database) as con:
		cur = con.cursor()
		cur.execute("INSERT INTO AssignmentList (AssignmentName, CourseNumber, DepartmentName, DueDate, AssignmentDescription) VALUES (?,?,?,?,?)", (assignmentName, courseNumber, departmentName, dueDate, assignmentDescription))
		for email in studentEmails:
			cur.execute("INSERT INTO AssignmentTable (Email, AssignmentName, Completed, DueDate, AssignmentDescription, CourseNumber, DepartmentName) VALUES (?,?,?,?,?,?,?)", (email[0], assignmentName, "Not Completed", dueDate, assignmentDescription, courseNumber, departmentName,))
		con.commit()

def addTask(email, assignmentName, courseNumber, departmentName, dueDate, assignmentDescription):
	with sql.connect(database) as con:
		cur = con.cursor()
		cur.execute("INSERT INTO AssignmentTable (Email, AssignmentName, Completed, DueDate, AssignmentDescription, CourseNumber, DepartmentName) VALUES (?,?,?,?,?,?,?)", (email, assignmentName, "Not Completed", dueDate, assignmentDescription, courseNumber, departmentName,))
		con.commit()	

def markAsCompleted(email, assignmentName, classNum):
	with sql.connect(database) as con:
		cur = con.cursor()
		cur.execute("UPDATE AssignmentTable SET Completed = 'Completed' WHERE Email = (?) AND AssignmentName = (?) AND CourseNumber = (?);", (email,assignmentName,classNum,))
		con.commit()

def getTotalCompleted(assignmentName, classNum, departmentName):
	with sql.connect(database) as con:
		cur = con.cursor()
		completed = cur.execute("SELECT COUNT(*) FROM AssignmentTable WHERE AssignmentName = (?) AND CourseNumber = (?) AND DepartmentName = (?) AND Completed='Completed';", (assignmentName, classNum, departmentName,))
		con.commit()
		return completed.fetchall()[0]

def getTotalIncompleted(assignmentName, classNum, departmentName):
	with sql.connect(database) as con:
		cur = con.cursor()
		incompleted = cur.execute("SELECT COUNT(*) FROM AssignmentTable WHERE AssignmentName = (?) AND CourseNumber = (?) AND DepartmentName = (?) AND Completed='Not Completed';", (assignmentName, classNum, departmentName,))
		con.commit()
		return incompleted.fetchall()[0]

def getDepartments():
	with sql.connect(database) as con:
		cur = con.cursor()
		result = cur.execute("SELECT DepartmentName FROM ClassTable;")
		con.commit()
		return result.fetchall()

def extendDeadline(assignmentName, classNum, departmentName, extendDate):
	with sql.connect(database) as con:
			cur = con.cursor()
			cur.execute("UPDATE AssignmentTable SET DueDate = (?) WHERE AssignmentName = (?) AND CourseNumber = (?) AND DepartmentName = (?);", (extendDate,assignmentName,classNum,departmentName,))
			con.commit()

def searchForClasses(department, keyword):
	with sql.connect(database) as con:
		cur = con.cursor()
		result = cur.execute("SELECT * FROM ClassTable WHERE departmentName = (?) AND CourseDescription LIKE (?);", (department, keyword, ))
		con.commit()
		return result.fetchall()	

def register(email, professorEmail, className, courseNumber, departmentName, courseDescription):
	with sql.connect(database) as con:
		cur = con.cursor()
		cur.execute("INSERT INTO StudentClasses (Email, ProfessorEmail, ClassName, CourseNumber, DepartmentName, CourseDescription) VALUES (?,?,?,?,?,?)", (email, professorEmail, className, courseNumber, departmentName, courseDescription,))
		con.commit()
		# return result.fetchall()	

def getSubmissions():
	with sql.connect(database) as con:
		cur = con.cursor()
		result = cur.execute("SELECT Email, AssignmentName, DueDate, CourseNumber, DepartmentName FROM AssignmentTable WHERE Graded = 'Not Graded' AND Completed = 'Completed';")
		con.commit()
		return result.fetchall()

def gradeAssignment(grade, feedback, assignmentName, courseNumber, departmentName, email):
	with sql.connect(database) as con:
		cur = con.cursor()
		cur.execute("UPDATE AssignmentTable SET Grade = (?), Feedback = (?), Graded='Graded' WHERE AssignmentName = (?) AND CourseNumber = (?) AND DepartmentName = (?) AND Email = (?);", (grade,feedback,assignmentName,courseNumber,departmentName,email,))
		con.commit()

def getDiscussionList(assignmentName):
	sortedComments = []
	getChildren(assignmentName, sortedComments, 0, -1)
	return sortedComments

def getChildren(assignmentName, sortedComments, level, parentid):
	#c.execute("SELECT * FROM comments WHERE projectname = '%s'" % symbol)
	with sql.connect(database) as con:
		cur = con.cursor()
		result = cur.execute("SELECT * FROM Discussion WHERE AssignmentName = (?) AND ParentId = (?);", (assignmentName, parentid, )).fetchall()
		if len(result) == 0:
			return
		else:
			for post in result:
				sortedComments.append(Post(post[2], level, post[0], post[1], post[3], post[4]))
				getChildren(assignmentName, sortedComments, level+1, post[0])

def addPost(parentid, content, user, assignment):
	with sql.connect(database) as con:
		cur = con.cursor()
		cur.execute("INSERT INTO Discussion (ParentId, Content, User, AssignmentName) VALUES (?,?,?,?)", (parentid, content, user, assignment,))
		con.commit()

def deletePost(postid):
	with sql.connect(database) as con:
		cur = con.cursor()
		result = cur.execute("SELECT * FROM Discussion WHERE ParentId = (?);", (postid,)).fetchall()
		cur.execute("DELETE FROM Discussion WHERE PostId = (?);", (postid,))
		con.commit()
		if len(result) == 0:
			return
		else:
			for post in result:
				deletePost(post[0])

def getUniqueRecipients(user):
	with sql.connect(database) as con:
		cur = con.cursor()
		result = cur.execute("SELECT DISTINCT SentFrom, SentTo FROM (SELECT SentFrom, SentTo FROM Message UNION ALL SELECT SentTo, SentFrom FROM Message) WHERE SentFrom < SentTo AND (SentFrom = (?) OR SentTo = (?));", (user, user,)).fetchall()
		con.commit()
		return result

def getAllMessages(sentFrom, sentTo):
	with sql.connect(database) as con:
		cur = con.cursor()
		result = cur.execute("SELECT * FROM Message WHERE (sentFrom=(?) AND sentTo=(?)) OR (sentFrom=(?) AND sentTo=(?)) ", (sentFrom, sentTo, sentTo, sentFrom)).fetchall()
		con.commit()
		return result

def insertMessage(content, sentFrom, sentTo):
	with sql.connect(database) as con:
		cur = con.cursor()
		result = cur.execute("INSERT INTO Message (SentFrom, SentTo, Content) VALUES (?,?,?)", (sentFrom, sentTo, content,))
		con.commit()
		return result

def getGradeDistribution(assignmentName):
	with sql.connect(database) as con:
		cur = con.cursor()
		fGrade = cur.execute("SELECT COUNT(*) FROM AssignmentTable WHERE AssignmentName = (?) AND Graded='Graded' AND Grade <= 59;", (assignmentName,)).fetchall()[0]
		dGrade = cur.execute("SELECT COUNT(*) FROM AssignmentTable WHERE AssignmentName = (?) AND Graded='Graded' AND Grade >= 59 AND Grade <= 69;", (assignmentName,)).fetchall()[0]
		cGrade = cur.execute("SELECT COUNT(*) FROM AssignmentTable WHERE AssignmentName = (?) AND Graded='Graded' AND Grade >= 69 AND Grade <= 79;", (assignmentName,)).fetchall()[0]
		bGrade = cur.execute("SELECT COUNT(*) FROM AssignmentTable WHERE AssignmentName = (?) AND Graded='Graded' AND Grade >= 79 AND Grade <= 89;", (assignmentName,)).fetchall()[0]
		aGrade = cur.execute("SELECT COUNT(*) FROM AssignmentTable WHERE AssignmentName = (?) AND Graded='Graded' AND Grade >= 90;", (assignmentName,)).fetchall()[0]
		con.commit()
		grades = [fGrade[0], dGrade[0], cGrade[0], bGrade[0], aGrade[0]]
		return grades

def searchUsers(query):
	with sql.connect(database) as con:
		cur = con.cursor()
		query = "%" + query + "%"
		result = cur.execute("SELECT * FROM UserTable WHERE Email LIKE (?) OR Name LIKE (?)", (query, query,)).fetchall()
		con.commit()
		return result

def removeClass(email, departmentName, courseNumber):
	with sql.connect(database) as con:
		cur = con.cursor()
		cur.execute("DELETE FROM StudentClasses WHERE Email = (?) AND CourseNumber = (?) AND DepartmentName = (?);", (email, courseNumber, departmentName, ))
		con.commit()

def removeTasks(email, departmentName, courseNumber):
	with sql.connect(database) as con:
		cur = con.cursor()
		cur.execute("DELETE FROM AssignmentTable WHERE Email = (?) AND CourseNumber = (?) AND DepartmentName = (?);", (email, courseNumber, departmentName, ))
		con.commit()

def getClassAverages(courseNumber, departmentName):
	classAverages = [0, 0, 0, 0, 0]
	with sql.connect(database) as con:
		cur = con.cursor()
		result = cur.execute("SELECT DISTINCT Email FROM AssignmentTable WHERE CourseNumber=(?) AND DepartmentName=(?) AND Graded='Graded';", (courseNumber, departmentName, )).fetchall()
		for student in result:
			average = cur.execute("SELECT AVG(Grade) FROM AssignmentTable WHERE CourseNumber=(?) AND DepartmentName=(?) AND Graded='Graded' AND Email=(?);", (courseNumber, departmentName, student[0], )).fetchall()[0][0]
			if average <= 59:
				classAverages[0]+=1
			elif average <= 69:
				classAverages[1]+=1
			elif average <=79:
				classAverages[2]+=1
			elif average <=89:
				classAverages[3]+=1
			else:
				classAverages[4]+=1
	return classAverages
