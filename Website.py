from flask import render_template, make_response, request, Flask, redirect, url_for, flash, Response
from models import *
from Professor import Professor
import datetime
import pygal
import hashlib
from boxsdk import OAuth2
import os
from boxview import boxview
import urlparse
from time import sleep
import webbrowser

app = Flask(__name__)
global salt
salt = "3sn34E03rj"
view_api_key = 'xlrf76qka1j7egv5b7338kcmpthxu455'


@app.route('/', methods=['GET', 'POST'])
def mainPage():
	if request.method == 'POST':
		account = get_user(request.form['email'])
		if len(account) > 0:
			if checkLoginCreds(account):
				resp = ""
				if account[0][2] == "Admin":
					resp = make_response(redirect('/adminpage'))
				elif account[0][2] == 'Professor':
					resp = make_response(redirect('/professorPage'))
				elif account[0][2] == 'Student':
					resp = make_response(redirect('studentPage')) 	
				else:
					resp = make_response(redirect('logged in as something besides admin/prof'))
				resp.set_cookie('username', request.form['email'])
 				return resp
			else:
				return render_template('signin.html', loginError="Wrong password")
		else:
			return render_template('signin.html', loginError="Email not found in database")
	else:
		if 'username' in request.cookies:
			userType = get_user(request.cookies.get('username'))[0][2]
			if userType == "Student":
				return redirect('studentPage')
			elif userType == "Professor":
				return redirect('/professorPage')
			else:
				return redirect('/adminpage')
		else:
			return render_template('signin.html')

def checkLoginCreds(account):
	return account[0][1] == hashlib.sha224(salt + request.form['password']).hexdigest()

@app.route('/createAccount', methods=['POST'])
def createAccount():
	if len(get_user(request.form['email'])) > 0:
		flash(request.form['email'] + ' already in use')
		return render_template('signin.html', signUpError="Email already exists")
	accountType = ''
	if request.form.get('signUpStudent', None):
		accountType = 'Student'
	elif request.form.get('signUpProfessor', None):
		accountType = 'Professor'

	hashDigest = hashlib.sha224(salt + request.form['password']).hexdigest()

	insert_user(request.form['email'], hashDigest, request.form['name'], accountType)
	flash('Welcome to Cascada, ' + request.form['name'] + '!\nAn admin will approve your account as soon as possible.')
	return render_template("signin.html")

@app.route('/adminpage', methods=['GET', 'POST'])
def adminPage():
	if request.method == 'POST':
		profEmail = request.form.get('professorEmail', None)
		approveProfessor(profEmail)
	if 'username' not in request.cookies or checkAdmin(request) == False:
		return render_template('signin.html', loginError="Going to unauthorized page")

	approvedProfList = []
	unapprovedProfList = []
	approvedProfs = get_approved_professors()
	unapprovedProfs = get_unapproved_professors()
	for approved in approvedProfs:
		approvedProfList.append((Professor(approved[3], approved[0]), getProfStatsForAdmin(approved[0])))
	for unapproved in unapprovedProfs:
		unapprovedProfList.append(Professor(unapproved[3], unapproved[0]))
	return render_template('adminpage.html', approved=approvedProfList, unapproved=unapprovedProfList)

def checkAdmin(req):
	currUser = req.cookies.get('username')
	if get_user(currUser)[0][2] != "Admin":
		return False
	return True

def createBoxView(inputFile):
	api = boxview.BoxView(view_api_key)

	doc = api.create_document(file=inputFile, name=inputFile)

	doc_id = doc['id']

	bool(api.ready_to_view(doc_id))
	
	retry = 0
	max_retry = 3

	while True:
		try:
			session = api.create_session(doc_id, duration=300)

			ses_id = session['id']

			return api.get_session_url(ses_id)

		except boxview.RetryAfter as e:
			retry += 1
			if retry > max_retry:
				break
			else:
				sleep(e.seconds)

	return ''


