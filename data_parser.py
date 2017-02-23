import csv
import pickle


def get_questions(path):
	with open(path) as csvfile:
		reader = csv.reader(csvfile)
		# dictionary of StackExchange with key=question id and value=question text
		qids = {}
		reader.next()
		reader.next()
		for row in reader:
			link = row[3]
			if link:
				if '\n' in link:
					links = link.split()
				else:
					links = [link]
				for l in links:
					qid = l.split('/')[-2]
					qids[qid] = l
	return qids


if __name__ == '__main__':
	path = 'data/Links to topics v2.1 - Sheet1.csv'
	qids = get_questions(path)
	# for k, v in qids.items():
	# 	print k, v
	with open('data.pkl', 'w') as f:
		pickle.dump(qids, f)
