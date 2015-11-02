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

if __name__ == '__main__':
	app.run(debug=True)
