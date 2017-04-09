import pickle
import os

from preprocess import clean
from datetime import datetime
from stack import get_answers
from similarity import calculate_similarity

# window of n seconds
interval = 20


def calculate_interval(path):
	"""
	Given a transcript file, create snippets of time interval = interval.
	script = each line in the transcript (broken at the subtitle timing breaks)
	times = timestamps in the video corresponding to each of the lines in the script
	time_interval_index = a list where each element, i, is the index of the list times
		such that script[i] and script[times[i]] are interval seconds apart
		therefore, the window = snippet between script[i] and script[time_interval_index[i]]
	"""
	with open(path, 'r', encoding='utf-8') as f:
		text = clean(f.read())
	script = [x[0] for x in text]
	times = [x[1] for x in text]

	time_interval_index = []
	l = len(times)
	fmt = '%M:%S'
	for i in range(l):
		for j in range(i+1, l):
			t1, t2 = times[i], times[j]
			tdelta = datetime.strptime(t2, fmt) - datetime.strptime(t1, fmt)
			if tdelta.total_seconds() >= interval:
				time_interval_index.append(j)
				break
		else:
			time_interval_index.append(l-1)
	return script, time_interval_index, times


def get_pairwise_similarity(snippet, forum_texts):
	sum_similarity, sub_similarity, max_similarity, min_similarity = [], [], [], []
	sum_sim, sub_sim, max_sim, min_sim = 0, 1, 0, 999
	l = len(forum_texts)

	for post in forum_texts:
		temp = calculate_similarity([snippet, post])[0][1]

		# sum the pairwise similarity for each post (normalize in the end)
		sum_sim += temp

		# take the max of pairwise similarity for the posts
		if temp > max_sim:
			max_sim = temp

		# take the min of pairwise similarity for the posts
		if temp < min_sim:
			min_sim = temp
	sum_sim /= l
	sub_sim -= sum_sim

	return [sum_sim, sub_sim, max_sim, min_sim]


if __name__ == '__main__':
	path = 'data/C and Cpp/First-C-Program.txt'
	script, time_intervals, times = calculate_interval(path)
	snippets = []
	for t in range(len(time_intervals)):
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
		with open(path, 'rb') as f:
			stack_data = pickle.load(f)
			qids = list(stack_data.keys())
	forum_texts = []
	for id_ in ids:
		if id_ in qids:
			forum_texts.append(stack_data[id_])
		else:
			print('Fetching:', id_)
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
	print('Relevant id:', ids[-1])
	print('Irrelevant ids:', ids[:-1])
	print('=' * 100)
	for index in range(len(forum_texts)):
		forum = forum_texts[index]
		print('Comparing with id:', ids[index])
		similarity = get_pairwise_similarity(snippets[73], forum)

		print('Snippet:', snippets[73])
		print('Forum text:', forum)
		print('-' * 50)
		print('Similarity:')
		print('Sum similarity:', similarity[0])
		print('Sub similarity:', similarity[1])
		print('Max similarity:', similarity[2])
		print('Min similarity:', similarity[3])
		print('=' * 50)

	"""
	Compare data against relevant and irrelevant forums.
	"""