@app.route('/createClass', methods=['GET', 'POST'])
def createClassPage():
	return render_template('createClass.html')

@app.route('/unapproved')
def createUnapprovedPage():
	return render_template('unapproved.html')

@app.route('/professorPage', methods=['GET', 'POST'])
def professorPage():
	if request.method == 'POST':
		if request.form.get('classForm') == 'Create class':
			email = request.cookies.get('username')
			className = request.form.get('className', None)
			courseNumber = request.form.get('courseNumber', None)
			departmentName = request.form.get('departmentName', None)
			courseDescription = request.form.get('courseDescription', None)
			if courseNumber.isdigit():
				createClass(email, className, courseNumber, departmentName, courseDescription)
		elif request.form.get('taskForm') == 'taskForm':
			assignmentName = request.form.get('assignmentName', None)
			dueDate = request.form.get('dueDates', None)
			assignmentDescription = request.form.get('assignmentDescription', None)
			inputFile = request.form.get('inputFile', None)
			print 'inputFile = ' + inputFile
			fileLink = ''
			if not os.path.exists(inputFile):
				fileLink = ''
			else:
				fileLink = createBoxView(inputFile)
			print 'fileLink = ' + fileLink
			
			vals = getMyCourse(request.cookies.get('username'))
			courseNumber = vals[0]
			departmentName = vals[1]

			students = getStudents(request.cookies.get('username'), courseNumber, departmentName)
			createTask(students, assignmentName, dueDate, assignmentDescription, courseNumber, departmentName, fileLink)
		elif request.form.get('extendForm') == 'extendForm':
			assignmentName = request.form.get('assignmentName', None)
			courseNumber = request.form.get('courseNumber', None)
			departmentName = request.form.get('departmentName', None)
			extendDate = request.form.get('dueDate', None)
			if len(extendDate) == 10:
				extendDeadline(assignmentName, courseNumber, departmentName, extendDate)

	account = get_user(request.cookies.get('username'))[0]
	if account[2] == "Professor":
		isApproved = checkApproved(account[0])[0][0]
		if isApproved == 'Unapproved':
			return redirect('/unapproved')
		elif isApproved == 'Approved':
			return redirect('/createClass')
		else:
			profClass = getClass(account[0])[0] 
			assignments = getClassAssignments(profClass[2], profClass[3])
			assignmentWithPercents = {}
			print 'Assignments:'
			for assignment in assignments:
				print assignment
				totalCompleted = getTotalCompleted(assignment[0], assignment[1], assignment[2])[0]
				totalIncompleted = getTotalIncompleted(assignment[0], assignment[1], assignment[2])[0]
				if (totalCompleted+totalIncompleted) == 0:
					assignmentWithPercents[assignment] = 0
				else:
					assignmentWithPercents[assignment] = (totalCompleted*100/(totalCompleted+totalIncompleted))
			return render_template('professor.html', currClass=profClass, name=account[3], currAssignments=assignmentWithPercents)
	else:
		return render_template('signin.html', loginError="Please sign in as professor to visit this page")


@app.route('/studentPage', methods=['GET', 'POST'])
def studentPage():
	dropped = False
	if request.method == 'POST':
		email = request.cookies.get('username')
		if request.form.get('departmentDrop', None):
			departmentName = request.form.get('departmentDrop', None)
			courseNum = request.form.get('courseNumDrop', None)
			removeClass(email, departmentName, courseNum)
			removeTasks(email, departmentName, courseNum)
			dropped = True
		else:
			assignmentName = request.form.get('assignmentName', None)
			classNum = request.form.get('classNum', None)
			markAsCompleted(email, assignmentName, classNum)
	account = get_user(request.cookies.get('username'))[0]
	if account[2] == 'Student':
		classes = getClassesForStudent(request.cookies.get('username'))
		tasks = getTasksForStudent(request.cookies.get('username'))
		now = datetime.datetime.now()
		currDate = now.strftime("%Y-%m-%d")
		completeTasks = getCompletedTasksForStudent(request.cookies.get('username'))
		if dropped:
			flash('You have dropped ' + departmentName + ' ' + courseNum)
		return render_template('student.html', classList=classes, taskList=tasks, completeTaskList=completeTasks, currDate=currDate)
	else:
		return render_template('signin.html', loginError='Please sign in as student to visit this page')

