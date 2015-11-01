from flask import Flask
from flask import request
import sqlite3
import xml.etree.ElementTree as ET
from flask import render_template
import json

app = Flask(__name__)

@app.route('/')
def hello(name=None):
	return render_template('signin.html')

@app.route('/<name>', methods=['GET', 'POST'])
def hello2(name=None):
	commentList = getCommentList(assignments[name].getName())
	return render_template('files.html', name=assignments[name], comments=commentList)

if __name__ == '__main__':
	app.run(debug=True)
