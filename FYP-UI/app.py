from flask import Flask
from flask_cors import CORS, cross_origin
from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify, send_from_directory
import os
import sqlite3
import urllib.request
from bs4 import BeautifulSoup

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
def home():
	return render_template("index.html")


@app.route('/list')
def url_list():
	conn = sqlite3.connect("test.db")
	conn.row_factory = sqlite3.Row

	cur = conn.cursor()
	cur.execute("SELECT * FROM SPOKEN_TUTORIAL WHERE FILE_NAME=? AND TIME>=? AND TIME<? GROUP BY RELEVANCE",
				('Functions.txt', 0, 100))

	rows = cur.fetchall()
	# for i in range(len(rows)):
	# time = rows['TIME'] +
	return render_template("list.html", rows=rows)


@app.route('/fetch', methods=['GET'])
def fetch():
	conn = sqlite3.connect("test.db")
	conn.row_factory = sqlite3.Row

	cur = conn.cursor()
	time = int(request.args['time'])
	cur.execute(
		"SELECT * FROM SPOKEN_TUTORIAL WHERE FILE_NAME=? AND TIME>=? AND TIME<? AND RELEVANCE=? ORDER BY SIMILARITY DESC",
		(request.args['file'], time, time + 20, 'Relevant'))
	rows_r = cur.fetchall()

	cur.execute(
		"SELECT * FROM SPOKEN_TUTORIAL WHERE FILE_NAME=? AND TIME>=? AND TIME<? AND RELEVANCE=? ORDER BY SIMILARITY DESC",
		(request.args['file'], time, time + 20, 'Slightly relevant'))
	rows_sr = cur.fetchall()

	cur.execute(
		"SELECT * FROM SPOKEN_TUTORIAL WHERE FILE_NAME=? AND TIME>=? AND TIME<? AND RELEVANCE=? ORDER BY SIMILARITY DESC",
		(request.args['file'], time, time + 20, 'Irrelevant'))
	rows_ir = cur.fetchall()

	r, sr, ir = '', '', ''
	counter = 0
	for row in rows_r:
		if counter < 3:
			r += ' ' + row['LINK']
			counter += 1
	# counter = 0
	if rows_sr[0]:
		sr = rows_sr[0]['LINK']
	if rows_ir[0]:
		ir = rows_ir[0]['LINK']

	# response = jsonify({'Relevant': R, 'Slightly': SR, 'Irrelevant': IR})
	all_ = r + ' ' + sr + ' ' + ir
	response = jsonify({'Links': all_})
	return response


@app.route('/gettitle')
def get_title():
	soup = BeautifulSoup(urllib.request.urlopen(request.args['url']), "lxml")
	response = jsonify({'title': soup.title.string})
	return response


if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run(debug=True)
