import csv
import pickle
from stack import get_answers
import os


def fetch_answer_from_link(link):
	details = link.split('/')
	site = details[2]
	qid = details[-2]
	if qid not in qids:
		try:
			print('Fetching:', link)
			question, answers = get_answers(qid, site)
			qids[qid] = [question] + answers
		except Exception as e:
			print("Couldn't fetch, error:", e)
	else:
		print('Already fetched question:', qid)


def get_questions(path):
	with open(path, 'r', encoding='utf-8') as csvfile:
		reader = csv.reader(csvfile)
		# dictionary of StackExchange with key=question id and value=question + answer text
		next(reader)
		for row in reader:
			link = row[3]
			if link:
				if '\n' in link:
					links = link.split()
				else:
					links = [link]
				for l in links:
					fetch_answer_from_link(l)
	return qids


if __name__ == '__main__':
	path = 'data/Links to topics v2.1 - Sheet1.csv'
	pickle_path = 'data/data.pkl'
	qids = {}
	if os.path.exists(pickle_path):
		with open(pickle_path, 'rb') as f:
			qids = pickle.load(f)
	get_questions(path)
	# for k, v in qids.items():
	# 	print(k, v)
	with open(pickle_path, 'wb') as f:
		pickle.dump(qids, f)
