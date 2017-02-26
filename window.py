import pickle
import os

from preprocess import clean
from datetime import datetime
from stack import get_answers
from similarity import calculate_similarity

# window of 60 seconds
interval = 60


def calculate_interval(path):
	"""
	Given a transcript file, create snippets of time interval = interval.
	script = each line in the transcript (broken at the subtitle timing breaks)
	times = timestamps in the video corresponding to each of the lines in the script
	time_interval_index = a list where each element, i, is the index of the list times
		such that scripts[i] and scripts[times[i]] are interval seconds apart
		therefore, the window = snippet between scripts[i] and scripts[times[i]]
	"""
	with open(path, 'r') as f:
		text = clean(f.read())
	script = [x[0] for x in text]
	times = [x[1] for x in text]

	time_interval_index = []
	l = len(times)
	fmt = '%M:%S'
	for i in xrange(l):
		for j in xrange(i+1, l):
			t1, t2 = times[i], times[j]
			tdelta = datetime.strptime(t2, fmt) - datetime.strptime(t1, fmt)
			if tdelta.total_seconds() >= 60:
				time_interval_index.append(j)
				break
		else:
			time_interval_index.append(l-1)
	return script, time_interval_index


if __name__ == '__main__':
	path = 'data/C and Cpp/First-C-Program.txt'
	script, time_intervals = calculate_interval(path)
	snippets = []
	for t in xrange(len(time_intervals)):
		snippet = ' '.join(script[t:time_intervals[t]])
		snippets.append(snippet)
	'''
	for index, snippet in enumerate(snippets):
		print index, snippet, '\n'
	'''

	"""
	Compare snippet against forum text
	"""
	# first two ids are irrelevant, last two are relevant
	ids = ['23774466', '333889', '571076', '3661251']
	qids = []
	path = 'data/data.pkl'
	if os.path.exists(path):
		with open(path, 'r') as f:
			stack_data = pickle.load(f)
			qids = stack_data.keys()
	forum_texts = []
	for id_ in ids:
		if id_ in qids:
			forum_texts.append(stack_data[id_])
		else:
			print 'Fetching:', id_
			question, answers = get_answers(id_)
			"""
			Model for vanilla comparison
			"""
			# forum_texts.append(question + '\n' + ' '.join(answers))
			"""
			Bag of post model
			"""
			forum_texts.append([question] + answers)
	"""
	Pairwise similarity without learning weight of upvotes
	"""
	similarity = []
	for text in forum_texts:
		sim = 0
		l = len(text)
		for post in text:
			# sum the pairwise similarity for each post (normalize in the end)
			sim += calculate_similarity([snippets[73], post])[0][1]

			# take the max of pairwise similarity for the posts
			# temp = calculate_similarity([snippets[73], post])[0][1]
			# if temp > sim:
			# 	sim = temp
		sim /= l
		similarity.append(sim)
	print 'Snippet:', snippets[73]
	print 'Forum text:', forum_texts
	print similarity

	"""
	Compare data against relevant and irrelevant forums.
	"""

