from preprocess import clean
from datetime import datetime
from stack import get_answers
from similarity import calculate_similarity

# window of 60 seconds
interval = 60


def calculate_interval(path):
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

	# compare snippet against forum text
	ids = ['2377466', '333889', '571076', '3661251']
	forum_texts = []
	for id_ in ids:
		print 'Fetching:', id_
		question, answers = get_answers(id_)
		forum_texts.append(question + '\n' + ' '.join(answers))
	print 'Snippet:', snippets[73]
	print 'Forum text:', forum_texts
	calculate_similarity([snippets[73]] + forum_texts)
