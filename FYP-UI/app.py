from flask import Flask, render_template, request, jsonify
import os
import sqlite3
import pickle

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['CORS_HEADERS'] = 'Content-Type'

with open('../data/title.pkl', 'rb') as f:
	titles = pickle.load(f)


@app.route('/')
def home():
	return render_template("index.html")


@app.route('/tutorial')
def tutorial():
	return render_template("tutorial.html")


@app.route('/list')
def url_list():
	conn = sqlite3.connect("test.db")
	conn.row_factory = sqlite3.Row

	cur = conn.cursor()
	cur.execute("SELECT * FROM SPOKEN_TUTORIAL WHERE FILE_NAME=? AND TIME>=? AND TIME<? GROUP BY RELEVANCE",
				('Functions.txt', 0, 100))

	rows = cur.fetchall()
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
	response = jsonify({'links': all_})
	return response


@app.route('/getTitle')
def get_title():
	qid = str(request.args['url']).split('/')[-1]
	response = jsonify(({'title': titles[qid]}))
	return response


@app.route('/getTopics')
def get_topics():
	file_list = []
	for dir_ in os.listdir("../data"):
		if dir_ == request.args['course']:
			for file in os.listdir(os.path.join("../data", dir_)):
				f = file.split('.')[0].split('-')
				file_name = ' '.join(f)
				file_list.append(file_name)
			break
	response = jsonify({'files': file_list})
	return response


if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run(debug=True)
