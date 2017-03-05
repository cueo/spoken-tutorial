import csv
import pickle
import numpy as np
import matplotlib.pyplot as plt

from stack import get_answers
from window import get_pairwise_similarity


def get_data(path):
	scripts = []
	forums = []
	forum_data = {}
	with open('data/data.pkl', 'r') as pklfile:
		forum_data = pickle.load(pklfile)

	with open(path, 'r') as csvfile:
		reader = csv.reader(csvfile)
		reader.next()
		for row in reader:
			script = row[2]
			link = row[3]
			# check if scripts are empty (because incomplete data)
			if script:
				# if a script has more than one matching forums, taking just the first one
				if '\n' in link:
					link = link.split('\n')[0]
				details = link.split('/')
				# check if the links are proper (because discrepancies in data)
				if len(details) > 5:
					site = details[2]
					qid = details[-2]
					try:
						forum = forum_data[qid]
						scripts.append(script)
						forums.append(forum)
					except Exception as e:
						print "Couldn't find qid:", qid
						print 'Reason:', e

	return scripts, forums


if __name__ == '__main__':
	path = 'data/Links to topics v2.1 - Sheet1.csv'
	# get the transcript and the forum data
	scripts, forums = get_data(path)
	l = len(scripts)
	# compare using cosine similarity
	sum_sim, sub_sim, max_sim, min_sim = [], [], [], []
	for index in xrange(l):
		print index
		script = scripts[index]
		forum = forums[index]
		try:
			similarity = get_pairwise_similarity(script, forum)
		except Exception as e:
			print 'Exception:', e
			print 'Script:', script
			print 'Forum:', forum
		sum_sim.append(similarity[0])
		sub_sim.append(similarity[1])
		max_sim.append(similarity[2])
		min_sim.append(similarity[3])
	x = np.arange(l)

	# plot
	plt.plot(x, sum_sim, 'ro', color='red', )
	plt.plot(x, sub_sim, 'ro', color='blue')
	plt.plot(x, max_sim, 'ro', color='green')
	plt.plot(x, min_sim, 'ro', color='yellow')

	plt.show()
