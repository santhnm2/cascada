from flask import Flask
from flask import request
from flask import render_template
from models import *

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def mainPage():
	if request.method == 'POST':
		if len(storedPass = get_user_password(request.form['email'])) > 0:
			if request.form['password'] == storedPass[0][0]:
				return 'hello'
			else:
				return render_template('signin.html', loginError="Wrong password")
		else:
			return render_template('signin.html', loginError="Email not found in database")
	else:
		return render_template('signin.html')


@app.route('/createAccount', methods=['POST'])
def createAccount():
	if len(get_user_password(request.form['email'])) > 0:
		return render_template('signin.html', signUpError="Email already exists")
	insert_user(request.form['email'], request.form['password'], request.form['name'], request.form['accountType'])
	return "add user page here"

if __name__ == '__main__':
	app.run(debug=True)
