from flask import Flask
from flask_cors import CORS, cross_origin
from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
import os
import sqlite3
 
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/fetch": {"origins": "http://localhost"}})

@app.route('/')
def home():
	return render_template("index.html")

@app.route('/list')
def list():
	conn = sqlite3.connect("test.db")
	conn.row_factory = sqlite3.Row
	
	cur = conn.cursor()
	cur.execute("select * from SPOKEN_TUTORIAL where FILE_NAME=? and TIME>=? and TIME<? group by RELEVANCE", ('Functions.txt', 0, 100))
	
	rows = cur.fetchall()
	# for i in range(len(rows)):
	# 	time = rows['TIME'] +  
	return render_template("list.html", rows = rows)
	 
@app.route('/fetch', methods=['GET'])
@cross_origin(origin='localhost')#, headers=['Content-Type', 'Authorization'])
def fetch():
	conn = sqlite3.connect("test.db")
	conn.row_factory = sqlite3.Row
	
	cur = conn.cursor()
	time = int(request.args['time'])
	cur.execute("select * from SPOKEN_TUTORIAL where FILE_NAME=? and TIME>=? and TIME<? and RELEVANCE=? order by SIMILARITY desc", (request.args['file'], time, time+20, 'Relevant'))
	rows_R = cur.fetchall()
	
	cur.execute("select * from SPOKEN_TUTORIAL where FILE_NAME=? and TIME>=? and TIME<? and RELEVANCE=? order by SIMILARITY desc", (request.args['file'], time, time+20, 'Slightly relevant'))
	rows_SR = cur.fetchall()
	
	cur.execute("select * from SPOKEN_TUTORIAL where FILE_NAME=? and TIME>=? and TIME<? and RELEVANCE=? order by SIMILARITY desc", (request.args['file'], time, time+20, 'Irrelevant'))
	rows_IR = cur.fetchall()
	
	R, SR, IR = '', '', ''
	counter = 0
	for row in rows_R:
		if(counter < 3):
			R += ' ' + row['LINK']
			counter += 1
	counter = 0
	if rows_SR[0] != None:
		SR = rows_SR[0]['LINK']
	if rows_IR[0] != None:
		IR = rows_IR[0]['LINK']

	response = jsonify({'Relevant': R, 'Slightly': SR, 'Irrelevant': IR})
	#print(request)
	return response
	#return 'hi'

if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run()