@app.route('/Assignment/<assignment>', methods=['GET', 'POST'])
def discussionBoard(assignment=None):
	if request.method == 'POST':
		if request.form.get('submitType') == 'add':
			user = request.cookies.get('username')
			parentid = request.form.get('parentid', None)
			content = request.form.get('newcomment', None)
			addPost(parentid, content, user, assignment)
		else:
			postid = request.form.get('postid', None)
			deletePost(postid)
	discussionList = getDiscussionList(assignment)
	accountType = get_user(request.cookies.get('username'))[0][2]
	return render_template('discussion.html', discussionList=discussionList, accountType=accountType, assignment=assignment)

@app.route('/gradebook', methods=['GET', 'POST'])
def profGradebook():
	if request.method == 'POST':
		grade = request.form.get('grade', None)
		feedback = request.form.get('feedback', None)
		email = request.form.get('email', None)
		assignmentName = request.form.get('assignment', None)
		courseNumber = request.form.get('courseNum', None)
		departmentName = request.form.get('departmentName', None)
		if grade.isdigit():
			gradeAssignment(grade, feedback, assignmentName, courseNumber, departmentName, email)
	email = request.cookies.get('username')
	submissions = getSubmissions(email)
	sublength = len(submissions)
	return render_template('submissions.html', submissions=submissions, sublength = sublength)

@app.route('/message', methods=['GET', 'POST'])
def getUniqueConversations():
	results = ""
	if request.method == 'POST':
		query = request.form.get('query', None)
		results = searchUsers(query)
	users = getUniqueRecipients(request.cookies.get('username'))
	return render_template('message.html', messages=users, currUser=request.cookies.get('username'), results=results)

@app.route('/conversation', methods=['GET', 'POST'])
def getConversation():
	recipient = ""
	if request.method == 'POST':
		content = request.form.get('content')
		sentFrom = request.cookies.get('username')
		recipient = request.form.get('sentTo', None)
		if content != "":
			insertMessage(content, sentFrom, recipient)
		return redirect('/conversation?sentTo=' + request.form.get('sentTo', None))
	else:
		recipient = request.args.get('sentTo')
	messages = getAllMessages(request.cookies.get('username'), recipient)
	return render_template('conversation.html', messages=messages, sentFrom=request.cookies.get('username'), sentTo=recipient)

@app.route('/registration', methods=['GET', 'POST'])
def registration():
	account = get_user(request.cookies.get('username'))[0]
	if account[2] == 'Student':
		
		departmentsRaw = getDepartments();
		departments = {}
		for dep in departmentsRaw:
			departments[dep] = True

		if request.method == 'POST':
			if request.form.get('departmentRegister'):
				department = request.form.get('departmentRegister')
				courseNumber = request.form.get('courseNumRegister')
				email = request.cookies.get('username')
				currentClasses = getClassesForStudent(email)

				registered = False

				for curClass in currentClasses:
					if curClass[4] == department and curClass[3] == courseNumber:
						registered = True
						flash('You are already registered for ' + department + ' ' + courseNumber)
						break
				if not registered:
					professorEmail = request.form.get('professorEmailRegister')
					className = request.form.get('courseNameRegister')
					courseDescription = request.form.get('courseDescriptionRegister')

					register(email, professorEmail, className, courseNumber, department, courseDescription)

					tasks = getClassAssignments(courseNumber, department)

					now = datetime.datetime.now()
					currDate = now.strftime("%Y-%m-%d")
					for task in tasks:
						if task[3] > currDate:
							addTask(email, task[0], task[1], task[2], task[3], task[4], task[5])

					flash('You are now registered for ' + department + ' ' + courseNumber)

				return render_template('register.html', departments=list(departments.keys()), searchResults=[])
			elif request.form.get('department'):
				department = request.form.get('department', None)
				keyword = request.form.get('keyword', None)
			
				if keyword == '':
					keyword = '%'
				else:
					keyword = '%' + keyword + '%'

				searchResults = searchForClasses(department, keyword)
				return render_template('register.html', departments=list(departments.keys()), searchResults=searchResults)
			else:
				return render_template('register.html', departments=list(departments.keys()), searchResults=[])
		else:
			return render_template('register.html', departments=list(departments.keys()), searchResults=[])
	else:
		return render_template('signin.html', loginError='Please sign in as a student to visit this page')

