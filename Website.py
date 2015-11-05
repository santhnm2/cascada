from flask import render_template, make_response, request, Flask, redirect, url_for
from models import *
from Professor import Professor

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def mainPage():
	if request.method == 'POST':
		account = get_user(request.form['email'])
		if len(account) > 0:
			if request.form['password'] == account[0][1]:
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
		return render_template('signin.html')


@app.route('/createAccount', methods=['POST'])
def createAccount():
	if len(get_user(request.form['email'])) > 0:
		return render_template('signin.html', signUpError="Email already exists")
	insert_user(request.form['email'], request.form['password'], request.form['name'], request.form['accountType'])
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
		approvedProfList.append(Professor(approved[3], approved[0]))
	for unapproved in unapprovedProfs:
		unapprovedProfList.append(Professor(unapproved[3], unapproved[0]))
	return render_template('adminpage.html', approved=approvedProfList, unapproved=unapprovedProfList)

def checkAdmin(req):
	currUser = req.cookies.get('username')
	if get_user(currUser)[0][2] != "Admin":
		return False
	return True

@app.route('/createClass', methods=['GET', 'POST'])
def createClassPage():
	return render_template('createClass.html')

@app.route('/unapproved')
def createUnapprovedPage():
	return render_template('unapproved.html')

@app.route('/professorPage', methods=['GET', 'POST'])
def professorPage():
	if request.method == 'POST':
		email = request.cookies.get('username')
		className = request.form.get('className', None)
		courseNumber = request.form.get('courseNumber', None)
		departmentName = request.form.get('departmentName', None)
		courseDescription = request.form.get('courseDescription', None)
		createClass(email, className, courseNumber, departmentName, courseDescription)

	account = get_user(request.cookies.get('username'))[0]
	if account[2] == "Professor":
		isApproved = checkApproved(account[0])[0][0]
		if isApproved == 'Unapproved':
			return redirect('/unapproved')
		elif isApproved == 'Approved':
			return redirect('/createClass')
		else:
			profClass = getClass(account[0])[0]
			return render_template('professor.html', currClass=profClass)
	else:
		return render_template('signin.html', loginError="Please sign in as professor to visit this page")


@app.route('/studentPage', methods=['GET', 'POST'])
def studentPage():

	account = get_user(request.cookies.get('username'))[0]
	if account[2] == 'Student':
		classes = getAllClasses()
		return render_template('student.html', classList=classes)
	else:
		return render_template('signin.html', loginError='Please sign in as student to visit this page')

if __name__ == '__main__':
	app.run(debug=True)













