from preprocess import clean
from datetime import datetime

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
	path = 'scripts/C and Cpp/First-C-Program.txt'
	script, time_intervals = calculate_interval(path)
	snippets = []
	for t in xrange(len(time_intervals)):
		snippet = ' '.join(script[t:time_intervals[t]])
		snippets.append(snippet)
	for index, snippet in enumerate(snippets):
		print index, snippet, '\n'

	# compare snippet against forum text
	pass