@app.route('/barchart', methods=['GET', 'POST'])
def barchart():
	if request.method == 'POST':
	    bar_chart = pygal.Bar(width=500, height=400)
	    bar_chart.title = "Assignment grades"
	    assignmentName = request.form.get('assignmentName', None)
	    grades = getGradeDistribution(assignmentName)
	    rangeCount,cutoffs = grades,['0-59','60-69', '70-79', '80-89', '90+']
	    bar_chart.add('count', rangeCount)
	    bar_chart.x_labels = cutoffs
	    return Response(response=bar_chart.render(), content_type='image/svg+xml')

@app.route('/classAverages', methods=['GET', 'POST'])
def classAverages():
	if request.method == 'POST':
		courseNumber = request.form.get('courseNumber', None)
		departmentName = request.form.get('departmentName', None)
		averages = getClassAverages(courseNumber, departmentName)
		bar_chart = pygal.Bar(width=500, height=400)
		bar_chart.title = "Class Averages"
		avgs,cutoffs = averages,['0-59', '60-69', '70-79', '80-89', '90+']
		bar_chart.add('count', avgs)
		bar_chart.x_labels = cutoffs
		return Response(response=bar_chart.render(), content_type='image/svg+xml')

@app.route('/chara', methods=['GET', 'POST'])
def chara():
	if request.method == 'POST':
		courseNumber = request.form.get('courseNumber', None)
		departmentName = request.form.get('departmentName', None)
		email = request.cookies.get('username')
		assignmentNames, assignmentGrades = getStudentGrades(email, courseNumber, departmentName)
		averageGrades = getAverageGrades(assignmentNames, courseNumber, departmentName)
		bar_chart = pygal.Bar(width=800, height=400, range=(0, 100))
		bar_chart.title = "Chara"
		grades,assignmentName = assignmentGrades,assignmentNames
		grades2,assignmentName = averageGrades,assignmentNames
		bar_chart.add('My grades', grades)
		bar_chart.add('Class avg', grades2)
		bar_chart.x_labels = assignmentName

		return Response(response=bar_chart.render(), content_type='image/svg+xml')

@app.route('/radar', methods=['GET', 'POST'])
def radar():
	if request.method == 'POST':
		courseNumber = request.form.get('courseNumber', None)
		departmentName = request.form.get('departmentName', None)
		email = request.cookies.get('username')
		assignmentNames, assignmentGrades = getStudentGrades(email, courseNumber, departmentName)
		averageGrades = getAverageGrades(assignmentNames, courseNumber, departmentName)
		radar_chart = pygal.Radar(range=(0, 100))
		radar_chart.title = 'Grades'
		radar_chart.x_labels = assignmentNames
		radar_chart.add(email, assignmentGrades)
		radar_chart.add('averages', averageGrades)
		return Response(response=radar_chart.render(), content_type='image/svg+xml')


@app.route('/logout', methods=['GET'])
def logOutFromWebsite():
	resp = make_response(render_template('signin.html'))
	resp.set_cookie('username', '', expires=0)
	return resp

if __name__ == '__main__':
	app.secret_key = 'some_secret'
	app.run(debug=True)










