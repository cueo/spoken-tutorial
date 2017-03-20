import csv
import pickle
import numpy as np
import matplotlib.pyplot as plt

from preprocess import simple_clean
from window import get_pairwise_similarity
from lsa import lsa_similarity
from rake.rake import extract_keywords
from similarity import calculate_similarity


def get_data(path):
	scripts = []
	forums = []
	forum_data = {}
	with open('data/data.pkl', 'rb') as pklfile:
		forum_data = pickle.load(pklfile)

	with open(path, 'r', encoding='utf-8') as csvfile:
		reader = csv.reader(csvfile)
		next(reader)
		next(reader)
		for row in reader:
			script = row[2]
			link = row[3]
			relevance = row[4]
			if relevance == 'R' or relevance == 'SR':
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
							print("Couldn't find qid:", qid)
							print('Reason:', e)

	return scripts, forums


if __name__ == '__main__':
	path = 'data/Links to topics v2.1 - Sheet1.csv'
	# get the transcript and the forum data
	scripts, forums = get_data(path)
	l = len(scripts)
	evaluated_scripts = 0
	sum_sim, sub_sim, max_sim, min_sim = [], [], [], []
	lsa_sim = []
	key_sim = []
	for index in range(l):
		print('Evaluating: %d/%d' % (index, l))
		script = scripts[index]
		forum = forums[index]

		# compare using cosine similarity
		try:
			similarity = get_pairwise_similarity(script, forum)
			evaluated_scripts += 1
		except Exception as e:
			print('Exception:', e)
			print('Script:', script)
			print('Forum:', forum)
		sum_sim.append(similarity[0])
		# sub_sim.append(similarity[1])
		max_sim.append(similarity[2])
		# min_sim.append(similarity[3])

		# LSA
		documents = [simple_clean(script), ' '.join(forum)]
		lsa_sim.append(lsa_similarity(documents))

		# Keyword matching
		script_keywords = extract_keywords(documents[0])
		forum_keywords = extract_keywords(documents[1])
		try:
			sk = ' '.join([x[0] for x in script_keywords])
			fk = ' '.join([x[0] for x in forum_keywords])
			documents = [sk, fk]
			keyword_similarity = calculate_similarity(documents)[0][1]
			key_sim.append(keyword_similarity)
		except Exception as e:
			print(e)
			key_sim.append(0)

	x = np.arange(l)

	print('=' * 50)
	print('{:26}{}'.format('Sum cosine similarities:', sum_sim))
	print('{:26}{}'.format('Max cosine similarities:', max_sim))
	print('{:26}{}'.format('LSA similarities:', lsa_sim))
	print('{:26}{}'.format('Keyword similarities:', key_sim))
	print('=' * 50)

	# plot
	plt.figure(1)
	red_dot, = plt.plot(x, sum_sim, 'ro', color='red')
	blue_dot, = plt.plot(x, max_sim, 'ro', color='blue')
	green_dot, = plt.plot(x, lsa_sim, 'ro', color='green')
	orange_dot, = plt.plot(x, key_sim, 'ro', color='orange')

	plt.legend([red_dot, blue_dot, green_dot, orange_dot], ['cosine sum', 'cosine max', 'lsa', 'keyword matching'])
	plt.show()
	plt.close()

	BASE_SIMILARITY = 0.2
	n = np.arange(3)
	ss_accuracy, ms_accuracy, lsa_accuracy, key_accuracy = 0, 0, 0, 0
	for i in range(l):
		ss, ms, lsa, ks = sum_sim[i], max_sim[i], lsa_sim[i], key_sim[i]
		if ss > BASE_SIMILARITY:
			ss_accuracy += 1
		if ms > BASE_SIMILARITY:
			ms_accuracy += 1
		if lsa > BASE_SIMILARITY:
			lsa_accuracy += 1
		if ks > BASE_SIMILARITY:
			key_accuracy += 1

	ss_accuracy /= evaluated_scripts
	ms_accuracy /= evaluated_scripts
	lsa_accuracy /= evaluated_scripts
	key_accuracy /= evaluated_scripts

	x = np.arange(4)
	y = np.array([ss_accuracy, ms_accuracy, lsa_accuracy, key_accuracy])
	c = ['r', 'b', 'g', 'orange']
	area = np.pi * (50 * y) ** 2

	print('Evaluated scripts: %d/%d' % (evaluated_scripts, l))
	print('=' * 50)
	print('{:22}{}'.format('Sum cosine accuracy:', ss_accuracy))
	print('{:22}{}'.format('Max cosine accuracy:', ms_accuracy))
	print('{:22}{}'.format('LSA accuracy:', lsa_accuracy))
	print('{:22}{}'.format('Keyword accuracy:', key_accuracy))
	print('=' * 50)

	# accuracy plot
	plt.figure(2)
	plt.scatter(x, y, s=area, c=c, alpha=0.7, label='Cosine')
	plt.ylabel('accuracy')
	plt.show()
	plt.close()
